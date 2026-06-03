"""M01 Hello World — servidor MCP minimalista.

Demonstra os três conceitos centrais do protocolo em ~80 linhas de Python:
- Resource: notes://today (leitura)
- Tool:     create_note (ação com efeito)
- Prompt:   summarize_my_day (template)

Como rodar:
    pip install -r requirements.txt
    python server.py                 # roda em stdio aguardando cliente
    python client_test.py            # cliente de teste, em outro terminal
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Diretórios locais — sandboxed; nada escreve fora daqui.
NOTES_DIR = Path("./notes")
TRACES_DIR = Path("./traces")
NOTES_DIR.mkdir(exist_ok=True)
TRACES_DIR.mkdir(exist_ok=True)

TRACE_FILE = TRACES_DIR / f"mcp-m01-{time.strftime('%Y%m%d-%H%M%S')}.jsonl"


def _trace(event: str, **payload) -> None:
    """Auditoria local: cada chamada vira uma linha JSON."""
    record = {"ts": time.time(), "event": event, **payload}
    with TRACE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


# Inicialização do servidor. O nome é o que aparece no cliente.
mcp = FastMCP("hello-world-notes")


# --------------------------------------------------------------------
# RESOURCE — algo que o cliente LÊ. Sem efeito. URI identifica.
# --------------------------------------------------------------------
@mcp.resource("notes://today")
def get_today_note() -> str:
    """Retorna a nota do dia atual. Se não existir, devolve mensagem default.

    Resource é leitura pura. Equivalente conceitual ao GET em REST. O cliente
    pode incluir o conteúdo no contexto da conversa sem precisar pedir
    autorização — é só dado.
    """
    today = time.strftime("%Y-%m-%d")
    note_path = NOTES_DIR / f"{today}.md"
    _trace("resource_read", uri="notes://today", path=str(note_path))
    if not note_path.exists():
        return f"# Nota de {today}\n\n(Nenhuma nota criada ainda hoje.)"
    return note_path.read_text(encoding="utf-8")


# --------------------------------------------------------------------
# TOOL — algo que o cliente EXECUTA. Tem efeito. Nome identifica.
# Permissão declarada: escreve em ./notes/{data}.md. Não escreve fora.
# --------------------------------------------------------------------
@mcp.tool()
def create_note(text: str) -> str:
    """Anexa uma nova entrada à nota do dia atual.

    SCOPE: escrita restrita ao diretório ./notes/, no arquivo {YYYY-MM-DD}.md.
    EFFECT: cria arquivo se não existir; senão, anexa ao fim.
    REVERSIBLE: sim, basta apagar o arquivo ou editar manualmente.

    Args:
        text: conteúdo da entrada (sem formatação especial).

    Returns:
        Confirmação com o path do arquivo escrito.
    """
    today = time.strftime("%Y-%m-%d")
    note_path = NOTES_DIR / f"{today}.md"
    timestamp = time.strftime("%H:%M:%S")
    entry = f"\n- **{timestamp}** — {text}\n"
    if not note_path.exists():
        note_path.write_text(f"# Nota de {today}\n{entry}", encoding="utf-8")
    else:
        with note_path.open("a", encoding="utf-8") as f:
            f.write(entry)
    _trace("tool_call", name="create_note", path=str(note_path), text_preview=text[:80])
    return f"Entrada adicionada em {note_path}"


# --------------------------------------------------------------------
# PROMPT — template REUTILIZÁVEL que o servidor SUGERE ao cliente.
# Não existe em REST. É a contribuição original do MCP: padronizar a
# forma como o cliente conversa com o servidor.
# --------------------------------------------------------------------
@mcp.prompt()
def summarize_my_day() -> str:
    """Template que o cliente usa para pedir resumo executivo do dia.

    Carrega a nota do dia e devolve um prompt formatado, pronto para o
    cliente enviar ao modelo. Quem padronizar prompts dessa forma evita
    que cada usuário invente o seu, ganhando consistência de output.
    """
    today_note = get_today_note()
    return (
        "Leia a nota abaixo e produza um resumo executivo em três frases, "
        "destacando: (1) decisões tomadas, (2) ações pendentes, (3) bloqueios.\n\n"
        f"---\n{today_note}\n---"
    )


# --------------------------------------------------------------------
# Entry point: roda em stdio, padrão para Claude Desktop e clientes locais.
# --------------------------------------------------------------------
if __name__ == "__main__":
    _trace("server_start", server="hello-world-notes")
    mcp.run()
