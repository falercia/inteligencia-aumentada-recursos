"""Kill switch testável do A03.

O kill switch é um arquivo .killed no diretório do agente. A presença
do arquivo bloqueia qualquer execução nova; sua ausência libera.

Em produção, isto vira flag em Redis ou feature flag externa, mas a mecânica
é a mesma: ler estado externo barato a cada ciclo do agente.

Uso:
    python kill_switch.py status         # mostra estado atual
    python kill_switch.py kill           # cria .killed (agente para de aceitar despacho)
    python kill_switch.py revive         # remove .killed
"""

from __future__ import annotations

import sys
from pathlib import Path

KILL_FILE = Path(__file__).parent / ".killed"


def is_killed() -> bool:
    return KILL_FILE.exists()


def kill() -> None:
    KILL_FILE.touch()
    print(f"[A03] kill switch ATIVADO: {KILL_FILE}")
    print("Toda execução nova será bloqueada até `revive`.")


def revive() -> None:
    if KILL_FILE.exists():
        KILL_FILE.unlink()
        print(f"[A03] kill switch DESATIVADO: removido {KILL_FILE}")
    else:
        print("[A03] kill switch já estava desativado.")


def status() -> None:
    if is_killed():
        print("[A03] estado: KILLED (.killed presente)")
    else:
        print("[A03] estado: ATIVO")


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
