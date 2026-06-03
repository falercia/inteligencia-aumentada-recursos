"""Tool 'fake_web_search' — pesquisa simulada com resultados canned.

Por que canned?
Educacional rodável sem internet, sem chave de API de buscador, sem custo
adicional. Os resultados são determinísticos por consulta, o que torna o
agente reproduzível em sala de aula e em CI.

Em produção, troque pela tool real do buscador escolhido (Brave Search,
Tavily, Exa, Serper, etc.). O schema continua o mesmo.
"""

from __future__ import annotations

from typing import Any

WEB_SEARCH_TOOL = {
    "name": "fake_web_search",
    "description": (
        "Pesquisa simulada na web com resultados pré-determinados, para fins "
        "educacionais. Devolve até 3 resultados com título e snippet. "
        "Use para demonstrar o padrão ReAct sem depender de chave externa."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Termo a buscar, ex: 'taxa selic atual'",
            }
        },
        "required": ["query"],
    },
}

# Resultados canned: cobrem casos típicos dos exemplos da pasta.
# A escolha é deliberadamente didática; quem quer pesquisa real troca a tool.
_CANNED_RESULTS: dict[str, list[dict[str, str]]] = {
    "selic": [
        {
            "title": "Banco Central do Brasil — Taxa Selic",
            "snippet": (
                "A meta para a taxa Selic é definida pelo Copom. "
                "[Resultado simulado para fins didáticos — consulte fonte primária.]"
            ),
            "url": "https://www.bcb.gov.br/controleinflacao/taxaselic",
        }
    ],
    "lgpd": [
        {
            "title": "ANPD — Lei Geral de Proteção de Dados",
            "snippet": (
                "A LGPD (Lei 13.709/2018) regula o tratamento de dados pessoais. "
                "[Resultado simulado para fins didáticos.]"
            ),
            "url": "https://www.gov.br/anpd/",
        }
    ],
    "claude": [
        {
            "title": "Anthropic — Claude",
            "snippet": (
                "Claude é o assistente de IA da Anthropic. "
                "[Resultado simulado — versão corrente no Apêndice J do livro.]"
            ),
            "url": "https://www.anthropic.com/claude",
        }
    ],
}

_DEFAULT_RESULT = [
    {
        "title": "Resultado simulado",
        "snippet": (
            "Esta tool é uma simulação. Em produção, plugue um buscador real "
            "(Brave/Tavily/Exa) mantendo o mesmo schema."
        ),
        "url": "https://exemplo.local/sem-resultado",
    }
]


def execute_web_search(tool_input: dict[str, Any]) -> str:
    if tool_input.get("_dry_run"):
        return "[dry-run] resultado simulado de pesquisa web"
    query = (tool_input.get("query") or "").lower().strip()
    for keyword, results in _CANNED_RESULTS.items():
        if keyword in query:
            return _format_results(results)
    return _format_results(_DEFAULT_RESULT)


def _format_results(results: list[dict[str, str]]) -> str:
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['title']}\n   {r['snippet']}\n   {r['url']}")
    return "\n".join(lines)
