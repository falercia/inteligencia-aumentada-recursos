"""Kill switch testável para A01.

Em ambiente educacional sem processo persistente, o kill switch real é Ctrl+C.
Este arquivo existe para demonstrar o padrão (declaração explícita, teste
rodável) e serve de molde para quando o agente virar serviço em produção.

Quando o A01 for promovido para serviço:
- Substitua o file-flag por feature-flag de configuração (LaunchDarkly, etc.)
- Substitua `is_killed()` por uma chamada cacheada à fonte de verdade
- Garanta que o loop principal verifique o switch a cada iteração

Como rodar este script:
    python kill_switch.py status     # mostra estado atual
    python kill_switch.py kill       # ativa o kill switch
    python kill_switch.py revive     # desativa
    python kill_switch.py test       # mede tempo até propagação (deve ser <30s)
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

KILL_FLAG = Path(__file__).parent / ".killed"


def is_killed() -> bool:
    """Verifica se o kill switch está ativo. Retorna True se o agente deve parar."""
    return KILL_FLAG.exists()


def kill() -> None:
    KILL_FLAG.touch()
    print(f"[KILL] kill switch ativado em {KILL_FLAG}")


def revive() -> None:
    if KILL_FLAG.exists():
        KILL_FLAG.unlink()
    print(f"[KILL] kill switch desativado")


def test() -> int:
    """Mede latência entre kill() e propagação para o loop. Deve ser <30s."""
    revive()
    t0 = time.time()
    kill()
    # Em produção, este sleep simula o intervalo de polling do loop.
    while not is_killed():
        if time.time() - t0 > 30:
            print("[TEST] FALHOU — kill switch não propagou em <30s")
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
    if cmd == "status":
        state = "ATIVO" if is_killed() else "inativo"
        print(f"[KILL] estado: {state}")
        return 0
    if cmd == "kill":
        kill()
        return 0
    if cmd == "revive":
        revive()
        return 0
    if cmd == "test":
        return test()
    print(f"[KILL] comando desconhecido: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
