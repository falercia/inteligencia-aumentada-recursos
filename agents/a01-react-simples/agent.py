"""A01 — ReAct Simples.

Entry point do agente. Lê argumentos de linha de comando, monta tools,
carrega o system prompt do arquivo .md adjacente, chama o cliente
compartilhado e imprime o resultado.

Filosofia: este arquivo é deliberadamente curto. Toda a mecânica interessante
está em ../_common/anthropic_client.py. Quem entendeu o cliente, entende este
agente em cinco minutos.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Permite rodar como `python agent.py` de dentro do diretório do agente.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _common.anthropic_client import AnthropicClient  # noqa: E402
from _common.tools.calculator import (  # noqa: E402
    CALCULATOR_TOOL,
    execute_calculator,
)
from _common.tools.fake_web_search import (  # noqa: E402
    WEB_SEARCH_TOOL,
    execute_web_search,
)
from _common.tools.file_reader import (  # noqa: E402
    FILE_READER_TOOL,
    execute_file_reader,
)
from _common.tracing import Tracer  # noqa: E402

# Registry: nome da tool → função executora.
TOOL_REGISTRY = {
    "calculator": execute_calculator,
    "file_reader": execute_file_reader,
    "fake_web_search": execute_web_search,
}

TOOLS = [CALCULATOR_TOOL, FILE_READER_TOOL, WEB_SEARCH_TOOL]

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text(encoding="utf-8")


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatcher: chama a função certa do registry."""
    executor = TOOL_REGISTRY.get(name)
    if executor is None:
        return f"Erro: tool desconhecida {name!r}."
    return executor(tool_input)


def human_gate(name: str, tool_input: dict) -> bool:
    """Gate humano síncrono no terminal. Devolve True se aprovado, False se bloqueado.

    Em produção, este gate vira API com aprovação assíncrona, slack-bot,
    fila de revisão, etc. Aqui é input() para o leitor sentir a fricção
    de aprovar cada ação.
    """
    print(f"\n[GATE] Agente quer chamar tool {name!r}")
    print(f"       com input: {tool_input}")
    while True:
        answer = input("       aprovar? (y/n): ").strip().lower()
        if answer in ("y", "yes", "s", "sim"):
            return True
        if answer in ("n", "no", "nao", "não"):
            print("       [GATE] bloqueado pelo humano.")
            return False
        print("       resposta inválida — use y ou n.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="A01 ReAct Simples — agente educacional com loop reasoning+acting.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python agent.py --dry-run --task 'Calcule 18%% de 12450'\n"
            "  python agent.py --task 'Pesquise sobre LGPD'\n"
            "  python agent.py --task '...' --gate --verbose\n"
        ),
    )
    parser.add_argument(
        "--task",
        required=True,
        help="Tarefa para o agente resolver (em linguagem natural).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Não chama a API; imprime o que faria.",
    )
    parser.add_argument(
        "--gate",
        action="store_true",
        help="Pede confirmação humana antes de cada chamada de tool.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Imprime cada chamada de tool e o resultado.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=8,
        help="Limite de iterações do loop (default: 8). Kill switch suave.",
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5",
        help="Modelo a usar (default: claude-sonnet-4-5).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    tracer = Tracer()
    print(f"[A01] tracing em {tracer.path}")

    client = AnthropicClient(
        model=args.model,
        dry_run=args.dry_run,
        tracer=tracer,
        max_iterations=args.max_iterations,
    )

    on_tool_call = human_gate if args.gate else None

    print(f"[A01] tarefa: {args.task}")
    if args.dry_run:
        print("[A01] modo seco ativo — nenhuma chamada real será feita.")
    if args.gate:
        print("[A01] gate humano ativo — toda tool exigirá aprovação no terminal.")

    response = client.run_agent(
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": args.task}],
        tools=TOOLS,
        tool_executor=execute_tool,
        on_tool_call=on_tool_call,
    )

    if args.verbose and response.tool_calls:
        print("\n--- TOOL CALLS ---")
        for i, call in enumerate(response.tool_calls, 1):
            print(f"{i}. {call['name']}({call['input']})")
            if "output" in call:
                preview = str(call["output"])[:200]
                print(f"   → {preview}")
            elif call.get("blocked"):
                print("   → bloqueado pelo gate humano")

    print("\n--- RESPOSTA FINAL ---")
    print(response.final_text)

    if not args.dry_run:
        summary = tracer.summary()
        print(
            f"\n--- TELEMETRIA --- "
            f"iterações={response.iterations} · "
            f"tools_chamadas={len(response.tool_calls)} · "
            f"tokens_in={response.total_input_tokens} · "
            f"tokens_out={response.total_output_tokens}"
        )
        print(f"trace completo em: {summary['path']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
