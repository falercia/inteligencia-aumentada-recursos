"""Gates de promoção entre níveis F3, com CLI.

Em produção: substitua o JSON local por estado em banco/feature-flag, e os
contadores fakes (simulate-day) por leitura real das métricas de operação.

Estado persistido em ./state/gates.json. Estrutura:
{
    "days_stable": 0,
    "incidents_sev_1_2": 0,
    "cost_within_envelope": true,
    "owner_approved": false,
    "rollback_tested_last_30_days": false,
    "promoted_to_level_4": false
}

Regras de promoção a Nível 4 (todas precisam ser verdadeiras):
- days_stable >= 14
- incidents_sev_1_2 == 0
- cost_within_envelope == True
- owner_approved == True
- rollback_tested_last_30_days == True
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

STATE_FILE = Path("./state/gates.json")

DEFAULT_STATE = {
    "days_stable": 0,
    "incidents_sev_1_2": 0,
    "cost_within_envelope": True,
    "owner_approved": False,
    "rollback_tested_last_30_days": False,
    "promoted_to_level_4": False,
}

DAYS_REQUIRED = 14


def _load() -> dict:
    if not STATE_FILE.exists():
        return dict(DEFAULT_STATE)
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _save(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def promotion_status() -> dict:
    """Avalia se o agente pode operar em nível 4."""
    state = _load()
    eligible = (
        state["days_stable"] >= DAYS_REQUIRED
        and state["incidents_sev_1_2"] == 0
        and state["cost_within_envelope"]
        and state["owner_approved"]
        and state["rollback_tested_last_30_days"]
    )
    state["promoted_to_level_4"] = eligible and state.get("promoted_to_level_4", False)
    return state


def cmd_status() -> int:
    state = promotion_status()
    print(json.dumps(state, ensure_ascii=False, indent=2))
    eligible = (
        state["days_stable"] >= DAYS_REQUIRED
        and state["incidents_sev_1_2"] == 0
        and state["cost_within_envelope"]
        and state["owner_approved"]
        and state["rollback_tested_last_30_days"]
    )
    print(f"\nelegível para nível 4: {eligible}")
    print(f"efetivamente promovido: {state['promoted_to_level_4']}")
    return 0


def cmd_simulate_day() -> int:
    """Simula um dia bem-sucedido de operação. Demonstração educacional."""
    state = _load()
    state["days_stable"] += 1
    _save(state)
    print(f"[gates] dia simulado. days_stable={state['days_stable']}")
    return 0


def cmd_record_incident() -> int:
    state = _load()
    state["incidents_sev_1_2"] += 1
    state["days_stable"] = 0
    state["promoted_to_level_4"] = False
    _save(state)
    print(f"[gates] incidente registrado. Contadores resetados. Nível 4 desativado.")
    return 0


def cmd_approve_owner() -> int:
    state = _load()
    state["owner_approved"] = True
    _save(state)
    print(f"[gates] aprovação nominal do dono operacional registrada.")
    return 0


def cmd_record_rollback_test() -> int:
    state = _load()
    state["rollback_tested_last_30_days"] = True
    _save(state)
    print(f"[gates] teste de rollback registrado nos últimos 30 dias.")
    return 0


def cmd_promote() -> int:
    state = promotion_status()
    eligible = (
        state["days_stable"] >= DAYS_REQUIRED
        and state["incidents_sev_1_2"] == 0
        and state["cost_within_envelope"]
        and state["owner_approved"]
        and state["rollback_tested_last_30_days"]
    )
    if not eligible:
        print(f"[gates] PROMOÇÃO RECUSADA. Faltam critérios. Veja 'status'.")
        return 1
    state["promoted_to_level_4"] = True
    _save(state)
    print(f"[gates] PROMOVIDO a nível 4. Operação autônoma autorizada.")
    return 0


def cmd_reset() -> int:
    _save(dict(DEFAULT_STATE))
    print(f"[gates] estado resetado para default.")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "uso: python gates.py {status|simulate-day|record-incident|"
            "approve-owner|record-rollback-test|promote|reset}"
        )
        return 1
    commands = {
        "status": cmd_status,
        "simulate-day": cmd_simulate_day,
        "record-incident": cmd_record_incident,
        "approve-owner": cmd_approve_owner,
        "record-rollback-test": cmd_record_rollback_test,
        "promote": cmd_promote,
        "reset": cmd_reset,
    }
    cmd = sys.argv[1]
    if cmd not in commands:
        print(f"comando desconhecido: {cmd}")
        return 1
    return commands[cmd]()


if __name__ == "__main__":
    sys.exit(main())
