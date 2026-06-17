#!/usr/bin/env python3
"""
extract-prompts.py
====================================================================
Extrai os 30 prompts profissionais do APX-L (Apêndice L do Livro 1
Inteligência Aumentada) e popula a estrutura do repositório
inteligencia-aumentada-recursos, gerando:

  prompts/P-XXX-NN-slug/
    ├── README.md         ← ficha conceitual + metadados
    ├── prompt.xml        ← XML completo
    ├── golden-set.yaml   ← 20 casos
    └── anti-padroes.md   ← antipadrões observados

Execução (a partir da raiz do repositório clonado):

    python3 /caminho/para/extract-prompts.py

Sem argumentos. O script assume o caminho do APX-L hardcoded.
Ajuste a constante APX_L_PATH se necessário.
====================================================================
"""

import os
import re
import sys
from pathlib import Path

# ====================================================================
# CONFIGURAÇÃO
# ====================================================================

# Caminho do APX-L (fonte dos prompts no manuscrito). Resolvido nesta ordem:
#   1. variável de ambiente APX_L_PATH
#   2. 1º argumento de linha de comando
#   3. default abaixo (máquina do autor) — ferramenta de autor, não portável
import os
_DEFAULT_APX_L = (
    "/Users/fabiogarcia/Documents/Personal/Livros/Ebook IA/"
    "Livro-1-Os-Invariantes/04-apendices/L1-APX-L-biblioteca-prompts.md"
)
APX_L_PATH = Path(
    os.environ.get("APX_L_PATH")
    or (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else _DEFAULT_APX_L)
)

REPO_ROOT = Path.cwd()  # assume execução dentro do repo clonado
PROMPTS_DIR = REPO_ROOT / "prompts"

# Mapa de ID curto -> slug do diretório
PROMPT_SLUGS = {
    "P-LEG-01": "P-LEG-01-clausula-nao-concorrencia-clt",
    "P-LEG-02": "P-LEG-02-nda-lgpd-compliant",
    "P-LEG-03": "P-LEG-03-red-flags-contrato-ma",
    "P-LEG-04": "P-LEG-04-parecer-compliance-lgpd",
    "P-MED-01": "P-MED-01-triagem-sintomas",
    "P-MED-02": "P-MED-02-sumula-prontuario",
    "P-MED-03": "P-MED-03-interacao-medicamentosa",
    "P-FIN-01": "P-FIN-01-anomalia-extrato",
    "P-FIN-02": "P-FIN-02-risco-credito-pf",
    "P-FIN-03": "P-FIN-03-sumula-itr",
    "P-FIN-04": "P-FIN-04-analise-carteira",
    "P-SAAS-01": "P-SAAS-01-feature-request",
    "P-SAAS-02": "P-SAAS-02-sumula-nps",
    "P-SAAS-03": "P-SAAS-03-release-notes",
    "P-SAAS-04": "P-SAAS-04-churn-signal",
    "P-SUP-01": "P-SUP-01-severidade-ticket",
    "P-SUP-02": "P-SUP-02-resposta-empatica",
    "P-SUP-03": "P-SUP-03-escalonamento",
    "P-RH-01": "P-RH-01-triagem-curriculo",
    "P-RH-02": "P-RH-02-feedback-360",
    "P-RH-03": "P-RH-03-descritivo-vaga",
    "P-MKT-01": "P-MKT-01-copy-ab",
    "P-MKT-02": "P-MKT-02-brand-voice",
    "P-MKT-03": "P-MKT-03-sumula-pesquisa",
    "P-EDU-01": "P-EDU-01-plano-aula",
    "P-EDU-02": "P-EDU-02-avaliacao-rubrica",
    "P-EDU-03": "P-EDU-03-resposta-socratica",
    "P-TR-01": "P-TR-01-extracao-json",
    "P-TR-02": "P-TR-02-multi-label",
    "P-TR-03": "P-TR-03-recusa-fallback",
}

# ====================================================================
# PARSER
# ====================================================================

def parse_apx_l(content: str) -> list[dict]:
    """
    Quebra o conteúdo do APX-L em blocos por prompt e extrai os campos
    relevantes de cada um.
    """
    # Cada prompt canônico começa com "### P-XXX-NN — ..."
    # O changelog usa "#### P-XXX-NN" (quatro hashes), então não casa.
    pattern = re.compile(r'^### (P-[A-Z]+-\d+)\s+—\s+(.+?)$', re.MULTILINE)
    matches = list(pattern.finditer(content))

    prompts = []
    for i, m in enumerate(matches):
        pid = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else None
        body = content[start:end] if end else content[start:]

        prompts.append(parse_prompt_block(pid, title, body))

    return prompts


