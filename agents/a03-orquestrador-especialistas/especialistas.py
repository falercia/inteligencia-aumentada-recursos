"""Wrappers que transformam prompts de /prompts/ em tools chamáveis.

Cada especialista é construído a partir de um diretório em /prompts/<ID>/, que
contém o golden set, a configuração de eval e (em release futuro) o XML do
prompt em si. Aqui simulamos o XML inline com o ID e a descrição editorial
do prompt, suficiente para o agente operar.

Decisão deliberada: a tool exposta ao orquestrador é UMA por especialista,
nominal (ex.: `especialista_juridico_trabalhista`), com schema enxuto e
descrição que explica claramente quando o orquestrador DEVE chamar e quando
NÃO DEVE. Schema enxuto reduz a chance de o orquestrador inventar campos.

Em produção, esta camada vira:
- carregamento dinâmico do XML de /prompts/<ID>/prompt.xml
- versionamento por hash do conteúdo
- cache de prompt (Capítulo 18) para reduzir custo dos especialistas
- circuit breaker por especialista quando golden score cai
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

# Permite import de _common quando rodando como módulo.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Lazy import do SDK — só carrega quando NÃO está em dry-run.
try:
    from anthropic import Anthropic
except ImportError:  # pragma: no cover
    Anthropic = None  # type: ignore


# ---------------------------------------------------------------------------
# CONSTITUIÇÃO RESUMIDA DE CADA ESPECIALISTA
# ---------------------------------------------------------------------------
# Em vez de carregar o XML completo de /prompts/<ID>/prompt.xml (que pode ter
# centenas de linhas), carregamos aqui a constituição compacta que dá ao
# especialista o que ele precisa para responder UMA query. O XML completo é
# para o pipeline de regressão; este resumo é para o despacho ao vivo.
#
# Esta separação é deliberada: o agente pedagógico foca no padrão estrela;
# o pipeline de regressão foca em eval. As duas camadas vivem em paralelo.
# ---------------------------------------------------------------------------

ESPECIALISTAS_RESUMOS = {
    "especialista_juridico_trabalhista": {
        "prompt_id": "P-LEG-01",
        "nome": "Cláusula de Não-Concorrência CLT",
        "system": (
            "Você é Advogado(a) Trabalhista sênior brasileiro. Sua função é "
            "fazer triagem inicial de cláusula de não-concorrência em contrato "
            "CLT. Você AVALIA cinco elementos jurisprudência TST: temporal "
            "(até 2 anos), geográfico (mercado relevante), material (atividade "
            "exercida), contraprestação (~30% remuneração no período), interesse "
            "legítimo do empregador. Você NUNCA emite parecer final vinculante "
            "(constituição bloqueia), apenas triagem com classe de risco "
            "(baixo/médio/alto/crítico) e recomendação de revisão por advogado "
            "responsável. NUNCA invente acórdão ou cite lei inexistente; se a "
            "memória não bate, marque 'verificar fonte primária'. Se o conteúdo "
            "for irrelevante para cláusula CLT, devolva 'fora de escopo'."
        ),
        "input_schema_description": (
            "Conteúdo bruto da cláusula ou descrição da situação trabalhista "
            "que o cliente está enfrentando."
        ),
    },
    "especialista_clinico_triagem": {
        "prompt_id": "P-MED-01",
        "nome": "Triagem clínica básica",
        "system": (
            "Você é Enfermeiro(a) sênior em triagem ambulatorial. Sua função é "
            "fazer triagem clínica preliminar a partir de queixa textual do "
            "paciente, classificando urgência em quatro tiers (azul/verde/"
            "amarelo/vermelho conforme protocolo Manchester) e recomendando "
            "próximo passo. Você NUNCA prescreve medicamento, NUNCA dá "
            "diagnóstico definitivo, NUNCA substitui consulta médica. Se a "
            "queixa sugerir emergência (vermelho), oriente busca imediata de "
            "atendimento. Se for fora de escopo (questão administrativa, "
            "agendamento, jurídico), devolva 'fora de escopo'. Em caso de "
            "incerteza, prefira escalar (suba uma cor)."
        ),
        "input_schema_description": (
            "Queixa do paciente em texto livre. Pode incluir sintomas, "
            "tempo de evolução, contexto."
        ),
    },
    "especialista_suporte_tecnico": {
        "prompt_id": "P-SUP-01",
        "nome": "Suporte técnico nível 1",
        "system": (
            "Você é Agente de Suporte Técnico sênior em SaaS B2B. Sua função é "
            "responder a ticket de suporte com (a) classificação em categoria "
            "(bug, dúvida de uso, requisição de feature, faturamento, outro), "
            "(b) urgência (baixa/média/alta/crítica), (c) primeira hipótese "
            "diagnóstica e (d) próximo passo recomendado. Você NUNCA promete "
            "prazo de correção, NUNCA garante reembolso, NUNCA acessa conta de "
            "cliente sem autorização explícita. Se a query for jurídica ou "
            "clínica, devolva 'fora de escopo'."
        ),
        "input_schema_description": (
            "Descrição do problema técnico do cliente, com contexto do ambiente "
            "e tentativas já feitas, quando disponível."
        ),
    },
}


def build_especialista_tools() -> list[dict[str, Any]]:
    """Constrói o schema de tools (uma por especialista) no formato Anthropic.

    Cada tool tem schema enxuto: input único `consulta` (string), output
    estruturado pelo próprio prompt do especialista.
    """
    tools = []
    for tool_name, meta in ESPECIALISTAS_RESUMOS.items():
        tools.append(
            {
                "name": tool_name,
                "description": (
                    f"Despacha consulta ao especialista {meta['nome']} "
                    f"(prompt {meta['prompt_id']}). Use APENAS quando o domínio "
                    f"da consulta do usuário casa com este especialista. "
                    f"Se a consulta cobre múltiplos domínios, despache para "
                    f"cada um separadamente. Se não casa com nenhum, NÃO chame "
                    f"e responda diretamente que está fora dos domínios atendidos."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "consulta": {
                            "type": "string",
                            "description": meta["input_schema_description"],
                        }
                    },
                    "required": ["consulta"],
                },
            }
        )
    return tools


def dispatch_especialista(
    name: str,
    tool_input: dict[str, Any],
    dry_run: bool = False,
    tracer: Any = None,
) -> str:
    """Executa um especialista: faz uma chamada LLM SEPARADA com o system
    prompt do especialista correspondente.

    Cada chamada aqui é uma nova sessão de modelo. O especialista NÃO vê o
    histórico do orquestrador, apenas a consulta isolada. Isso é deliberado:
    cada especialista é uma 'mente' independente, evitando contaminação de
    contexto entre domínios distintos.
    """
    meta = ESPECIALISTAS_RESUMOS.get(name)
    if meta is None:
        return f"Erro: especialista {name!r} não registrado."

    consulta = tool_input.get("consulta", "").strip()
    if not consulta:
        return "Erro: campo 'consulta' vazio."

    if dry_run:
        return (
            f"[dry-run] especialista={name} ({meta['prompt_id']}) "
            f"receberia consulta de {len(consulta)} chars. "
            f"Resposta simulada: classe=média; encaminhar para revisão humana."
        )

    if Anthropic is None:
        return "Erro: pacote 'anthropic' não instalado."

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "Erro: ANTHROPIC_API_KEY não configurada."

    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-haiku-4-5",  # Especialistas em Haiku para conter custo
        max_tokens=1024,
        system=meta["system"],
        messages=[{"role": "user", "content": consulta}],
    )

    if tracer is not None:
        tracer.log(
            event="especialista_call",
            especialista=name,
            prompt_id=meta["prompt_id"],
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            stop_reason=response.stop_reason,
        )

    # Extrai apenas blocos de texto da resposta.
    text_blocks = [b.text for b in response.content if b.type == "text"]
    return "\n".join(text_blocks)
