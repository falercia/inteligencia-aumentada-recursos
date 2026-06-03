"""Tool 'calculator' — avalia expressões matemáticas com segurança.

Por que não usar eval() direto?
Porque eval() em produção é vulnerabilidade clássica. Mesmo em educacional,
mostrar eval() ensina o vício. A implementação aqui usa ast.parse + visitor
pattern para aceitar apenas operadores aritméticos básicos.
"""

from __future__ import annotations

import ast
import operator
from typing import Any

CALCULATOR_TOOL = {
    "name": "calculator",
    "description": (
        "Avalia uma expressão matemática segura com operadores +, -, *, /, **, %, // "
        "e parênteses. Não aceita variáveis nem funções. Use para cálculos exatos "
        "que LLMs costumam errar (porcentagem, juros, conversão de unidade)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Expressão a avaliar, ex: '(12450 * 0.18)'",
            }
        },
        "required": ["expression"],
    },
}

_ALLOWED_OPERATORS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError(f"Constante não numérica: {node.value!r}")
    if isinstance(node, ast.BinOp):
        op = _ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operador binário não permitido: {type(node.op).__name__}")
        return op(_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp):
        op = _ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operador unário não permitido: {type(node.op).__name__}")
        return op(_evaluate(node.operand))
    raise ValueError(f"Nó AST não permitido: {type(node).__name__}")


def execute_calculator(tool_input: dict[str, Any]) -> str:
    """Executa a tool 'calculator'. Devolve string com o resultado ou erro."""
    if tool_input.get("_dry_run"):
        return "[dry-run] cálculo simulado: 2242.10"
    expression = tool_input.get("expression", "")
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
    except (SyntaxError, ValueError, ZeroDivisionError) as exc:
        return f"Erro ao avaliar expressão {expression!r}: {exc}"
    # Formato amigável: inteiro se exato, duas casas decimais caso contrário.
    if result == int(result):
        return str(int(result))
    return f"{result:.4f}".rstrip("0").rstrip(".")
