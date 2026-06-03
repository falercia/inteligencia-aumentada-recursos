# CHANGELOG

> Histórico versionado do repositório acompanhante de **Inteligência Aumentada · Os Invariantes da IA** (Fabio Garcia, 2026). Sem cadência fixa anunciada — releases acontecem quando a entrega está pronta para crítica pública.

---

## v1.3.0 — junho de 2026

**Release de multiagentes completos.** A03 (cooperativo) e A04 (adversarial) saem do estado de stub para implementação executável, com READMEs no padrão "Que problema este agente resolve" e exemplos rodáveis. CONTRATO, README mestre e `/prompts/README.md` reescritos honestamente refletindo o estado real do repositório, sem maquiagem.

### Adicionado

**`/agents/a03-orquestrador-especialistas` — multiagente cooperativo em estrela**
- `agent.py` (~200 LOC) com CLI, FanOutGate e tracing integrado
- `especialistas.py` com wrappers de 3 prompts (P-LEG-01, P-MED-01, P-SUP-01) como tools
- `system_prompt_orquestrador.md` com regras invioláveis e formato de parecer consolidado
- 3 exemplos rodáveis: jurídico único, multidomínio (clínico + jurídico), fora de escopo
- `kill_switch.py` testável + `requirements.txt`
- Custo estimado: ~0,01–0,02 USD por execução

**`/agents/a04-multiagente-debate` — multiagente adversarial**
- `agent.py` (~250 LOC) orquestrando proponente → oponente → réplicas opcionais → juiz
- 3 system prompts distintos (proponente, oponente, juiz com formato de parecer)
- `eval_config.json` com rubrica de 5 critérios ponderados integrável a `/evals/eval_runner.py`
- Transcript JSON gravado em `outbox/` por execução, para auditoria posterior
- 3 exemplos rodáveis: RAG vs fine-tuning, deploy próprio vs API, promoção F3 nível 3→4
- `kill_switch.py` testável + `requirements.txt`
- Custo estimado: ~0,04–0,08 USD por execução

### Alterado

- `agents/README.md` — A03 e A04 saem de "stub" para "completo" na tabela
- `README.md` (raiz) — tabela "Outras pastas" atualizada; A03 e A04 marcados como executáveis
- `CONTRATO.md` — reescrito no formato "Para quem é" + estado real por pasta, com glossário inline para "Camada Dupla" e referência aos releases anteriores
- `prompts/README.md` — reescrito refletindo os 30 prompts publicados em v1.0.0 + 3 calibrações de v1.1.1, com lista completa dos 30 prompts e seção de convite à calibração por painel especialista
- `prompts/<ID>/README.md` (individuais) — sem mudança nesta release; estado v1.0.0 preservado

### Filosofia editorial reafirmada

A04 trata explicitamente o caso de **empate técnico honesto** como decisão arbitral legítima — não há covardia editorial em reconhecer que dois argumentos sustentam mérito comparável quando o contexto admite. A rubrica em `eval_config.json` penaliza vitória forçada quando as notas por critério saem empatadas, e o juiz é instruído a identificar **pontos cegos não cobertos por nenhum dos dois lados** como parte obrigatória do parecer.

A03 trata explicitamente o caso de **fora de escopo** como output legítimo — o orquestrador não deve atender consulta que cabe a especialista não registrado. Recusar com encaminhamento é resposta de qualidade; tentar atender com cobertura parcial é o anti-padrão clássico do multiagente que entrega medíocre em tudo.

---

## v1.2.0 — junho de 2026

**Release de agentes educacionais, servidores MCP e notebooks fundacionais.** Cumpre as três frentes pendentes da arquitetura prevista no APX-L: agentes em Python puro lado a lado nos níveis F3, servidores MCP demonstráveis e notebooks didáticos que materializam os capítulos de fundação.

### Adicionado

**`/agents` — agentes educacionais em Python puro**
- `_common/` — infraestrutura compartilhada (cliente Anthropic com dry-run, tracer JSONL, 3 tools educacionais seguras)
- `a01-react-simples/` — loop ReAct canônico, ~150 LOC, com 3 exemplos e kill switch
- `a02-escala-propriedade/` — mesmo agente em 4 níveis F3 (Assistente / Co-piloto / Supervisionado / Autônomo Regulado) com gates de promoção, kill switch e rollback documentado
- `a03-orquestrador-especialistas/` — stub estrutural com README explicando o que vai entrar
- `a04-multiagente-debate/` — stub estrutural com README explicando o que vai entrar

**`/mcp` — servidores MCP educacionais**
- `m01-hello-world/` — servidor MCP com 1 Resource + 1 Tool + 1 Prompt mínimos (~80 LOC)
- `m02-biblioteca-interna/` — expõe `/prompts` e `/governance/v1` como Resources dinâmicos, com Tools `list_prompts(domain)` e `search_governance(term)`
- Cliente de teste local em ambos (sem necessidade de Claude Desktop)
- SDK oficial Anthropic `mcp>=1.0.0`, transporte stdio

