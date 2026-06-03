"""Tracing local em JSONL, sem dependência externa.

Por que JSONL e não OpenTelemetry?
Educacional. JSONL é legível em qualquer editor de texto, processável em uma
linha de jq, e não exige rodar Jaeger/Tempo/Honeycomb para o leitor ver o que
saiu. Em produção, o tracer aqui é o ponto natural de troca: sua infra interna
pluga um exporter para OTLP/OpenTelemetry GenAI sem mexer no resto.

Cada chamada vira uma linha JSON com timestamp, event, e payload arbitrário.
O arquivo cresce indefinidamente; quem quer rotacionar passa um novo path.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any


class Tracer:
    """Logger JSONL local. Thread-safe não é objetivo; agentes educacionais
    rodam single-thread.
    """

    def __init__(self, path: str | Path | None = None, enabled: bool = True):
        self.enabled = enabled
        if path is None:
            traces_dir = Path("./traces")
            traces_dir.mkdir(exist_ok=True)
            ts = time.strftime("%Y%m%d-%H%M%S")
            self.path = traces_dir / f"trace-{ts}-{os.getpid()}.jsonl"
        else:
            self.path = Path(path)
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: str, **payload: Any) -> None:
        if not self.enabled:
            return
        record = {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event,
            **payload,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    def __enter__(self) -> Tracer:
        self.log(event="trace_start")
        return self

    def __exit__(self, *args: Any) -> None:
        self.log(event="trace_end")

    def summary(self) -> dict[str, Any]:
        """Lê o trace e devolve um sumário básico — útil para o agente imprimir
        no fim da execução.
        """
        if not self.path.exists():
            return {"events": 0, "path": str(self.path)}
        events: list[dict[str, Any]] = []
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        api_calls = [e for e in events if e.get("event") == "api_call"]
        tool_calls = [e for e in events if e.get("event") == "tool_call"]
        return {
            "events": len(events),
            "api_calls": len(api_calls),
            "tool_calls": len(tool_calls),
            "total_input_tokens": sum(e.get("input_tokens", 0) for e in api_calls),
            "total_output_tokens": sum(e.get("output_tokens", 0) for e in api_calls),
            "total_latency_ms": sum(e.get("latency_ms", 0) for e in api_calls),
            "path": str(self.path),
        }
