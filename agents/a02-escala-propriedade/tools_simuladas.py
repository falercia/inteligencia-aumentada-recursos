"""Quatro tools simuladas para a tarefa de cancelamento de assinatura.

Padrão de risco crescente:
1. customer_lookup        → leitura pura (sem efeito)
2. draft_cancellation_email → gera texto (sem efeito externo)
3. simulate_send_email     → escreve em ./outbox/ (compensável)
4. update_subscription     → muda estado em ./state/ (compensável com fricção)

Nenhuma das tools tem efeito real. O "envio" escreve um arquivo .eml no
diretório local. A atualização de subscription grava em JSON local. O ponto
educacional não é a mecânica das tools, é o GATE de autorização nos arquivos
nivel_*.py.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

OUTBOX = Path("./outbox")
STATE = Path("./state")

# Tools "read-only" — disponíveis em todos os níveis.
CUSTOMER_LOOKUP_TOOL = {
    "name": "customer_lookup",
    "description": (
        "Busca os dados atuais da assinatura de um cliente. Retorna nome do contato, "
        "plano, status, data de início e indicação se há fatura em aberto. "
        "Esta tool é leitura pura, sem efeito externo."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_name": {"type": "string"},
        },
        "required": ["customer_name"],
    },
}

DRAFT_EMAIL_TOOL = {
    "name": "draft_cancellation_email",
    "description": (
        "Gera o texto de um e-mail de confirmação de cancelamento. NÃO envia. "
        "Retorna assunto e corpo prontos para revisão."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_name": {"type": "string"},
            "contact_email": {"type": "string"},
            "cycle_end_date": {"type": "string"},
        },
        "required": ["customer_name", "contact_email", "cycle_end_date"],
    },
}

# Tools "write" — restritas conforme o nível.
SEND_EMAIL_TOOL = {
    "name": "simulate_send_email",
    "description": (
        "Envia um e-mail (simulação: escreve um arquivo .eml em ./outbox/). "
        "Ação compensável via envio de e-mail de retratação."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "to": {"type": "string"},
            "subject": {"type": "string"},
            "body": {"type": "string"},
        },
        "required": ["to", "subject", "body"],
    },
}

UPDATE_SUB_TOOL = {
    "name": "update_subscription",
    "description": (
        "Atualiza o status da assinatura de um cliente. Ação compensável: o estado "
        "anterior é gravado em backup antes da mudança e pode ser revertido."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_name": {"type": "string"},
            "new_status": {
                "type": "string",
                "enum": ["ativa", "cancelada-fim-ciclo", "suspensa"],
            },
        },
        "required": ["customer_name", "new_status"],
    },
}

# Dataset simulado de clientes — único arquivo de "fonte da verdade".
_FAKE_CUSTOMERS = {
    "Acme Industrial": {
        "contact_email": "contratos@acme.example",
        "plan": "Enterprise",
        "status": "ativa",
        "started_at": "2024-03-15",
        "cycle_end_date": "2026-09-30",
        "open_invoice": False,
    },
    "Beta Logistics": {
        "contact_email": "financeiro@beta.example",
        "plan": "Growth",
        "status": "ativa",
        "started_at": "2025-01-10",
        "cycle_end_date": "2026-12-31",
        "open_invoice": True,  # caso adverso: o agente deve recusar cancelamento
    },
}


def execute_customer_lookup(tool_input: dict[str, Any]) -> str:
    if tool_input.get("_dry_run"):
        return "[dry-run] dados simulados do cliente"
    name = tool_input.get("customer_name", "")
    data = _FAKE_CUSTOMERS.get(name)
    if data is None:
        return f"Cliente {name!r} não encontrado."
    return json.dumps(data, ensure_ascii=False)


def execute_draft_email(tool_input: dict[str, Any]) -> str:
    if tool_input.get("_dry_run"):
        return "[dry-run] rascunho de e-mail"
    name = tool_input.get("customer_name", "Cliente")
    end = tool_input.get("cycle_end_date", "[data]")
    subject = f"Confirmação de cancelamento — {name}"
    body = (
        f"Prezados,\n\n"
        f"Confirmamos o recebimento do pedido de cancelamento da assinatura "
        f"de {name}. O serviço permanecerá ativo até o fim do ciclo atual, "
        f"em {end}, após o qual o acesso será descontinuado.\n\n"
        f"Quaisquer dúvidas sobre o processo de offboarding ou exportação de "
        f"dados podem ser endereçadas a esta caixa.\n\n"
        f"Atenciosamente,\nOperações"
    )
    return json.dumps({"subject": subject, "body": body}, ensure_ascii=False)


def execute_send_email(tool_input: dict[str, Any]) -> str:
    if tool_input.get("_dry_run"):
        return "[dry-run] e-mail seria enviado"
    OUTBOX.mkdir(exist_ok=True)
    to = tool_input["to"]
    subject = tool_input["subject"]
    body = tool_input["body"]
    ts = time.strftime("%Y%m%d-%H%M%S")
    filename = OUTBOX / f"{ts}-{to.replace('@', '-at-')}.eml"
    content = f"To: {to}\nSubject: {subject}\n\n{body}\n"
    filename.write_text(content, encoding="utf-8")
    return f"E-mail simulado escrito em {filename}"


def execute_update_subscription(tool_input: dict[str, Any]) -> str:
    if tool_input.get("_dry_run"):
        return "[dry-run] status atualizado"
    STATE.mkdir(exist_ok=True)
    name = tool_input["customer_name"]
    new_status = tool_input["new_status"]
    state_file = STATE / "subscriptions.json"
    if state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))
    else:
        state = {}
    previous = state.get(name, {}).get("status", "desconhecido")
    # Backup compensável: grava o estado anterior em arquivo separado.
    backup = STATE / f"backup-{name.replace(' ', '_')}-{time.strftime('%Y%m%d-%H%M%S')}.json"
    backup.write_text(
        json.dumps({"name": name, "previous_status": previous}, ensure_ascii=False),
        encoding="utf-8",
    )
    state[name] = {"status": new_status, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return f"Status de {name!r} atualizado: {previous} → {new_status}. Backup em {backup}."


# Registros canônicos a importar nos arquivos nivel_*.py
ALL_TOOLS = [
    CUSTOMER_LOOKUP_TOOL,
    DRAFT_EMAIL_TOOL,
    SEND_EMAIL_TOOL,
    UPDATE_SUB_TOOL,
]

READ_ONLY_TOOLS = [CUSTOMER_LOOKUP_TOOL, DRAFT_EMAIL_TOOL]

WRITE_TOOL_NAMES = {"simulate_send_email", "update_subscription"}

TOOL_REGISTRY = {
    "customer_lookup": execute_customer_lookup,
    "draft_cancellation_email": execute_draft_email,
    "simulate_send_email": execute_send_email,
    "update_subscription": execute_update_subscription,
}


def dispatch(name: str, tool_input: dict[str, Any]) -> str:
    fn = TOOL_REGISTRY.get(name)
    if fn is None:
        return f"Erro: tool {name!r} desconhecida."
    return fn(tool_input)
