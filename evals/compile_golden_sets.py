#!/usr/bin/env python3
"""
compile_golden_sets.py — Compila YAML → JSONL para uso em CI
============================================================
v1.1.0 (julho de 2026)

Lê todos os golden sets em prompts/{ID}/golden.yaml e escreve em
datasets/{ID}.jsonl, um caso por linha. JSONL é mais rápido para
streaming em pipelines de CI e mais simples para grep/jq.

USO
---
    python compile_golden_sets.py              # todos os prompts
    python compile_golden_sets.py P-LEG-01     # um prompt específico
    python compile_golden_sets.py --validate   # apenas valida estrutura

ESTRUTURA ESPERADA DO YAML
--------------------------
    prompt_id: P-LEG-01
    version: 1.0.0
    cases:
      - id: P-LEG-01-F-001
        category: facil
        calibration_date: 2026-05-15
        input:
          clausula: "..."
          cargo: "..."
          salario: 8500
        expected:
          must_contain:
            - "elemento temporal"
            - "elemento geográfico"
          regex_required:
            - "classificação:\\s*(baixo|médio|alto|crítico)"
          json_keys:
            - "status"
            - "elementos"
        notes: "Caso canônico de cláusula válida com 12 meses"

ESTRUTURA DE SAÍDA JSONL
------------------------
Uma linha por caso, com campo `prompt_id` e `version` adicionados em cada linha
para que o arquivo seja autocontido em pipelines de processamento.
"""

from __future__ import annotations

import json
import pathlib
import sys

try:
    import yaml
except ImportError:
    print("ERRO: este script requer pyyaml. Instale com: pip install pyyaml")
    sys.exit(1)

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
DATASETS_DIR = ROOT / "datasets"
DATASETS_DIR.mkdir(exist_ok=True)


def resolve_prompt_dir(prompt_id: str) -> pathlib.Path:
    """Resolve um ID para a pasta do prompt, aceitando o nome exato
    (P-LEG-01) ou o prefixo da pasta canônica (P-LEG-01-clausula-...)."""
    exact = PROMPTS_DIR / prompt_id
    if exact.is_dir():
        return exact
    matches = sorted(p for p in PROMPTS_DIR.glob(f"{prompt_id}*") if p.is_dir())
    return matches[0] if matches else exact


def golden_path(prompt_dir: pathlib.Path) -> pathlib.Path:
    """Nome canônico do golden set é 'golden-set.yaml' (gerado por
    extract-prompts.py); aceita 'golden.yaml' por retrocompatibilidade."""
    canonical = prompt_dir / "golden-set.yaml"
    return canonical if canonical.exists() else prompt_dir / "golden.yaml"


def validate_case(case: dict, prompt_id: str) -> list[str]:
    errors = []
    required = ["id", "category", "input", "expected"]
    for k in required:
        if k not in case:
            errors.append(f"{prompt_id}: caso sem campo obrigatório '{k}'")
    if "category" in case and case["category"] not in (
        "facil", "medio", "limitrofe", "adversarial"
    ):
        errors.append(f"{prompt_id}/{case.get('id')}: category inválida '{case['category']}'")
    return errors


def compile_prompt(prompt_id: str, validate_only: bool = False) -> tuple[int, list[str]]:
    prompt_dir = resolve_prompt_dir(prompt_id)
    prompt_id = prompt_dir.name  # normaliza para o nome canônico da pasta
    yaml_path = golden_path(prompt_dir)
    if not yaml_path.exists():
        return 0, [f"{prompt_id}: golden-set.yaml não encontrado em {yaml_path}"]

    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    version = data.get("version", "0.0.0")

    # Dois formatos coexistem no repo: o EXECUTÁVEL ('cases' com input/expected,
    # que o motor roda) e o DESCRITIVO ('casos' com descrição livre, gerado por
    # extract-prompts.py a partir do golden set em prosa do livro). O descritivo
    # não tem asserções e não pode ser compilado para JSONL executável.
    if not cases and data.get("casos"):
        n = len(data["casos"])
        return 0, [f"{prompt_id}: golden set DESCRITIVO ({n} casos), sem asserções "
                   f"executáveis — requer upgrade ao formato 'cases/input/expected'"]

    errors = []
    for c in cases:
        errors.extend(validate_case(c, prompt_id))

    if validate_only or errors:
        return len(cases), errors

    out_path = DATASETS_DIR / f"{prompt_id}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for c in cases:
            row = {"prompt_id": prompt_id, "version": str(version), **c}
            # JSON não serializa date/datetime nativos — convertemos para ISO string
            f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")

    return len(cases), errors


def main():
    args = sys.argv[1:]
    validate_only = "--validate" in args
    args = [a for a in args if not a.startswith("--")]

    if args:
        prompts = args
    else:
        prompts = sorted(
            p.name for p in PROMPTS_DIR.iterdir()
            if p.is_dir() and (
                (p / "golden-set.yaml").exists() or (p / "golden.yaml").exists()
            )
        )

    total_cases = 0
    total_errors = []
    for pid in prompts:
        n, errors = compile_prompt(pid, validate_only)
        total_cases += n
        total_errors.extend(errors)
        action = "validado" if validate_only else "compilado"
        if errors:
            print(f"  ✗ {pid}: {len(errors)} erro(s)")
        else:
            print(f"  ✓ {pid}: {n} casos {action}")

    print()
    print(f"Total: {len(prompts)} prompts · {total_cases} casos")
    if total_errors:
        print(f"\n{len(total_errors)} erros encontrados:")
        for e in total_errors[:20]:
            print(f"  - {e}")
        sys.exit(1)
    print("OK." if validate_only else f"JSONL escritos em {DATASETS_DIR}")


if __name__ == "__main__":
    main()
