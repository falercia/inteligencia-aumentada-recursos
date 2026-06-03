"""Nível 4 — AUTÔNOMO REGULADO.

Contrato F3:
- Operação SEM supervisão humana direta.
- Pré-condição: gates de promoção aprovados em gates.py.
- Kill switch verificado a cada iteração.
- Eval automatizado roda contra golden set após cada execução (stub aqui;
  em produção, dispara para /evals).
- Resultado é amostrado pelo humano em janela definida (não em tempo real).

Quando usar este nível na sua organização:
- Métrica de qualidade estável >= 14-30 dias
- Zero incidentes SEV-1 ou SEV-2 no período
- Custo composto dentro do envelope
- Aprovação nominal do dono operacional (Princípio 8)
- Plano de rollback testado no nível em questão

Rebaixamento automático:
- Qualquer incidente SEV-1/2 derruba este nível para Supervisionado (3).
- O gate de promoção precisa ser reaprovado para subir de novo.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _common.anthropic_client import AnthropicClient  # noqa: E402
from _common.tracing import Tracer  # noqa: E402
from tools_simuladas import ALL_TOOLS, dispatch  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from gates import promotion_status  # noqa: E402
from kill_switch import is_killed  # noqa: E402

SYSTEM_PROMPT = (
    (Path(__file__).parent / "system_prompt_base.md").read_text(encoding="utf-8")
    + "\n\n## Contrato de execução deste nível\n\n"
    "Você está operando em NÍVEL 4 (AUTÔNOMO REGULADO). Não há humano "
    "monitorando seu trace em tempo real. Sua execução será auditada por "
    "amostragem e por eval automatizado contra golden set. Use a mesma "
    "cautela; a diferença é o nível de instrumentação ao seu redor. Se "
    "houver QUALQUER ambiguidade na tarefa, recuse e devolva ao humano em "
    "vez de tomar decisão com confiança injustificada."
)

DEFAULT_TASK = (
    "Processe o pedido de cancelamento da Acme Industrial conforme sua "
    "constituição. Execute autonomamente."
)


def kill_gate(name: str, tool_input: dict) -> bool:
    if is_killed():
        print(f"[KILL] kill switch ativo — bloqueando tool {name!r}")
        return False
    return True


def run_eval_stub(response_text: str, tool_calls: list[dict]) -> dict:
    """Stub educacional. Em produção, dispara o eval real.

    Verifica regras heurísticas básicas:
    - Pelo menos uma chamada de tool de leitura
    - Resposta final mencionando "cancelamento" e prazo
    - Sem chamada de tool em registro de erro
    """
    issues = []
    tool_names = [c["name"] for c in tool_calls]
    if "customer_lookup" not in tool_names:
        issues.append("não chamou customer_lookup antes de agir")
    if "cancel" not in response_text.lower() and "cancelamento" not in response_text.lower():
        issues.append("resposta final não menciona o cancelamento")
    blocked = [c for c in tool_calls if c.get("blocked")]
    if blocked:
        issues.append(f"{len(blocked)} tool(s) bloqueada(s) — investigar")
    return {"passed": len(issues) == 0, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description="A02 nível 4 — Autônomo Regulado.")
    parser.add_argument("--task", default=DEFAULT_TASK)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="claude-sonnet-4-5")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignora gates de promoção (apenas para teste; proibido em produção).",
    )
    args = parser.parse_args()

    # Pré-condição 1: kill switch desativado.
    if is_killed():
        print("[NIVEL 4] kill switch ATIVO — agente não vai iniciar.")
        return 2

    # Pré-condição 2: gates de promoção aprovados.
    status = promotion_status()
    if not status["promoted_to_level_4"] and not args.force:
        print("[NIVEL 4] gates de promoção NÃO aprovados — agente não vai iniciar.")
        print(f"          estado: {status}")
        print(f"          rode 'python gates.py status' para detalhes.")
        return 3

    tracer = Tracer()
    print(f"[NIVEL 4 / AUTÔNOMO REGULADO] tracing em {tracer.path}")
    print(f"[NIVEL 4] tarefa: {args.task}")
    print(f"[NIVEL 4] sem supervisão humana em tempo real")
    print(f"[NIVEL 4] eval automatizado vai rodar após a execução\n")

    client = AnthropicClient(model=args.model, dry_run=args.dry_run, tracer=tracer)
    response = client.run_agent(
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": args.task}],
        tools=ALL_TOOLS,
        tool_executor=dispatch,
        on_tool_call=kill_gate,
    )

    print("\n--- RESPOSTA FINAL ---")
    print(response.final_text)

    if not args.dry_run:
        summary = tracer.summary()
        print(
            f"\n--- TELEMETRIA --- iterações={response.iterations} · "
            f"tools={len(response.tool_calls)} · "
            f"tokens_in={response.total_input_tokens} · "
            f"tokens_out={response.total_output_tokens}"
        )

    # Eval automatizado pós-execução.
    eval_result = run_eval_stub(response.final_text, response.tool_calls)
    print("\n--- EVAL AUTOMATIZADO ---")
    print(f"passed: {eval_result['passed']}")
    if eval_result["issues"]:
        print("issues:")
        for issue in eval_result["issues"]:
            print(f"  - {issue}")
        print("\n[NIVEL 4] rebaixando para nível 3 automaticamente.")
        # Em produção: chamar API de rebaixamento; aqui só sinalizamos.

    return 0


if __name__ == "__main__":
    sys.exit(main())
