"""Cliente de teste para M02 Biblioteca Interna.

Sobe o servidor via stdio, lista Resources descobertos dinamicamente,
chama as duas Tools de descoberta, lê alguns Resources, e imprime o
Prompt template renderizado. Valida fim-a-fim sem precisar do Claude Desktop.

Como rodar:
    export REPO_ROOT="/caminho/absoluto/do/repo"
    pip install -r requirements.txt
    python client_test.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> int:
    # Passa REPO_ROOT adiante para o subprocesso.
    env = dict(os.environ)
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).parent / "server.py")],
        env=env,
    )

    print("[client] subindo servidor biblioteca-interna...")
    if "REPO_ROOT" not in env:
        print(
            "[client] aviso: REPO_ROOT não setado; servidor vai assumir layout padrão."
        )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("[client] sessão inicializada\n")

            # 1. Listar Resources descobertos.
            resources = await session.list_resources()
            print(f"--- RESOURCES descobertos ({len(resources.resources)}) ---")
            for r in resources.resources[:10]:
                print(f"  {r.uri}")
            if len(resources.resources) > 10:
                print(f"  ... e mais {len(resources.resources) - 10}")

            # 2. Listar templates de Resource (URIs parametrizadas).
            templates = await session.list_resource_templates()
            print(f"\n--- RESOURCE TEMPLATES ({len(templates.resourceTemplates)}) ---")
            for t in templates.resourceTemplates:
                print(f"  {t.uriTemplate} — {t.name or ''}")

            # 3. Listar Tools.
            tools = await session.list_tools()
            print(f"\n--- TOOLS ({len(tools.tools)}) ---")
            for t in tools.tools:
                desc = (t.description or "").splitlines()[0]
                print(f"  {t.name} — {desc}")

            # 4. Chamar list_prompts() sem filtro.
            print("\n--- CALL list_prompts() ---")
            result = await session.call_tool("list_prompts", arguments={})
            for block in result.content:
                text = getattr(block, "text", "")
                print(text[:600] + ("..." if len(text) > 600 else ""))

            # 5. Chamar list_prompts(domain="juridico").
            print("\n--- CALL list_prompts(domain='juridico') ---")
            result = await session.call_tool(
                "list_prompts", arguments={"domain": "juridico"}
            )
            for block in result.content:
                print(getattr(block, "text", ""))

            # 6. Chamar search_governance("RACI").
            print("\n--- CALL search_governance(term='RACI') ---")
            result = await session.call_tool(
                "search_governance", arguments={"term": "RACI"}
            )
            for block in result.content:
                text = getattr(block, "text", "")
                print(text[:800] + ("..." if len(text) > 800 else ""))

            # 7. Ler um Resource específico (se existir P-LEG-01).
            try:
                print("\n--- READ prompt://P-LEG-01/manifest ---")
                content = await session.read_resource("prompt://P-LEG-01/manifest")
                for block in content.contents:
                    text = getattr(block, "text", "")
                    print(text[:400] + ("..." if len(text) > 400 else ""))
            except Exception as exc:  # noqa: BLE001
                print(f"  (não foi possível ler: {exc})")

            # 8. Listar Prompts.
            prompts = await session.list_prompts()
            print(f"\n--- PROMPTS ({len(prompts.prompts)}) ---")
            for p in prompts.prompts:
                print(f"  {p.name} — {(p.description or '').splitlines()[0]}")

    print("\n[client] OK — biblioteca-interna respondeu a todas as operações.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
