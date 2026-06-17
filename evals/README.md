# /evals — Motor de regressão

> v1.1.0 · julho de 2026 · Implementação executável do Framework Oito · Pirâmide da Avaliação

Esta pasta entrega o motor de regressão que sustenta o Invariante Sete da obra, **Termômetro Permanente**, em forma executável. Trocar prompt porque "ficou melhor" sem golden set é torcida, não decisão. Aqui está a bateria de testes automatizada que separa os dois.

---

## O que tem aqui

| Arquivo | Função |
|---|---|
| [`eval_runner.py`](./eval_runner.py) | Motor principal. Roda um prompt contra seu golden set, calcula score, gera relatório, retorna gate de CI |
| [`compile_golden_sets.py`](./compile_golden_sets.py) | Compila os 30 golden sets de YAML → JSONL para uso em CI |
| [`reports/`](./reports/) | Relatórios timestampados de cada execução (gerado automaticamente) |
| `requirements.txt` | Dependências mínimas (`anthropic`, `pyyaml`, opcionalmente `openai`) |

---

## Como rodar em 30 segundos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar credencial (Anthropic é o provedor padrão)
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Rodar um prompt específico
python eval_runner.py --prompt P-LEG-01

# 4. Modo dry-run (não chama API — valida estrutura)
python eval_runner.py --prompt P-LEG-01 --dry-run

# 5. Suite completa
python eval_runner.py --suite all

# 6. Modo CI (exit 1 se score < limiar)
python eval_runner.py --prompt P-LEG-01 --ci
```

---

## Arquitetura aplicada do Framework Oito

```
Topo      ◇ Adversariais   (10 casos)   — robustez contra jailbreak, injection, edge cases
Meio      ◇ Limítrofes     (5 casos)    — ambiguidade calibrada, escolha conservadora
Meio      ◇ Médios         (5 casos)    — variação típica de tráfego real
Base      ◇ Fáceis         (10 casos)   — sanidade básica, garantia mínima
```

Cada caso do golden set carrega:
- `id`: identificador estável
- `category`: `facil` | `medio` | `limitrofe` | `adversarial`
- `input`: variáveis nomeadas que serão substituídas no prompt
- `expected`: critérios de avaliação (`must_contain`, `regex_required`, `json_keys`, etc.)
- `calibration_date`: data em que o caso foi calibrado (Invariante 5, Honestidade Temporal)
- `notes`: contexto humano da calibração

---

## Os judges disponíveis

| Judge | Quando usar | Custo | Confiabilidade |
|---|---|---|---|
| `substring` | Verificação de presença/ausência de termos obrigatórios | Zero | Alta para regras categóricas |
| `regex` | Padrões com variação léxica | Zero | Alta com regex bem calibrado |
| `json_schema` | Outputs estruturados em JSON | Zero | Alta para schema fechado |
| `classification` | Comparação de classe categórica esperada | Zero | Alta quando o output declara explicitamente |
| `llm_as_judge` (v1.2.0) | Critério qualitativo (clareza, completude) | Médio-alto | Calibrar contra rotulagem humana |

A escolha dos judges ativos por prompt fica em `prompts/{ID}/eval.config.yaml`. Recomendação: combinar pelo menos dois judges (substring + json_schema, ou regex + classification) para reduzir falso positivo.

---

## Gate de CI

O comportamento padrão é informativo (sai com código 0 sempre, imprime relatório). O modo `--ci` ativa o gate de release:

```yaml
# .github/workflows/eval.yml
- name: Eval prompts críticos
  run: |
    python evals/eval_runner.py --prompt P-LEG-01 --ci
    python evals/eval_runner.py --prompt P-MED-01 --ci
    python evals/eval_runner.py --prompt P-FIN-02 --ci
```

Score abaixo do limiar (`threshold` em `eval.config.yaml`, padrão 0.85) → exit 1 → build falha.

---

## Custo estimado por execução

Cálculo orientativo, em USD, considerando Anthropic em junho de 2026:

| Cenário | Modelo | Casos | Custo aproximado |
|---|---|---|---|
| Um prompt em CI | Haiku 4.5 | 20 | ~$0,05 |
| Suite completa em CI | Haiku 4.5 | 600 | ~$1,50 |
| Suite completa em release | Sonnet 4.6 | 600 | ~$10 |
| Suite completa em release com Opus | Opus 4.6 | 600 | ~$45 |

**Recomendação operacional.** Haiku no PR check, Sonnet no merge para main, Opus apenas no release público com tag versionada. Invariante Cinco, Custo Composto, aplicado à esteira de avaliação.

---

## Limitações conhecidas

- **LLM-as-judge não é determinístico.** Mesmo com temperatura 0, há variação entre execuções. Para gate crítico, rodar duas amostras e usar consenso, ou calibrar contra rotulagem humana periodicamente.
- **Custo de Opus em CI é proibitivo.** Não rodar suite completa em Opus a cada commit. Reserva para release.
- **Golden set congela.** Casos calibrados em 2026 podem virar irrelevantes em 2027. Revisão anual obrigatória.

---

## Como contribuir

Calibração especialista de golden case continua sendo a contribuição mais valiosa. Abra issue com o template `golden-set-calibration` (em `.github/ISSUE_TEMPLATE/`).

Para contribuir um novo judge (por exemplo, validador específico de jurídico LGPD), enviar PR adicionando função em `eval_runner.py` no dicionário `JUDGES` e atualizando este README.

---

*Versão executável v1.1.0 — primeira release com motor rodável. Próximo marco (v1.5.0, nov/2026): `llm_as_judge` calibrado contra rotulagem humana, com adversarial sets ampliados.*
