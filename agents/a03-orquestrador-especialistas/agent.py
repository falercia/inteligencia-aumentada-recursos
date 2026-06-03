"""A03 — Orquestrador-Especialistas.

Padrão multiagente em ESTRELA:
- 1 ORQUESTRADOR (este agente) recebe a query bruta do usuário.
- N ESPECIALISTAS (carregados de /prompts/) são tools que o orquestrador chama.
- O orquestrador classifica o domínio, despacha para o especialista certo,
  recebe a resposta e, opcionalmente, consolida em parecer único.

Decisão deliberada: cada especialista é UM PROMPT do diretório /prompts/,
carregado em runtime e injetado como tool. Isso aplica Camada Dupla ao
próprio agente — o prompt é ativo durável versionado em /prompts/<id>/;
o agente é o consumidor descartável. Mudar a versão do prompt (P-LEG-01
v1.0 → v1.1) não exige refatorar este arquivo.

Quem entendeu o A01 entende este em uma sentada: é o mesmo loop reasoning-
acting, com tools que internamente fazem outra chamada LLM.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Permite rodar como `python agent.py` de dentro do diretório do agente.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _common.anthropic_client import AnthropicClient  # noqa: E402
from _common.tracing import Tracer  # noqa: E402
from especialistas import build_especialista_tools, dispatch_especialista  # noqa: E402

SYSTEM_PROMPT = (
    Path(__file__).parent / "system_prompt_orquestrador.md"
).read_text(encoding="utf-8")

DEFAULT_TASK = (
    "Recebi um e-mail de cliente, e preciso de uma resposta inicial qualificada. "
    "Aqui vai o conteúdo bruto:\n\n"
    "\"Sou empregado de uma empresa de varejo e meu contrato tem cláusula de "
    "não-concorrência por 36 meses no Brasil inteiro, sem nenhuma "
    "contraprestação financeira. Isso é válido?\""
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "A03 Orquestrador-Especialistas — multiagente em estrela "
            "que reusa /prompts como especialistas."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python agent.py --dry-run\n"
            "  python agent.py --task '...'\n"
            "  python agent.py --task '...' --max-fan-out 1 --verbose\n"
        ),
    )
    parser.add_argument(
        "--task",
        default=DEFAULT_TASK,
        help="Query do usuário (default: caso ilustrativo CLT).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Não chama a API real; imprime o que faria.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Imprime cada despacho ao especialista e o resultado.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=6,
        help="Limite de iterações do loop do orquestrador (default: 6).",
    )
    parser.add_argument(
        "--max-fan-out",
        type=int,
        default=3,
        help=(
            "Limite de quantos especialistas o orquestrador pode chamar em uma "
            "execução (default: 3). Proteção de custo composto (F7)."
        ),
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5",
        help="Modelo do orquestrador (default: claude-sonnet-4-5).",
    )
    return parser.parse_args()


class FanOutGate:
    """Bloqueia chamadas adicionais a especialistas quando o limite é excedido.

    Decisão arquitetural: o gate é por execução, não por sessão de usuário.
    Cada `python agent.py` reseta o contador. Em produção, o contador entra em
    estado externo (Redis, banco, etc.) para sobreviver a múltiplas requisições.
    """

    def __init__(self, limit: int):
        self.limit = limit
        self.calls = 0

    def __call__(self, name: str, tool_input: dict) -> bool:
        if self.calls >= self.limit:
            print(
                f"[FAN-OUT GATE] limite de {self.limit} chamadas atingido. "
                f"Bloqueando despacho ao especialista {name!r}."
            )
            return False
        self.calls += 1
        return True


def main() -> int:
    args = parse_args()

    tracer = Tracer()
    print(f"[A03] tracing em {tracer.path}")

    client = AnthropicClient(
        model=args.model,
        dry_run=args.dry_run,
        tracer=tracer,
        max_iterations=args.max_iterations,
    )

    # Carrega os especialistas a partir de /prompts/ (P-LEG-01, P-MED-01, P-SUP-01).
    especialistas = build_especialista_tools()
    fan_out_gate = FanOutGate(args.max_fan_out)

    print(f"[A03] especialistas carregados: {[t['name'] for t in especialistas]}")
    print(f"[A03] limite de fan-out: {args.max_fan_out} despacho(s) por execução")
    print(f"[A03] tarefa do usuário:\n{'-' * 60}\n{args.task}\n{'-' * 60}\n")

    if args.dry_run:
        print("[A03] modo seco ativo — nenhuma chamada real será feita.")

    response = client.run_agent(
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": args.task}],
        tools=especialistas,
        tool_executor=lambda name, inp: dispatch_especialista(
            name, inp, dry_run=args.dry_run, tracer=tracer
        ),
        on_tool_call=fan_out_gate,
    )

    if args.verbose and response.tool_calls:
        print("\n--- DESPACHOS A ESPECIALISTAS ---")
        for i, call in enumerate(response.tool_calls, 1):
            status = "BLOQUEADO (fan-out)" if call.get("blocked") else "ok"
            print(f"{i}. [{status}] {call['name']}")
            print(f"   input: {call.get('input', {})}")
            if "output" in call:
                preview = str(call["output"])[:300]
                print(f"   → {preview}\n")

    print("\n--- PARECER FINAL DO ORQUESTRADOR ---")
    print(response.final_text)

    if not args.dry_run:
        summary = tracer.summary()
        print(
            f"\n--- TELEMETRIA --- "
            f"iterações={response.iterations} · "
            f"especialistas_chamados={fan_out_gate.calls} · "
            f"tokens_in={response.total_input_tokens} · "
            f"tokens_out={response.total_output_tokens}"
        )
        print(f"trace completo em: {summary['path']}")
        print(
            "\nObs: o trace contém também os tokens dos especialistas "
            "(cada despacho é uma chamada API separada)."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
