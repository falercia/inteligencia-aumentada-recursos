"""Tool 'file_reader' — leitura sandboxed limitada a ./data/.

Por que sandboxed?
Educacional, mas o leitor que copiar isso para a empresa não deve receber por
default uma tool que lê qualquer arquivo do disco. O wrapper recusa caminhos
absolutos, caminhos com '..', e qualquer coisa fora da raiz declarada.

Em produção, troque DATA_ROOT pela raiz controlada do seu ambiente.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

DATA_ROOT = Path("./data").resolve()

FILE_READER_TOOL = {
    "name": "file_reader",
    "description": (
        "Lê um arquivo de texto da pasta ./data/. Só aceita caminhos relativos "
        "dentro de ./data/. Devolve no máximo 4000 caracteres do conteúdo. "
        "Use para consultar documentos locais que o agente precisa para a tarefa."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Caminho relativo dentro de ./data/, ex: 'contrato.txt'",
            }
        },
        "required": ["path"],
    },
}

MAX_CHARS = 4000


def execute_file_reader(tool_input: dict[str, Any]) -> str:
    if tool_input.get("_dry_run"):
        return "[dry-run] conteúdo simulado de arquivo (até 4000 caracteres)"
    raw_path = tool_input.get("path", "")
    if not raw_path:
        return "Erro: parâmetro 'path' vazio."

    candidate = (DATA_ROOT / raw_path).resolve()

    # Guarda de sandbox: o caminho resolvido deve estar dentro de DATA_ROOT.
    try:
        candidate.relative_to(DATA_ROOT)
    except ValueError:
        return f"Erro: caminho {raw_path!r} fora da sandbox ./data/."

    if not candidate.exists():
        return f"Erro: arquivo não encontrado em {raw_path!r}."
    if not candidate.is_file():
        return f"Erro: {raw_path!r} não é arquivo."

    try:
        content = candidate.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"Erro ao ler arquivo: {exc}"

    if len(content) > MAX_CHARS:
        return content[:MAX_CHARS] + f"\n\n[...truncado em {MAX_CHARS} caracteres...]"
    return content
