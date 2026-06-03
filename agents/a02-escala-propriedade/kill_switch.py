"""Kill switch testável para A02 (compartilhado pelos 4 níveis).

Mesmo padrão do A01: file-flag em ./.killed local ao diretório do agente.
Em produção: feature-flag distribuída (LaunchDarkly, ConfigCat, Unleash).

Uso:
    python kill_switch.py status
    python kill_switch.py kill
    python kill_switch.py revive
    python kill_switch.py test
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

KILL_FLAG = Path(__file__).parent / ".killed"


def is_killed() -> bool:
    return KILL_FLAG.exists()


def kill() -> None:
    KILL_FLAG.touch()
    print(f"[KILL] kill switch ativado em {KILL_FLAG}")


def revive() -> None:
    if KILL_FLAG.exists():
        KILL_FLAG.unlink()
    print(f"[KILL] kill switch desativado")


def test() -> int:
    revive()
    t0 = time.time()
    kill()
    while not is_killed():
        if time.time() - t0 > 30:
            print("[TEST] FALHOU — propagação >30s")
            return 1
        time.sleep(0.1)
    elapsed = time.time() - t0
    print(f"[TEST] OK — propagação em {elapsed*1000:.1f}ms (limite: 30s)")
    revive()
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python kill_switch.py {status|kill|revive|test}")
        return 1
    cmd = sys.argv[1]
    actions = {
        "status": lambda: print(f"[KILL] estado: {'ATIVO' if is_killed() else 'inativo'}") or 0,
        "kill": lambda: kill() or 0,
        "revive": lambda: revive() or 0,
        "test": test,
    }
    if cmd not in actions:
        print(f"comando desconhecido: {cmd}")
        return 1
    result = actions[cmd]()
    return result if isinstance(result, int) else 0


if __name__ == "__main__":
    sys.exit(main())
