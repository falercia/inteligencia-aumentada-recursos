"""Cliente de teste para M01 Hello World.

Não exige Claude Desktop. Sobe o servidor via stdio, executa as três
operações canônicas (list_resources, read_resource, call_tool, list_prompts,
get_prompt) e imprime cada resposta. Ideal para CI e para entender o
protocolo antes de plugar no cliente real.

Como rodar:
    pip install -r requirements.txt
    python client_test.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> int:
    # Caminho do servidor a subir. stdio significa: o cliente lança o processo
    # do servidor e fala com ele via stdin/stdout. É o padrão para clientes
    # locais (Claude Desktop, Cursor, este script).
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).parent / "server.py")],
    )

    print("[client] subindo servidor MCP via stdio...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Handshake — toda sessão MCP começa com initialize.
            await session.initialize()
            print("[client] sessão inicializada\n")

            # 2. Listar Resources expostos pelo servidor.
            resources = await session.list_resources()
            print("--- RESOURCES ---")
            for r in resources.resources:
                print(f"  {r.uri} — {r.name or '(sem nome)'}")

            # 3. Ler o conteúdo de um Resource.
            print("\n--- READ notes://today ---")
            content = await session.read_resource("notes://today")
            for block in content.contents:
                print(getattr(block, "text", "(sem texto)"))

            # 4. Listar Tools expostas pelo servidor.
            tools = await session.list_tools()
            print("\n--- TOOLS ---")
            for t in tools.tools:
                print(f"  {t.name} — {(t.description or '').splitlines()[0]}")

            # 5. Chamar uma Tool.
            print("\n--- CALL create_note ---")
            result = await session.call_tool(
                "create_note",
                arguments={"text": "Teste do cliente: protocolo MCP funcionando."},
            )
            for block in result.content:
                print(getattr(block, "text", "(sem texto)"))

            # 6. Listar Prompts expostos pelo servidor.
            prompts = await session.list_prompts()
            print("\n--- PROMPTS ---")
            for p in prompts.prompts:
                print(f"  {p.name} — {(p.description or '').splitlines()[0]}")

            # 7. Ler um Prompt (devolve a mensagem formatada para o modelo).
            print("\n--- GET PROMPT summarize_my_day ---")
            prompt_msg = await session.get_prompt("summarize_my_day")
            for msg in prompt_msg.messages:
                content = msg.content
                text = getattr(content, "text", str(content))
                print(f"[{msg.role}] {text[:300]}{'...' if len(text) > 300 else ''}")

    print("\n[client] OK — servidor respondeu corretamente em todas as operações.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
