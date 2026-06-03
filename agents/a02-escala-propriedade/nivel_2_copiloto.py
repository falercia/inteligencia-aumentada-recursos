"""Nível 2 — CO-PILOTO.

Contrato F3:
- Agente pode usar TODAS as tools.
- Toda tool de ESCRITA exige confirmação humana síncrona no terminal.
- Tools read-only passam livres.

Quando usar este nível na sua organização:
- Tracing por span existe
- Rollback documentado, mas operação ainda é nova
- Aceita-se a fricção do gate para ganhar confiança operacional
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _common.anthropic_client import AnthropicClient  # noqa: E402
from _common.tracing import Tracer  # noqa: E402
from tools_simuladas import (  # noqa: E402
    ALL_TOOLS,
    WRITE_TOOL_NAMES,
    dispatch,
)

SYSTEM_PROMPT = (
    (Path(__file__).parent / "system_prompt_base.md").read_text(encoding="utf-8")
    + "\n\n## Contrato de execução deste nível\n\n"
    "Você está operando em NÍVEL 2 (CO-PILOTO). Você pode usar todas as "
    "tools, mas cada chamada a tool de escrita (`simulate_send_email`, "
    "`update_subscription`) exigirá aprovação humana no terminal antes da "
    "execução. Se o humano negar, ajuste sua estratégia e prossiga."
)

DEFAULT_TASK = (
    "Processe o pedido de cancelamento da Acme Industrial conforme sua "
    "constituição. Execute todas as ações necessárias; um operador humano "
    "vai aprovar cada ação com escrita."
)


def human_gate(name: str, tool_input: dict) -> bool:
    """Pede confirmação síncrona apenas para tools de escrita."""
    if name not in WRITE_TOOL_NAMES:
        return True  # passa direto

    print(f"\n[GATE] Co-piloto quer chamar tool de escrita: {name!r}")
    for k, v in tool_input.items():
        preview = str(v)[:120]
        print(f"       {k}: {preview}")
    while True:
        answer = input("       aprovar? (y/n): ").strip().lower()
        if answer in ("y", "yes", "s", "sim"):
            print("       [GATE] aprovado.")
            return True
        if answer in ("n", "no", "nao", "não"):
            print("       [GATE] bloqueado pelo humano.")
            return False
        print("       resposta inválida — use y ou n.")


def main() -> int:
    parser = argparse.ArgumentParser(description="A02 nível 2 — Co-piloto.")
    parser.add_argument("--task", default=DEFAULT_TASK)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="claude-sonnet-4-5")
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="DESLIGA o gate humano (útil para teste; em produção é proibido).",
    )
    args = parser.parse_args()

    tracer = Tracer()
    print(f"[NIVEL 2 / CO-PILOTO] tracing em {tracer.path}")
    print(f"[NIVEL 2] tarefa: {args.task}\n")
    if args.auto_approve:
        print("[NIVEL 2] aviso: gate humano desligado — modo teste.")

    client = AnthropicClient(model=args.model, dry_run=args.dry_run, tracer=tracer)

    on_tool_call = None if args.auto_approve else human_gate

    response = client.run_agent(
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": args.task}],
        tools=ALL_TOOLS,
        tool_executor=dispatch,
        on_tool_call=on_tool_call,
    )

    print("\n--- TOOL CALLS ---")
    for i, call in enumerate(response.tool_calls, 1):
        status = "BLOQUEADA" if call.get("blocked") else "ok"
        print(f"{i}. [{status}] {call['name']}({list(call['input'].keys())})")

    print("\n--- RESPOSTA FINAL ---")
    print(response.final_text)

    if not args.dry_run:
        print(
            f"\n--- TELEMETRIA --- iterações={response.iterations} · "
            f"tools={len(response.tool_calls)} · "
            f"tokens_in={response.total_input_tokens} · "
            f"tokens_out={response.total_output_tokens}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
