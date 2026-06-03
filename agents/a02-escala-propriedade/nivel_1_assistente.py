"""Nível 1 — ASSISTENTE.

Contrato F3:
- Agente só pode usar tools de leitura/rascunho.
- Toda tool com escrita é bloqueada pelo wrapper.
- Resposta final é um plano que o humano executa manualmente.

Quando usar este nível na sua organização:
- Observabilidade ainda em construção (sem tracing por span)
- Reversibilidade depende de procedimento manual não testado
- Equipe não confia no agente para tomar ação irreversível
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _common.anthropic_client import AnthropicClient  # noqa: E402
from _common.tracing import Tracer  # noqa: E402
from tools_simuladas import (  # noqa: E402
    READ_ONLY_TOOLS,
    WRITE_TOOL_NAMES,
    dispatch,
)

SYSTEM_PROMPT = (
    (Path(__file__).parent / "system_prompt_base.md").read_text(encoding="utf-8")
    + "\n\n## Contrato de execução deste nível\n\n"
    "Você está operando em NÍVEL 1 (ASSISTENTE). Você NÃO pode chamar "
    "`simulate_send_email` nem `update_subscription`. Use apenas "
    "`customer_lookup` e `draft_cancellation_email`, e na sua resposta final "
    "instrua o operador humano sobre quais ações com escrita ele precisa "
    "executar e com quais parâmetros exatos."
)

DEFAULT_TASK = (
    "Processe o pedido de cancelamento da Acme Industrial conforme sua "
    "constituição. Use as tools que você tem permissão."
)


def execute_with_block(name: str, tool_input: dict) -> str:
    """Wrapper: bloqueia tools de escrita conforme contrato do nível."""
    if name in WRITE_TOOL_NAMES:
        return (
            f"BLOQUEADO. A tool {name!r} é de escrita e não está disponível "
            f"no nível Assistente. Devolva ao operador humano a instrução do "
            f"que precisa ser feito manualmente."
        )
    return dispatch(name, tool_input)


def main() -> int:
    parser = argparse.ArgumentParser(description="A02 nível 1 — Assistente.")
    parser.add_argument("--task", default=DEFAULT_TASK)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="claude-sonnet-4-5")
    args = parser.parse_args()

    tracer = Tracer()
    print(f"[NIVEL 1 / ASSISTENTE] tracing em {tracer.path}")
    print(f"[NIVEL 1] tarefa: {args.task}\n")

    client = AnthropicClient(model=args.model, dry_run=args.dry_run, tracer=tracer)
    response = client.run_agent(
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": args.task}],
        tools=READ_ONLY_TOOLS,  # apenas tools sem efeito
        tool_executor=execute_with_block,
    )

    print("--- TOOL CALLS ---")
    for i, call in enumerate(response.tool_calls, 1):
        print(f"{i}. {call['name']}({list(call['input'].keys())})")

    print("\n--- RESPOSTA FINAL (plano para o operador) ---")
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
