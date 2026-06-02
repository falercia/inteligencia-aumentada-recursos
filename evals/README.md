# Evals

Scripts e padrões para avaliação de prompts em CI/CD e em produção.

## Estado atual (v1.0.0)

Stub estrutural. O `eval_runner.py` executável chega na **release v1.1.0**
(jul/2026).

## O que estará aqui

- `eval_runner.py` — runner para executar golden sets contra um modelo
- `llm_judge.py` — juiz LLM calibrado para avaliação semântica
- `metrics.py` — métricas padronizadas por tipo de prompt
- `regression_check.py` — comparação automática de releases

## Referência conceitual

Capítulo 39 (Evals) e Framework 8 (Pirâmide da Avaliação) do livro.
