# /datasets — Golden sets compilados em JSONL

> v1.1.0 · julho de 2026 · Companheiros do motor `evals/eval_runner.py`

Esta pasta carrega os 30 golden sets em formato **JSONL** (um caso por linha), gerados a partir dos `prompts/{ID}/golden.yaml` via `evals/compile_golden_sets.py`.

JSONL é o formato preferido para CI porque:
- **Streaming**: ferramentas de pipeline (`jq`, `grep`, `awk`) processam linha a linha sem carregar o arquivo inteiro
- **Diff legível**: cada caso é uma linha, o diff de calibração mostra exatamente o que mudou
- **Auto-contido por linha**: cada linha tem `prompt_id` e `version`, permitindo concatenação livre

---

## Arquivos por domínio

| Domínio | Prompts | Arquivos JSONL |
|---|---|---|
| Jurídico | 4 | `P-LEG-01.jsonl` → `P-LEG-04.jsonl` |
| Saúde | 3 | `P-MED-01.jsonl` → `P-MED-03.jsonl` |
| Financeiro | 4 | `P-FIN-01.jsonl` → `P-FIN-04.jsonl` |
| SaaS | 4 | `P-SAAS-01.jsonl` → `P-SAAS-04.jsonl` |
| Suporte | 3 | `P-SUP-01.jsonl` → `P-SUP-03.jsonl` |
| RH | 3 | `P-RH-01.jsonl` → `P-RH-03.jsonl` |
| Marketing | 3 | `P-MKT-01.jsonl` → `P-MKT-03.jsonl` |
| Educação | 3 | `P-EDU-01.jsonl` → `P-EDU-03.jsonl` |
| Transversais | 3 | `P-TR-01.jsonl` → `P-TR-03.jsonl` |
| **Total** | **30** | **30 arquivos** |

---

## Como gerar a partir dos YAML

```bash
# Compilar todos
python evals/compile_golden_sets.py

# Compilar um específico
python evals/compile_golden_sets.py P-LEG-01

# Apenas validar estrutura (não escreve JSONL)
python evals/compile_golden_sets.py --validate
```

A regra de ouro: **JSONL é gerado, YAML é editado.** A fonte da verdade fica em `prompts/{ID}/golden.yaml`. Editar JSONL diretamente vira inconsistência na próxima compilação.

---

## Esquema de cada linha

```json
{
  "prompt_id": "P-LEG-01",
  "version": "1.0.0",
  "id": "P-LEG-01-F-001",
  "category": "facil",
  "calibration_date": "2026-05-15",
  "input": {
    "clausula": "Texto da cláusula...",
    "cargo": "Gerente",
    "salario": 8500
  },
  "expected": {
    "must_contain": ["elemento temporal", "elemento geográfico"],
    "regex_required": ["classificação:\\s*(baixo|médio|alto|crítico)"],
    "json_keys": ["status", "elementos"]
  },
  "notes": "Caso canônico de cláusula válida com 12 meses"
}
```

Os 20 casos por prompt distribuem-se conforme a Pirâmide F8:

```
10 fáceis        → base canônica de sanidade
 5 médios        → variação típica de tráfego
 5 limítrofes    → ambiguidade calibrada
```

Adversarial sets (categoria `adversarial`) chegam em v1.5.0 (nov/2026), com 10 casos extras por prompt focados em jailbreak, injection e edge cases.

---

## Como usar em CI

```yaml
# .github/workflows/eval.yml
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r evals/requirements.txt
      - run: python evals/compile_golden_sets.py --validate
      - run: python evals/eval_runner.py --prompt P-LEG-01 --ci
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## Calibração e contribuição

Cada caso carrega `calibration_date`. Recomendação editorial: revisar todos os casos com data anterior a 12 meses, conforme `eval.config.yaml` declara `recalibration_due_after_days: 365`.

Contribuições de calibração especialista são incorporadas na revisão mensal seguinte, conforme `CONTRATO.md` do repositório.

---

*JSONL compilados v1.1.0 — primeira release executável. Cadência mensal de revisão nos primeiros 12 meses pós-lançamento.*
