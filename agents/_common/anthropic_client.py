"""Wrapper fino do SDK oficial da Anthropic, com modo seco (dry-run).

Por que não usar o SDK direto?
Porque toda chamada precisa ser instrumentada com tracing e ter opção de dry-run,
e centralizar isso aqui evita repetir o mesmo bloco em cada agente. O wrapper
preserva a interface do SDK; quem já conhece o cliente original migra em minutos.

Decisão deliberada: sem retry exponencial, sem rate limit handler, sem cache.
Em educacional executável, essas camadas escondem a mecânica. Em produção, são
exatamente o que sua infra interna já tem.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any

# Import lazy para não falhar em modo seco quando o SDK não está instalado.
try:
    from anthropic import Anthropic
except ImportError:  # pragma: no cover
    Anthropic = None  # type: ignore

from .tracing import Tracer

# Modelo padrão de produção da geração atual (Sonnet 4.6 — referência da obra).
# Ver Capítulo 15 do livro para o critério de encaixe (F2) e Apêndice J para
# a versão corrente datada.
DEFAULT_MODEL = "claude-sonnet-4-5"  # adapte conforme disponibilidade

# Limite de iteração do loop de tool use; protege contra runaway agent.
DEFAULT_MAX_ITERATIONS = 10


@dataclass
class AgentResponse:
    """Resposta consolidada de uma execução completa do agente."""

    final_text: str
    iterations: int
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    dry_run: bool = False


class AnthropicClient:
    """Cliente educacional com dry-run e tracing integrado.

    Uso típico:

        client = AnthropicClient(dry_run=False)
        response = client.run_agent(
            system="Você é um analista de cálculos financeiros.",
            messages=[{"role": "user", "content": "Quanto é 18% de R$ 12.450?"}],
            tools=[CALCULATOR_TOOL],
            tool_executor=execute_calculator,
        )
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        dry_run: bool = False,
        tracer: Tracer | None = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
    ):
        self.model = model
        self.dry_run = dry_run
        self.tracer = tracer or Tracer()
        self.max_iterations = max_iterations

        if not dry_run:
            if Anthropic is None:
                raise RuntimeError(
                    "Pacote 'anthropic' não instalado. "
                    "Rode: pip install anthropic"
                )
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY não configurada. "
                    "Use --dry-run para estudar sem gastar token."
                )
            self._client = Anthropic(api_key=api_key)
        else:
            self._client = None

    def run_agent(
        self,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_executor: Any = None,
        on_tool_call: Any = None,
    ) -> AgentResponse:
        """Loop principal do agente: pensa, age, observa, repete.

        Parâmetros:
            system: a constituição do agente (system prompt)
            messages: histórico de mensagens (a primeira costuma ser do usuário)
            tools: lista de schemas de tool no formato da Anthropic
            tool_executor: callable que recebe (tool_name, tool_input) e devolve string
            on_tool_call: callable opcional chamado antes de cada execução de tool;
                          se retornar False, a tool é bloqueada (gate humano)

        Retorna AgentResponse com texto final, iterações e contadores de token.
        """
        response = AgentResponse(final_text="", iterations=0, dry_run=self.dry_run)
        current_messages = list(messages)
        tools = tools or []

        for iteration in range(1, self.max_iterations + 1):
            response.iterations = iteration

            if self.dry_run:
                # Em modo seco, só imprime o que mandaria e simula uma resposta.
                self._print_dry_run_request(
                    iteration, system, current_messages, tools
                )
                # Simulação simples: se há tools, "usa" a primeira disponível;
                # caso contrário, retorna uma resposta sintética e encerra.
                if tools and iteration == 1:
                    fake_tool = tools[0]
                    fake_input = {"_dry_run": True}
                    current_messages.append(
                        {
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "tool_use",
                                    "id": f"dry-{iteration}",
                                    "name": fake_tool["name"],
                                    "input": fake_input,
                                }
                            ],
                        }
                    )
                    current_messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": f"dry-{iteration}",
                                    "content": "[dry-run] resultado simulado da tool",
                                }
                            ],
                        }
                    )
                    continue
                response.final_text = (
                    "[dry-run] resposta final simulada — "
                    "use ANTHROPIC_API_KEY para resposta real"
                )
                break

            t0 = time.time()
            api_response = self._client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system,
                tools=tools,
                messages=current_messages,
            )
            latency_ms = int((time.time() - t0) * 1000)

            response.total_input_tokens += api_response.usage.input_tokens
            response.total_output_tokens += api_response.usage.output_tokens

            self.tracer.log(
                event="api_call",
                iteration=iteration,
                input_tokens=api_response.usage.input_tokens,
                output_tokens=api_response.usage.output_tokens,
                latency_ms=latency_ms,
                stop_reason=api_response.stop_reason,
            )

            # Acrescenta a resposta do modelo ao histórico.
            current_messages.append(
                {"role": "assistant", "content": api_response.content}
            )

            # Se o modelo não pediu tool, terminamos.
            if api_response.stop_reason == "end_turn":
                final_text_blocks = [
                    block.text
                    for block in api_response.content
                    if block.type == "text"
                ]
                response.final_text = "\n".join(final_text_blocks)
                break

            # Executa cada tool pedida.
            tool_results = []
            for block in api_response.content:
                if block.type != "tool_use":
                    continue

                # Gate humano opcional: bloqueia a tool antes da execução.
                if on_tool_call is not None:
                    allowed = on_tool_call(block.name, block.input)
                    if not allowed:
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": "Tool bloqueada pelo gate humano.",
                                "is_error": True,
                            }
                        )
                        response.tool_calls.append(
                            {
                                "name": block.name,
                                "input": block.input,
                                "blocked": True,
                            }
                        )
                        continue

                result = tool_executor(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )
                response.tool_calls.append(
                    {"name": block.name, "input": block.input, "output": result}
                )
                self.tracer.log(
                    event="tool_call",
                    name=block.name,
                    input=block.input,
                    output_preview=str(result)[:200],
                )

            current_messages.append({"role": "user", "content": tool_results})

        return response

    @staticmethod
    def _print_dry_run_request(
        iteration: int,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> None:
        """Imprime no stdout o que seria enviado à API."""
        print(f"\n--- [DRY-RUN] iteração {iteration} ---")
        print(f"system: {system[:140]}...")
        print(f"messages: {len(messages)} mensagens no histórico")
        print(f"tools disponíveis: {[t['name'] for t in tools]}")
        last_user_msg = next(
            (m for m in reversed(messages) if m["role"] == "user"), None
        )
        if last_user_msg:
            content = last_user_msg["content"]
            preview = content if isinstance(content, str) else json.dumps(content)[:200]
            print(f"última mensagem do usuário (preview): {preview[:200]}")
