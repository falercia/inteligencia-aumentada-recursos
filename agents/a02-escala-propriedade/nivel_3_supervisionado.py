"""Nível 3 — SUPERVISIONADO.

Contrato F3:
- Agente pode usar TODAS as tools sem gate por ação.
- Trace é escrito em tempo real para o humano monitorar.
- Kill switch é verificado a cada iteração; humano pode interromper.

Quando usar este nível na sua organização:
- Tracing por span + replay disponíveis
- Rollback testado mensalmente
- Eval de qualidade rodando contra golden set
- Humano disponível para monitorar trace em janela paralela

Como acompanhar:
    # Em um terminal:
    tail -f ./traces/trace-*.jsonl | jq .

    # Em outro terminal:
    python nivel_3_supervisionado.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _common.anthropic_client import AnthropicClient  # noqa: E402
from _common.tracing import Tracer  # noqa: E402
from tools_simuladas import ALL_TOOLS, dispatch  # noqa: E402

# Import opcional do kill_switch deste mesmo diretório.
sys.path.insert(0, str(Path(__file__).parent))
from kill_switch import is_killed  # noqa: E402

SYSTEM_PROMPT = (
    (Path(__file__).parent / "system_prompt_base.md").read_text(encoding="utf-8")
    + "\n\n## Contrato de execução deste nível\n\n"
    "Você está operando em NÍVEL 3 (SUPERVISIONADO). Você pode usar todas "
    "as tools em sequência sem confirmação por passo. Um operador humano "
    "monitora seu trace em tempo real e pode interromper. Mantenha a mesma "
    "cautela do nível Co-piloto; a diferença operacional é a velocidade, "
    "não a permissão."
)

DEFAULT_TASK = (
    "Processe o pedido de cancelamento da Acme Industrial conforme sua "
    "constituição. Execute em sequência todas as ações necessárias. O "
    "operador humano está monitorando o trace."
)


def kill_switch_gate(name: str, tool_input: dict) -> bool:
    """Verifica o kill switch antes de cada tool. Se ativo, bloqueia tudo."""
    if is_killed():
        print(f"[KILL] kill switch ativo — bloqueando tool {name!r}")
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="A02 nível 3 — Supervisionado.")
    parser.add_argument("--task", default=DEFAULT_TASK)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="claude-sonnet-4-5")
    args = parser.parse_args()

    if is_killed():
        print(
            "[NIVEL 3] kill switch está ATIVO — agente não vai iniciar. "
            "Rode 'python kill_switch.py revive' para reativar."
        )
        return 2

    tracer = Tracer()
    print(f"[NIVEL 3 / SUPERVISIONADO] tracing em {tracer.path}")
    print(f"[NIVEL 3] tarefa: {args.task}")
    print(f"[NIVEL 3] kill switch verificado a cada tool. Para parar:")
    print(f"          python kill_switch.py kill")
    print(f"[NIVEL 3] monitorar trace em janela paralela:")
    print(f"          tail -f {tracer.path} | jq .\n")

    client = AnthropicClient(model=args.model, dry_run=args.dry_run, tracer=tracer)
    response = client.run_agent(
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": args.task}],
        tools=ALL_TOOLS,
        tool_executor=dispatch,
        on_tool_call=kill_switch_gate,
    )

    print("\n--- TOOL CALLS ---")
    for i, call in enumerate(response.tool_calls, 1):
        status = "KILLED" if call.get("blocked") else "ok"
        print(f"{i}. [{status}] {call['name']}({list(call['input'].keys())})")

    print("\n--- RESPOSTA FINAL ---")
    print(response.final_text)

    if not args.dry_run:
        summary = tracer.summary()
        print(
            f"\n--- TELEMETRIA --- iterações={response.iterations} · "
            f"tools={len(response.tool_calls)} · "
            f"latência_total_ms={summary['total_latency_ms']} · "
            f"tokens_in={response.total_input_tokens} · "
            f"tokens_out={response.total_output_tokens}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
