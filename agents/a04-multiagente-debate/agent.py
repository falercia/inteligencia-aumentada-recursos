"""A04 — Multiagente Debate.

Padrão multiagente ADVERSARIAL:
- 1 PROPONENTE defende a tese A.
- 1 OPONENTE defende a tese B (contraposta a A).
- 1 JUIZ avalia ambos os argumentos contra critérios estruturados e decide.

A diferença essencial em relação ao A03 (estrela cooperativa):
- Em A03, os especialistas colaboram em domínios diferentes.
- Em A04, os agentes COMPETEM no MESMO domínio com posições opostas.
- O resultado é uma decisão melhor calibrada quando o problema admite mais
  de uma resposta razoável e a melhor escolha depende de exposição honesta
  dos trade-offs.

O juiz é AGENTE também, mas com responsabilidade de avaliar contra rubrica
explícita (carregada de eval_config.json). Em produção, o juiz pode ser
integrado ao /evals/eval_runner.py do repositório para usar judges externos
(substring, regex, classification, LLM-as-judge calibrado).

Inspiração editorial: o debate é o instrumento clássico de elicitação de
trade-off honesto. Quando o operador pede "qual a melhor opção?" o modelo
costuma escolher conforme viés do treinamento; quando o operador estrutura
"alguém defenda A, alguém ataque, e julguemos com critério", a qualidade
da decisão sobe materialmente.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _common.anthropic_client import AnthropicClient  # noqa: E402
from _common.tracing import Tracer  # noqa: E402

PROMPT_PROPONENTE = (
    Path(__file__).parent / "system_prompt_proponente.md"
).read_text(encoding="utf-8")
PROMPT_OPONENTE = (
    Path(__file__).parent / "system_prompt_oponente.md"
).read_text(encoding="utf-8")
PROMPT_JUIZ = (
    Path(__file__).parent / "system_prompt_juiz.md"
).read_text(encoding="utf-8")

EVAL_CONFIG = (
    Path(__file__).parent / "eval_config.json"
).read_text(encoding="utf-8")

DEFAULT_QUESTION = (
    "Devo adotar RAG ou fine-tuning como caminho principal para o meu "
    "assistente jurídico em um escritório de M&A com 50 advogados, base de "
    "conhecimento de 20 mil documentos atualizados quase diariamente, e "
    "exigência de citações verificáveis a fontes primárias?"
)

DEFAULT_THESIS_A = "RAG é o caminho dominante neste contexto."
DEFAULT_THESIS_B = "Fine-tuning é o caminho dominante neste contexto."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "A04 Multiagente Debate — proponente x oponente com juiz integrado a /evals."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python agent.py --dry-run\n"
            "  python agent.py --question '...' --thesis-a '...' --thesis-b '...'\n"
            "  python agent.py --rounds 2 --verbose\n"
        ),
    )
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument("--thesis-a", default=DEFAULT_THESIS_A)
    parser.add_argument("--thesis-b", default=DEFAULT_THESIS_B)
    parser.add_argument(
        "--rounds",
        type=int,
        default=1,
        help=(
            "Número de rodadas de debate antes do juiz decidir (default: 1). "
            "Cada rodada extra inclui réplica do proponente e tréplica do oponente. "
            "Custo cresce linear; ganho marginal cai rápido depois de 2 rodadas."
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5",
        help="Modelo dos três agentes (default: claude-sonnet-4-5).",
    )
    return parser.parse_args()


def run_agent_singleshot(
    client: AnthropicClient,
    system: str,
    user_message: str,
    label: str,
    verbose: bool = False,
) -> str:
    """Roda um único turno de um agente (sem tool use). Devolve só o texto."""
    response = client.run_agent(
        system=system,
        messages=[{"role": "user", "content": user_message}],
        tools=[],
        tool_executor=None,
    )
    if verbose:
        print(f"\n--- {label} ---")
        print(response.final_text)
        print(f"  (tokens in={response.total_input_tokens} out={response.total_output_tokens})")
    return response.final_text


def main() -> int:
    args = parse_args()

    tracer = Tracer()
    print(f"[A04] tracing em {tracer.path}")
    print(f"[A04] pergunta:\n{'-' * 60}\n{args.question}\n{'-' * 60}")
    print(f"[A04] tese A (proponente): {args.thesis_a}")
    print(f"[A04] tese B (oponente):   {args.thesis_b}")
    print(f"[A04] rodadas configuradas: {args.rounds}")

    client = AnthropicClient(model=args.model, dry_run=args.dry_run, tracer=tracer)

    # Histórico do debate, acumulado a cada turno.
    transcript: list[dict[str, str]] = []

    # ---------- RODADA 1 ----------
    proponente_msg = (
        f"PERGUNTA EM DEBATE:\n{args.question}\n\n"
        f"VOCÊ DEFENDE A SEGUINTE TESE:\n{args.thesis_a}\n\n"
        f"Construa seu ARGUMENTO DE ABERTURA em até 6 parágrafos, ancorado em "
        f"trade-offs verificáveis e evidência específica do contexto descrito."
    )
    abertura_a = run_agent_singleshot(
        client, PROMPT_PROPONENTE, proponente_msg,
        "ABERTURA — PROPONENTE (Tese A)", args.verbose,
    )
    transcript.append({"turno": "abertura_proponente", "texto": abertura_a})

    oponente_msg = (
        f"PERGUNTA EM DEBATE:\n{args.question}\n\n"
        f"VOCÊ DEFENDE A SEGUINTE TESE:\n{args.thesis_b}\n\n"
        f"O proponente da tese oposta já apresentou sua abertura:\n\n"
        f"---\n{abertura_a}\n---\n\n"
        f"Construa seu ARGUMENTO DE ABERTURA em até 6 parágrafos, atacando "
        f"diretamente os pontos frágeis do proponente E construindo evidência "
        f"positiva a favor da sua tese."
    )
    abertura_b = run_agent_singleshot(
        client, PROMPT_OPONENTE, oponente_msg,
        "ABERTURA — OPONENTE (Tese B)", args.verbose,
    )
    transcript.append({"turno": "abertura_oponente", "texto": abertura_b})

    # ---------- RODADAS EXTRAS (réplica e tréplica) ----------
    for r in range(2, args.rounds + 1):
        replica_msg = (
            f"PERGUNTA EM DEBATE:\n{args.question}\n\n"
            f"VOCÊ DEFENDE: {args.thesis_a}\n\n"
            f"Sua abertura foi:\n{abertura_a}\n\n"
            f"O oponente respondeu:\n{abertura_b}\n\n"
            f"Construa sua RÉPLICA da rodada {r}, em até 4 parágrafos, "
            f"focando nos contra-ataques mais fortes do oponente e em "
            f"refinamento da sua tese onde a crítica tem mérito parcial."
        )
        replica = run_agent_singleshot(
            client, PROMPT_PROPONENTE, replica_msg,
            f"RÉPLICA RODADA {r} — PROPONENTE", args.verbose,
        )
        transcript.append({"turno": f"replica_proponente_r{r}", "texto": replica})
        abertura_a = abertura_a + "\n\n[RÉPLICA R" + str(r) + "]\n" + replica

        treplica_msg = (
            f"PERGUNTA EM DEBATE:\n{args.question}\n\n"
            f"VOCÊ DEFENDE: {args.thesis_b}\n\n"
            f"Histórico do debate até agora:\n"
            f"Proponente: {abertura_a}\n\n"
            f"Sua abertura anterior: {abertura_b}\n\n"
            f"Construa sua TRÉPLICA da rodada {r}, em até 4 parágrafos."
        )
        treplica = run_agent_singleshot(
            client, PROMPT_OPONENTE, treplica_msg,
            f"TRÉPLICA RODADA {r} — OPONENTE", args.verbose,
        )
        transcript.append({"turno": f"treplica_oponente_r{r}", "texto": treplica})
        abertura_b = abertura_b + "\n\n[TRÉPLICA R" + str(r) + "]\n" + treplica

    # ---------- JUIZ ----------
    juiz_msg = (
        f"PERGUNTA SOB JULGAMENTO:\n{args.question}\n\n"
        f"TESE A (defendida pelo Proponente):\n{args.thesis_a}\n\n"
        f"ARGUMENTOS DO PROPONENTE:\n{abertura_a}\n\n"
        f"TESE B (defendida pelo Oponente):\n{args.thesis_b}\n\n"
        f"ARGUMENTOS DO OPONENTE:\n{abertura_b}\n\n"
        f"RUBRICA DE AVALIAÇÃO (eval_config):\n{EVAL_CONFIG}\n\n"
        f"Apresente seu PARECER FINAL no formato exigido pelo seu system prompt."
    )
    parecer = run_agent_singleshot(
        client, PROMPT_JUIZ, juiz_msg,
        "PARECER DO JUIZ", verbose=True,  # sempre imprimir o parecer
    )
    transcript.append({"turno": "parecer_juiz", "texto": parecer})

    # ---------- SAÍDA ESTRUTURADA ----------
    out_path = Path(__file__).parent / "outbox" / f"debate-{tracer.path.stem}.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "pergunta": args.question,
                "tese_a": args.thesis_a,
                "tese_b": args.thesis_b,
                "rounds": args.rounds,
                "transcript": transcript,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\n[A04] transcript completo gravado em {out_path}")

    if not args.dry_run:
        summary = tracer.summary()
        print(f"[A04] trace completo em: {summary['path']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