def parse_prompt_block(pid: str, title: str, body: str) -> dict:
    """
    Extrai os campos de um bloco de prompt do APX-L.
    """
    # Metadados (Domínio, Caso de uso, Modelo recomendado)
    domain = extract_field(body, r'\*\*Domínio:\*\*\s*(.+?)$')
    use_case = extract_field(body, r'\*\*Caso de uso:\*\*\s*(.+?)$')
    model = extract_field(body, r'\*\*Modelo recomendado:\*\*\s*(.+?)$')

    # Bloco XML (entre ```xml e ```)
    xml_match = re.search(r'```xml\s*\n(.*?)\n```', body, re.DOTALL)
    xml_content = xml_match.group(1).strip() if xml_match else ""

    # Golden set (sob "#### Golden set", até próximo "####")
    golden = extract_section(body, "#### Golden set", "####")

    # Anti-padrões observados
    antipatterns = extract_section(body, "#### Anti-padrões observados", "####")

    # Métrica de qualidade
    metric = extract_section(body, "#### Métrica de qualidade", "---")

    return {
        "id": pid,
        "title": title,
        "domain": domain,
        "use_case": use_case,
        "model": model,
        "xml": xml_content,
        "golden_set": golden.strip(),
        "antipatterns": antipatterns.strip(),
        "metric": metric.strip(),
    }


