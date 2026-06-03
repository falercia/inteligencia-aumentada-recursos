"""M02 Biblioteca Interna — servidor MCP que expõe prompts e governança.

Lê dois diretórios do repositório:
- prompts/        → cada subdiretório vira um Resource (manifest YAML/MD)
- governance/v1/  → cada arquivo .md vira um Resource

Tools para descoberta:
- list_prompts(domain)  → filtra por domínio (juridico, medico, suporte, ...)
- search_governance(term) → busca textual nos arquivos de governança

Prompt:
- apply_prompt_to_task → template que carrega um prompt e o aplica a uma tarefa

Como rodar:
    export REPO_ROOT="/caminho/absoluto/do/repo"
    pip install -r requirements.txt
    python server.py
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# --------------------------------------------------------------------
# Setup: raiz do repo, sandbox de leitura, tracing.
# --------------------------------------------------------------------
REPO_ROOT_ENV = os.getenv("REPO_ROOT")
if REPO_ROOT_ENV:
    REPO_ROOT = Path(REPO_ROOT_ENV).resolve()
else:
    # Fallback: assume que estamos rodando dentro do próprio repo.
    REPO_ROOT = Path(__file__).resolve().parents[2]

PROMPTS_DIR = (REPO_ROOT / "prompts").resolve()
GOVERNANCE_DIR = (REPO_ROOT / "governance" / "v1").resolve()
TRACES_DIR = Path("./traces")
TRACES_DIR.mkdir(exist_ok=True)
TRACE_FILE = TRACES_DIR / f"mcp-m02-{time.strftime('%Y%m%d-%H%M%S')}.jsonl"


def _trace(event: str, **payload) -> None:
    record = {"ts": time.time(), "event": event, **payload}
    with TRACE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def _within(base: Path, candidate: Path) -> bool:
    """Validação de sandbox: candidate precisa estar dentro de base."""
    try:
        candidate.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


mcp = FastMCP("biblioteca-interna")


# --------------------------------------------------------------------
# Descoberta dinâmica: lê os diretórios e cria os Resources.
# --------------------------------------------------------------------
def _discover_prompts() -> dict[str, Path]:
    """Devolve mapa {P-CODE: path-do-manifest} para cada prompt em /prompts."""
    out: dict[str, Path] = {}
    if not PROMPTS_DIR.exists():
        return out
    for entry in sorted(PROMPTS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        # Aceita manifest em .yaml/.yml/.md/.json — o que existir primeiro vence.
        for candidate_name in ("manifest.yaml", "manifest.yml", "README.md", "prompt.md"):
            manifest = entry / candidate_name
            if manifest.exists():
                out[entry.name] = manifest
                break
    return out


def _discover_governance() -> dict[str, Path]:
    """Devolve mapa {slug: path} para cada arquivo .md em /governance/v1/."""
    out: dict[str, Path] = {}
    if not GOVERNANCE_DIR.exists():
        return out
    for entry in sorted(GOVERNANCE_DIR.glob("*.md")):
        slug = entry.stem.lower().replace("_", "-")
        out[slug] = entry
    return out


# --------------------------------------------------------------------
# RESOURCES dinâmicos — uma URI por arquivo descoberto.
# Usamos templates de URI: prompt://{code}/manifest e governance://{slug}
# --------------------------------------------------------------------
@mcp.resource("prompt://{code}/manifest")
def get_prompt_manifest(code: str) -> str:
    """Retorna o manifesto de um prompt profissional da biblioteca.

    code: identificador do prompt (ex.: 'P-LEG-01').
    """
    prompts = _discover_prompts()
    path = prompts.get(code)
    if path is None:
        _trace("resource_miss", uri=f"prompt://{code}/manifest")
        return f"Prompt {code!r} não encontrado. Use list_prompts() para ver disponíveis."
    if not _within(PROMPTS_DIR, path):
        _trace("sandbox_violation", uri=f"prompt://{code}/manifest", path=str(path))
        return "Erro: path fora da sandbox."
    _trace("resource_read", uri=f"prompt://{code}/manifest", path=str(path))
    return path.read_text(encoding="utf-8")


@mcp.resource("governance://{slug}")
def get_governance_section(slug: str) -> str:
    """Retorna uma seção do caderno de governança v1.

    slug: identificador da seção (ex.: 'accountability-raci').
    """
    governance = _discover_governance()
    path = governance.get(slug.lower())
    if path is None:
        _trace("resource_miss", uri=f"governance://{slug}")
        available = ", ".join(sorted(governance.keys())[:10])
        return (
            f"Seção {slug!r} não encontrada. "
            f"Use search_governance() para buscar. "
            f"Algumas disponíveis: {available}"
        )
    if not _within(GOVERNANCE_DIR, path):
        _trace("sandbox_violation", uri=f"governance://{slug}", path=str(path))
        return "Erro: path fora da sandbox."
    _trace("resource_read", uri=f"governance://{slug}", path=str(path))
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------
# TOOLS — descoberta e busca.
# --------------------------------------------------------------------
@mcp.tool()
def list_prompts(domain: str | None = None) -> str:
    """Lista todos os prompts profissionais disponíveis, opcionalmente filtrando por domínio.

    SCOPE: leitura pura, sem efeito.

    Args:
        domain: filtro por prefixo de domínio. Use 'juridico', 'medico', 'suporte',
                'financeiro', 'saas', 'rh', 'marketing', 'educacao', ou None para todos.

    Returns:
        Lista textual com código, domínio e título de cada prompt.
    """
    prompts = _discover_prompts()
    domain_prefix = {
        "juridico": "P-LEG",
        "medico": "P-MED",
        "suporte": "P-SUP",
        "financeiro": "P-FIN",
        "saas": "P-SAA",
        "rh": "P-RH",
        "marketing": "P-MKT",
        "educacao": "P-EDU",
    }.get((domain or "").lower())

    items = []
    for code, path in prompts.items():
        if domain_prefix and not code.startswith(domain_prefix):
            continue
        # Tenta extrair título da primeira linha h1/h2 do manifest.
        try:
            first_lines = path.read_text(encoding="utf-8").splitlines()[:5]
            title = next(
                (l.lstrip("# ").strip() for l in first_lines if l.startswith("#")),
                code,
            )
        except OSError:
            title = code
        items.append(f"- **{code}** — {title}")

    _trace("tool_call", name="list_prompts", domain=domain, results=len(items))

    if not items:
        return f"Nenhum prompt encontrado para domínio {domain!r}."
    return f"## Prompts disponíveis ({len(items)})\n\n" + "\n".join(items)


@mcp.tool()
def search_governance(term: str) -> str:
    """Busca textual nos arquivos do caderno de governança v1.

    SCOPE: leitura pura, sem efeito.

    Args:
        term: termo a buscar (case-insensitive). Mínimo 3 caracteres.

    Returns:
        Lista textual com seções que contêm o termo, e trecho de contexto.
    """
    if len(term) < 3:
        return "Erro: termo deve ter pelo menos 3 caracteres."

    governance = _discover_governance()
    term_lower = term.lower()
    hits = []
    for slug, path in governance.items():
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if term_lower not in content.lower():
            continue
        # Trecho de 200 caracteres ao redor da primeira ocorrência.
        idx = content.lower().find(term_lower)
        start = max(0, idx - 80)
        end = min(len(content), idx + 120)
        snippet = content[start:end].replace("\n", " ").strip()
        hits.append(f"- **governance://{slug}** — ...{snippet}...")

    _trace("tool_call", name="search_governance", term=term, results=len(hits))

    if not hits:
        return f"Nenhuma seção encontrada para o termo {term!r}."
    return f"## Seções encontradas ({len(hits)})\n\n" + "\n".join(hits)


# --------------------------------------------------------------------
# PROMPT — template para aplicar um prompt da biblioteca a uma tarefa.
# --------------------------------------------------------------------
@mcp.prompt()
def apply_prompt_to_task(prompt_code: str, task: str) -> str:
    """Template que carrega um prompt da biblioteca e o aplica a uma tarefa específica.

    Args:
        prompt_code: código do prompt na biblioteca (ex.: 'P-LEG-01').
        task: descrição da tarefa a executar usando esse prompt.
    """
    manifest = get_prompt_manifest(prompt_code)
    return (
        f"Você vai operar conforme a constituição do prompt **{prompt_code}** "
        f"da biblioteca profissional, reproduzida abaixo entre delimitadores. "
        f"Aplique essa constituição à tarefa indicada após o segundo delimitador, "
        f"preservando rigorosamente o formato de saída especificado.\n\n"
        f"--- CONSTITUIÇÃO {prompt_code} ---\n"
        f"{manifest}\n"
        f"--- TAREFA ---\n"
        f"{task}"
    )


# --------------------------------------------------------------------
# Entry point: stdio.
# --------------------------------------------------------------------
if __name__ == "__main__":
    _trace(
        "server_start",
        server="biblioteca-interna",
        prompts_dir=str(PROMPTS_DIR),
        governance_dir=str(GOVERNANCE_DIR),
        prompts_found=len(_discover_prompts()),
        governance_found=len(_discover_governance()),
    )
    mcp.run()
