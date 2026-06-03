"""Kill switch testável do A04 — mesmo padrão de A01/A02/A03."""

from __future__ import annotations

import sys
from pathlib import Path

KILL_FILE = Path(__file__).parent / ".killed"


def is_killed() -> bool:
    return KILL_FILE.exists()


def kill() -> None:
    KILL_FILE.touch()
    print(f"[A04] kill switch ATIVADO: {KILL_FILE}")


def revive() -> None:
    if KILL_FILE.exists():
        KILL_FILE.unlink()
        print(f"[A04] kill switch DESATIVADO: removido {KILL_FILE}")
    else:
        print("[A04] kill switch já estava desativado.")


def status() -> None:
    if is_killed():
        print("[A04] estado: KILLED")
    else:
        print("[A04] estado: ATIVO")


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python kill_switch.py {status|kill|revive}")
        return 1
    cmd = sys.argv[1]
    if cmd == "status":
        status()
    elif cmd == "kill":
        kill()
    elif cmd == "revive":
        revive()
    else:
        print(f"comando desconhecido: {cmd}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