def extract_field(body: str, pattern: str) -> str:
    m = re.search(pattern, body, re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_section(body: str, start_marker: str, end_marker: str) -> str:
    """
    Extrai o conteúdo entre um marcador inicial e o próximo marcador
    (de mesmo nível ou superior).
    """
    start = body.find(start_marker)
    if start == -1:
        return ""
    start += len(start_marker)
    end = body.find(end_marker, start)
    if end == -1:
        return body[start:].strip()
    return body[start:end].strip()


# ====================================================================
# GERADORES DE ARQUIVO
# ====================================================================

def write_prompt_xml(prompt_dir: Path, prompt: dict) -> None:
    """
    Salva o XML completo do prompt em prompt.xml.
    """
    (prompt_dir / "prompt.xml").write_text(prompt["xml"] + "\n", encoding="utf-8")


def write_golden_yaml(prompt_dir: Path, prompt: dict) -> None:
    """
    Converte o golden set markdown em YAML estruturado.
    """
    yaml_content = (
        f"# Golden set — {prompt['id']}\n"
        f"# {prompt['title']}\n"
        f"# Domínio: {prompt['domain']}\n"
        f"#\n"
        f"# 20 casos categorizados em fáceis (1-8), médios (9-15)\n"
        f"# e difíceis / limítrofes (16-20).\n"
        f"#\n"
        f"# Para usar em eval_runner.py: cada caso vira um par\n"
        f"# (input, saída_esperada). A descrição combina ambos.\n"
        f"\n"
        f"prompt_id: {prompt['id']}\n"
        f"prompt_title: \"{escape_yaml(prompt['title'])}\"\n"
        f"version: 1.0.0\n"
        f"language: pt-BR\n"
        f"\n"
        f"casos:\n"
    )

    # Parse dos casos numerados
    lines = prompt["golden_set"].split("\n")
    current_category = "facil"
    case_num = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detectar categoria
        if "Fáceis" in line:
            current_category = "facil"
            continue
        if "Médios" in line:
            current_category = "medio"
            continue
        if "Difíceis" in line or "limítrofes" in line:
            current_category = "limitrofe"
            continue

        # Detectar caso numerado
        m = re.match(r'^(\d+)\.\s+(.+)', line)
        if m:
            case_num = int(m.group(1))
            description = m.group(2).strip()
            yaml_content += (
                f"  - numero: {case_num}\n"
                f"    categoria: {current_category}\n"
                f"    descricao: |\n"
                f"      {escape_yaml(description)}\n"
            )

    yaml_content += (
        f"\n"
        f"# Total: {case_num} casos\n"
        f"# Última revisão: 2026-06-XX\n"
    )

    (prompt_dir / "golden-set.yaml").write_text(yaml_content, encoding="utf-8")


def write_antipatterns_md(prompt_dir: Path, prompt: dict) -> None:
    md = (
        f"# Anti-padrões observados — {prompt['id']}\n\n"
        f"## {prompt['title']}\n\n"
        f"Comportamentos do modelo que comprometem a qualidade da saída.\n"
        f"Cada anti-padrão foi observado em uso real ou em teste contra o\n"
        f"golden set, e deve ser mitigado pela constituição, pelo prefill,\n"
        f"pelo self-critique, ou pela combinação dos três.\n\n"
        f"---\n\n"
        f"{prompt['antipatterns']}\n\n"
        f"---\n\n"
        f"## Métrica de qualidade\n\n"
        f"{prompt['metric']}\n"
    )
    (prompt_dir / "anti-padroes.md").write_text(md, encoding="utf-8")


def write_prompt_readme(prompt_dir: Path, prompt: dict) -> None:
    """
    Gera o README de cada prompt com a ficha conceitual.
    """
    readme = (
        f"# {prompt['id']} · {prompt['title']}\n\n"
        f"**Domínio:** {prompt['domain']}\n"
        f"**Caso de uso:** {prompt['use_case']}\n"
        f"**Modelo recomendado:** {prompt['model']}\n\n"
        f"---\n\n"
        f"## Estrutura\n\n"
        f"```\n"
        f"{prompt_dir.name}/\n"
        f"├── README.md          ← este arquivo\n"
        f"├── prompt.xml         ← XML completo (persona, constituição,\n"
        f"│                       contexto, tarefa, formato, prefill,\n"
        f"│                       self_critique, input)\n"
        f"├── golden-set.yaml    ← 20 casos categorizados\n"
        f"├── anti-padroes.md    ← antipadrões + métrica\n"
        f"├── changelog.md       ← histórico de versões\n"
        f"└── exemplos-saida/    ← outputs reais anonimizados\n"
        f"```\n\n"
        f"## Como usar\n\n"
        f"1. Copie esta pasta inteira para o seu repositório.\n"
        f"2. Adapte a constituição em `prompt.xml` ao seu contexto.\n"
        f"3. Construa seu golden set próprio com pelo menos 20 casos do\n"
        f"   seu tráfego real, usando `golden-set.yaml` como template.\n"
        f"4. Rode `eval_runner.py` (release v1.1.0+) antes de cada release.\n\n"
        f"## Conexão com a obra\n\n"
        f"A ficha conceitual completa, com analogia, anti-padrões\n"
        f"detalhados e exemplos de aplicação, está no **APX-L · Biblioteca\n"
        f"de Prompts Profissionais** do livro Inteligência Aumentada · Os\n"
        f"Invariantes da IA.\n\n"
        f"## Licença\n\n"
        f"- `prompt.xml`, `golden-set.yaml`, `anti-padroes.md`,\n"
        f"  `changelog.md`: CC-BY 4.0\n"
        f"- Atribuição obrigatória a Fabio Garcia / Inteligência Aumentada.\n"
    )
    (prompt_dir / "README.md").write_text(readme, encoding="utf-8")


def escape_yaml(text: str) -> str:
    return text.replace('"', '\\"')


# ====================================================================
# MAIN
# ====================================================================

def main() -> int:
    print("═══════════════════════════════════════════════════════════════")
    print("  extract-prompts.py · Inteligência Aumentada · Recursos")
    print("═══════════════════════════════════════════════════════════════")
    print()

    if not APX_L_PATH.exists():
        print(f"✗ Arquivo APX-L não encontrado em:\n  {APX_L_PATH}")
        return 1

    if not PROMPTS_DIR.exists():
        print(f"✗ Pasta prompts/ não encontrada em {PROMPTS_DIR}")
        print("  Você executou setup-local.sh primeiro?")
        return 1

    print(f"▸ Lendo APX-L: {APX_L_PATH.name}")
    content = APX_L_PATH.read_text(encoding="utf-8")

    print("▸ Parseando blocos de prompts...")
    prompts = parse_apx_l(content)
    print(f"  Encontrados: {len(prompts)} prompts canônicos")

    if len(prompts) != 30:
        print(f"⚠ Aviso: esperado 30 prompts, encontrado {len(prompts)}")

    print()
    print("▸ Populando pastas de cada prompt:")
    for prompt in prompts:
        pid = prompt["id"]
        slug = PROMPT_SLUGS.get(pid)
        if not slug:
            print(f"  ✗ {pid}: slug não mapeado, pulando")
            continue

        prompt_dir = PROMPTS_DIR / slug
        if not prompt_dir.exists():
            print(f"  ✗ {pid}: pasta {prompt_dir} não existe, pulando")
            continue

        write_prompt_xml(prompt_dir, prompt)
        write_golden_yaml(prompt_dir, prompt)
        write_antipatterns_md(prompt_dir, prompt)
        write_prompt_readme(prompt_dir, prompt)
        print(f"  ✓ {pid} → {slug}")

    print()
    print("═══════════════════════════════════════════════════════════════")
    print("✅ Extração concluída.")
    print("═══════════════════════════════════════════════════════════════")
    print()
    print("Próximos passos:")
    print("1. cp /caminho/para/README.md .")
    print("2. git add .")
    print('3. git commit -m "v1.0.0 — biblioteca completa com 30 prompts"')
    print("4. git tag v1.0.0")
    print("5. git push origin main && git push origin v1.0.0")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
