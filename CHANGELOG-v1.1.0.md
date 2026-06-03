# CHANGELOG — v1.1.0

> Adicionar este conteúdo ao topo do `CHANGELOG.md` do repositório raiz no momento do push.

---

## v1.1.0 — julho de 2026

**Release de infraestrutura executável.** Cumpre o compromisso público declarado no README v1.0.0 de entregar `eval_runner.py` rodável e estrutura de golden sets em JSONL.

### Adicionado

**Motor de avaliação rodável em `/evals`**
- `evals/eval_runner.py` — motor de regressão executável com:
  - Provedores Anthropic, OpenAI e dry-run (sem dependência de API)
  - Quatro judges integrados: `substring`, `regex`, `json_schema`, `classification`
  - Gate de CI via flag `--ci` (exit 1 quando score < limiar)
  - Relatórios timestampados em `evals/reports/`
  - Suporte a suite completa (`--suite all`) ou prompt individual
- `evals/compile_golden_sets.py` — compila `prompts/{ID}/golden.yaml` em `datasets/{ID}.jsonl`
- `evals/requirements.txt` — dependências mínimas
- `evals/README.md` — documentação completa de uso, custos por modelo, integração CI

**Estrutura de golden sets em `/datasets`**
- `datasets/README.md` — esquema JSONL, distribuição F8 (10 fáceis / 5 médios / 5 limítrofes), workflow de calibração
- Arquivos `.jsonl` por prompt serão gerados localmente pelo autor via `compile_golden_sets.py` antes de cada release pública. O JSONL é resultado da compilação dos YAMLs originais; o YAML é a fonte da verdade

**Pasta `/governance` (publicada em v1.0.1, documentada aqui)**
- 10 arquivos do Caderno de Governança v1.0 já publicados, conforme Apêndice O em forma Camada Dupla

### Alterado

**README.md (raiz)**
- Tabela "Outras pastas" atualizada: `/evals` e `/datasets` saem de "stub estrutural" para "v1.1.0 executável"
- Status atual reflete v1.1.0 ao topo da seção `Cadência pública de expansão`
- Adicionada subseção sobre uso em CI com exemplo de workflow GitHub Actions

### Mantido em cadência futura

- `/notebooks` — chega em v1.2.0 (agosto)
- `/agents` — chega em v1.3.0 (setembro)
- `/mcp` — chega em v1.4.0 (outubro)
- Adversarial sets ampliados — chegam em v1.5.0 (novembro)

### Filosofia editorial reafirmada

O motor entrega a infraestrutura. A calibração dos golden sets continua sendo trabalho que **exige especialista do domínio**, conforme o pacto editorial do APX-L no livro. O motor não substitui o calibrador humano; ele instrumenta a confiança no que o calibrador definiu.

---

*Release v1.1.0 publicada em julho de 2026. Próxima janela: agosto de 2026 (v1.2.0 — Notebooks fundacionais).*