**`/notebooks` — 4 fundacionais**
- `N01-tokenizacao.ipynb` — `tiktoken` local, comparação PT vs EN, estimativa de custo (Capítulo 3)
- `N02-janela-contexto.ipynb` — reprodução do experimento Lost in the Middle (Capítulo 4)
- `N03-embeddings.ipynb` — sentence-transformers local, similaridade coseno, visualização 2D com PCA, busca semântica (Capítulo 5)
- `N04-prompt-caching.ipynb` — comparação SEM vs COM cache em conversa multi-turno (Capítulo 18)
- Cada notebook tem modo DEMO para quem não tem `ANTHROPIC_API_KEY`

### Alterado

- `README.md` (raiz) — reescrito sem promessas de cadência fixa anunciada (decisão editorial firme da obra estendida ao repositório)

---

## v1.1.1 — junho de 2026

**Release de golden sets calibrados.** Adiciona, para os 3 prompts mais utilizados em demonstrações da obra, golden sets expandidos prontos para execução automatizada via `eval_runner.py`.

### Adicionado

- `prompts/P-LEG-01/` — `eval.config.yaml` + `golden.yaml` com 20 casos calibrados (10 fáceis + 6 médios + 4 limítrofes) sobre cláusulas de não-concorrência CLT
- `prompts/P-MED-01/` — `eval.config.yaml` + `golden.yaml` com 20 casos calibrados sobre triagem clínica básica
- `prompts/P-SUP-01/` — `eval.config.yaml` + `golden.yaml` com 20 casos calibrados sobre classificação de severidade de ticket SaaS

A nomenclatura curta das 3 pastas (`P-LEG-01`, `P-MED-01`, `P-SUP-01`) coexiste com as pastas descritivas correspondentes de v1.0.0 (`P-LEG-01-clausula-nao-concorrencia-clt` etc.). A pasta curta carrega configuração de eval pronta para `eval_runner.py`; a pasta descritiva carrega o XML completo, golden inicial, anti-padrões e changelog editorial. Em release futuro, as duas serão consolidadas em estrutura unificada.

---

## v1.1.0 — junho de 2026

**Release de infraestrutura executável de evals.** Entrega o motor de regressão rodável e a estrutura de golden sets compilados em JSONL.

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
- Arquivos `.jsonl` por prompt gerados via `compile_golden_sets.py`. O JSONL é resultado da compilação dos YAMLs originais; o YAML é a fonte da verdade

---

## v1.0.1 — junho de 2026

**Release do Caderno de Governança v1.0.** Materializa o Apêndice O do livro em forma Camada Dupla — ficha conceitual no livro, caderno executável aqui.

### Adicionado

**`/governance/v1/` — caderno operacional executável**
- `00-modelo-caderno-completo.md` — caderno inteiro em arquivo único para imprimir e assinar
- `01-identificacao-escopo-principios.md`
- `02-raci-comite.md`
- `03-aup.md` (política de uso aceitável)
- `04-controles-canonicos.md` (10 controles com maturidade autodeclarada)
- `05-plano-incidente.md` (severidades e playbook)
- `06-assinaturas-revisao.md`
- `ANEXOS.md` — modelos dos 6 anexos referenciados
- `CHANGELOG.md` — versionamento próprio do caderno
- `README.md` — instruções de adoção

---

## v1.0.0 — junho de 2026

**Release inicial.** Biblioteca completa de 30 prompts profissionais em qualidade plena, distribuídos em 9 domínios, cada um com XML executável, golden set categorizado, anti-padrões, changelog e README.

### Adicionado

**`/prompts/` — 30 prompts em 9 domínios**

| Domínio | Prompts |
|---|---|
| Jurídico | P-LEG-01, P-LEG-02, P-LEG-03, P-LEG-04 |
| Saúde | P-MED-01, P-MED-02, P-MED-03 |
| Financeiro | P-FIN-01, P-FIN-02, P-FIN-03, P-FIN-04 |
| SaaS | P-SAAS-01, P-SAAS-02, P-SAAS-03, P-SAAS-04 |
| Suporte | P-SUP-01, P-SUP-02, P-SUP-03 |
| RH | P-RH-01, P-RH-02, P-RH-03 |
| Marketing | P-MKT-01, P-MKT-02, P-MKT-03 |
| Educação | P-EDU-01, P-EDU-02, P-EDU-03 |
| Transversais | P-TR-01, P-TR-02, P-TR-03 |

Cada prompt segue a anatomia da Engenharia de Prompt Estendida (Framework Quatro do livro) com 5 blocos XML obrigatórios + prefill + self-critique. Calibração inicial pelo autor com base em prática profissional do domínio; aberto a contribuição de especialistas via templates de issue.

**`/`** — documentação editorial inicial
- `README.md` — porta de entrada
- `CONTRATO.md` — escopo, política de versionamento, regras de contribuição
- `LICENSE-MIT` — código
- `LICENSE-CC-BY` — conteúdo editorial
- `CONTRIBUTORS.md` — painel de contribuintes

---

> *"Cada release versionado é compromisso editorial cumprido sob crítica pública. Quando a próxima entrega não estiver pronta, o silêncio é mais honesto do que cadência forçada."*
