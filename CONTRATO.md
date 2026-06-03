# CONTRATO DO REPOSITÓRIO ACOMPANHANTE

> **O que você está olhando.** Este repositório é o companheiro executável do livro **Inteligência Aumentada · Os Invariantes da IA** (Fabio Garcia, 2026). Ele existe deliberadamente fora do corpo do livro porque carrega artefatos que envelhecem mais rápido do que a tinta da página: prompts em XML versionado, golden sets executáveis, agentes em Python, servidores MCP, notebooks didáticos e o caderno operacional de governança.

> **Para quem é este documento.** Você está aqui se quer entender o contrato editorial deste repositório antes de clonar, antes de contribuir, antes de adotar em produção. Este arquivo declara o escopo, a política de versionamento, as regras de manutenção e os limites do que o autor se compromete a entregar.

---

## Para quem é este repositório

| Se você é... | Vai sair daqui com... |
|---|---|
| **Leitor do livro** que terminou o APX-L e quer baixar os 30 prompts em XML executável | Caminho direto para [`/prompts`](./prompts/) com 30 prompts profissionais publicados em v1.0.0, cada um com `prompt.xml`, `golden-set.yaml`, `anti-padroes.md`, `changelog.md` e `README.md` |
| **CTO / Tech Lead / AI Engineer** em adoção real de IA em produção | Caminho direto para [`/evals`](./evals/) — motor de regressão rodável + 4 judges (substring, regex, json_schema, classification) + gate de CI; complementado por 3 golden sets calibrados em [`/datasets`](./datasets/) |
| **Auditor / Compliance / DPO** validando governança de IA | Caminho direto para [`/governance/v1`](./governance/v1/) — caderno em 6 seções fatiadas + 10 controles + anexos clonáveis + changelog |
| **Especialista de domínio** (advogado, médico, suporte sênior, RH, professor) | Caminho para contribuir com calibração de golden set por painel especialista — ver seção **Como contribuir** |
| **Desenvolvedor curioso** querendo ver agente educacional executável em Python puro | Caminho direto para [`/agents`](./agents/) — A01 ReAct, A02 4 níveis F3, A03 Orquestrador cooperativo, A04 Multiagente Debate adversarial |
| **Profissional de IA** estudando integração de modelo com sistemas externos | Caminho direto para [`/mcp`](./mcp/) — M01 Hello World + M02 Biblioteca Interna que expõe `/prompts` e `/governance` como Resources MCP |

---

## A regra editorial inegociável: Camada Dupla

A obra opera sob o que o livro chama de **Camada Dupla** (o Princípio Três dos Nove Invariantes Permanentes da IA): conhecimento em IA vive em dois andares, o padrão que dura e o número que muda. O livro carrega o padrão — frameworks, arquiteturas, anti-padrões, vocabulário durável que sobrevive à próxima geração de modelos. Este repositório carrega o número — XML versionado, golden sets executáveis, scripts de regressão, exemplos rodáveis.

A separação física é deliberada e materializa o método. Quem só lê o livro sai com método; quem só usa este repositório sem ler o livro opera no escuro; quem usa os dois sai com modelo mental sólido e ativos prontos para entrar em pipeline.

---

## O que vive aqui (estado em junho de 2026 · v1.3.0)

```
inteligencia-aumentada-recursos/
├── README.md             ← porta de entrada com visão geral
├── CONTRATO.md           ← este arquivo (escopo, manutenção, contribuição)
├── CHANGELOG.md          ← histórico versionado de releases
├── CONTRIBUTORS.md       ← painel especialista creditado
├── LICENSE-MIT           ← código
├── LICENSE-CC-BY         ← conteúdo editorial
├── prompts/              ← 30 prompts em qualidade plena + 3 calibrações dedicadas
├── governance/v1/        ← caderno operacional executável (artefato do APX-O)
├── evals/                ← motor rodável + judges + gate de CI
├── datasets/             ← golden sets compilados em JSONL prontos para CI
├── agents/               ← A01 + A02 + A03 + A04 educacionais em Python puro
├── mcp/                  ← M01 hello world + M02 biblioteca interna
└── notebooks/            ← 4 fundacionais (tokens, contexto, embeddings, caching)
```

Cada pasta tem `README.md` próprio explicando o que entrega, como rodar e como se conecta ao livro.

---

## Estado real por pasta em v1.3.0 (sem maquiagem)

| Pasta | Estado |
|---|---|
| `/prompts` | **Executável.** 30 prompts profissionais com nomes descritivos (P-LEG-01 a P-LEG-04, P-MED-01 a P-MED-03, P-FIN-01 a P-FIN-04, P-SAAS-01 a P-SAAS-04, P-SUP-01 a P-SUP-03, P-RH-01 a P-RH-03, P-MKT-01 a P-MKT-03, P-EDU-01 a P-EDU-03, P-TR-01 a P-TR-03) publicados em v1.0.0, cada um com `prompt.xml`, `golden-set.yaml`, `anti-padroes.md`, `changelog.md` e `README.md`. Adicionalmente, 3 calibrações dedicadas (P-LEG-01, P-MED-01, P-SUP-01) publicadas em v1.1.1 com `eval.config.yaml` + `golden.yaml` expandido em 20 casos calibrados pelo autor para uso no motor de evals. |
| `/governance/v1` | **Executável.** 10 arquivos — caderno completo + 6 seções fatiadas + anexos + changelog. Pronto para imprimir, customizar e assinar. |
| `/evals` | **Executável.** `eval_runner.py` rodável, `compile_golden_sets.py`, judges integrados (substring, regex, json_schema, classification), gate de CI. |
| `/datasets` | **Executável.** Golden sets compilados em JSONL prontos para CI (a partir dos YAMLs originais em `/prompts`). |
| `/agents` | **Executável — 4 agentes completos.** A01 ReAct Simples, A02 Escala de Propriedade nos 4 níveis F3 lado a lado, A03 Orquestrador-Especialistas (cooperativo em estrela), A04 Multiagente Debate (adversarial com juiz integrável a `/evals`). |
| `/mcp` | **Executável.** M01 Hello World (Resource + Tool + Prompt mínimos), M02 Biblioteca Interna (expõe `/prompts` e `/governance` como Resources para qualquer cliente MCP). |
| `/notebooks` | **Executáveis.** 4 notebooks fundacionais com narrativa didática célula a célula — tokenização, janela de contexto, embeddings, prompt caching. |

Esta tabela é a fonte de verdade do estado do repositório. Qualquer discrepância entre o que outro arquivo declara e esta tabela é erro a corrigir, jamais o contrário.

---

## Política de manutenção e versionamento

| Item | Política |
|---|---|
| **Cadência de release** | Sem cadência fixa anunciada. O autor publica quando a entrega está pronta para crítica pública, e jamais antes. Honestidade temporal vale mais do que calendário cumprido com qualidade rebaixada. |
| **Versionamento** | SemVer aplicado ao repositório inteiro. Marcos publicados: v1.0.0 (30 prompts), v1.0.1 (governance), v1.1.0 (motor de evals), v1.1.1 (golden sets calibrados), v1.2.0 (agents A01/A02 + mcp + notebooks), v1.3.0 (A03 + A04 completos). Pastas com sub-versão (`/governance/v1` vs `v2`) preservam a versão antiga acessível enquanto a nova matura. |
| **Breaking changes** | Anunciados em `CHANGELOG.md` da raiz com nota de migração. |
| **Compatibilidade com o livro** | Cada release declara qual edição do livro o acompanha. A v1.3.0 acompanha a primeira edição (junho de 2026). |
| **Issues e PRs** | Aberto, com curadoria editorial. Aderência aos Invariantes do livro é critério de aceite. PRs sem golden set ou sem citação de fonte primária quando aplicável são rejeitados. |
| **Licença** | MIT para código (scripts Python, notebooks, agentes, servidores MCP). CC-BY 4.0 para conteúdo editorial (prompts em XML, golden sets, anti-padrões, documentação). Uso comercial permitido com atribuição. |

---

## Regras de contribuição

1. **Aderência aos Invariantes.** Todo artefato novo declara, na sua documentação, qual Invariante e qual Framework do livro ele instancia. Sem essa declaração, o PR fica em revisão até o contribuidor explicitar.

2. **Golden set obrigatório.** Todo prompt ou agente novo vem com golden set mínimo de 10 casos categorizados (fáceis / médios / limítrofes), calibrados contra prática profissional do domínio.

3. **Sem versão cravada em código.** Nenhum exemplo cita modelo "claude-sonnet-4-6" diretamente — usa env var ou config. O repositório atravessa gerações de modelos sem precisar refatorar exemplo a exemplo.

4. **Sem PII real.** Nenhum exemplo carrega dado pessoal de cliente, mesmo anonimizado. Todo input de exemplo é sintético, claramente identificado como tal.

5. **Documentação em PT-BR executivo.** O leitor primário é o operador brasileiro de IA. Comentários técnicos podem ser bilíngues; documentação principal é em português, sem hype e sem jargão sem ancoragem.

6. **Fonte primária quando aplicável.** Contribuições que tocam em referência jurídica, médica, regulatória ou em paper técnico devem citar fonte primária verificável. "Eu acho" e "li em algum lugar" são insuficientes.

---

## Tipos de contribuição bem-vindos

| Tipo | Como contribuir | Impacto |
|---|---|---|
| **Calibração especialista do golden set** | Issue com template `golden-set-calibration` — descreva o caso, a saída esperada conforme sua prática, e a fonte primária | **Maior impacto.** É o que vira o repositório referência calibrada por painel em vez de calibrada por autor único |
| **Correção de fato ou referência** | Issue com template `factual-correction` — cite fonte primária correta | Alto impacto; mantém o repositório auditável |
| **Sugestão de novo prompt para a biblioteca** | Issue com template `new-prompt-suggestion` — descreva a dor, o domínio e por que a biblioteca atual não resolve | Médio impacto; pode virar marco de release |
| **Sugestão de novo agente, MCP ou notebook** | Issue livre com proposta de escopo e racional pedagógico | Variável; depende de encaixe com o método |
| **Correção tipográfica ou de gramática** | PR direto, sem necessidade de issue prévia | Baixo impacto individual, alto coletivo |

Contribuições qualificadas entram em [`CONTRIBUTORS.md`](./CONTRIBUTORS.md) quando o contribuidor autoriza.

---

## O que NÃO está aqui (e onde está)

- **Explicação conceitual dos princípios e frameworks** — vive no livro, jamais aqui. Quem ler só este repositório sem o livro opera no escuro.
- **Versões correntes de modelos, preços e benchmarks** — vivem no Apêndice J do livro (instrumento vivo, sem cadência fixa anunciada).
- **Casos brasileiros nomeados em produção** — pendente atribuição nominal de 3-5 empresas BR (item externo do roadmap editorial, 60-90 dias).
- **Suporte 24×7** — este é projeto editorial de autor, não produto comercial com SLA. Issues são respondidas em janela razoável; PRs qualificados são incorporados; nada é prometido em horas.

---

## Conexão com o livro

Este repositório só faz sentido pleno em conjunto com a obra **Inteligência Aumentada · Os Invariantes da IA**, especialmente com:

- **Apêndice L · Biblioteca de Prompts Profissionais** — entrega as 30 fichas conceituais (anatomia, dor, anti-padrões, métrica), cada uma com implementação executável correspondente em [`/prompts`](./prompts/).
- **Apêndice O · Caderno de Governança de IA** — ficha conceitual no livro; caderno executável aqui em [`/governance/v1`](./governance/v1/).
- **Apêndice J · Trilha do Número** — referencia este repositório como fonte viva dos números (modelos, preços, benchmarks, papers, regulação) que mudam mais rápido do que o livro.
- **Framework Quatro · Engenharia de Prompt Estendida** — entrega a anatomia em cinco blocos XML que estrutura cada prompt aqui.
- **Framework Oito · Pirâmide da Avaliação** — entrega o método que sustenta os golden sets e os scripts de regressão da pasta `/evals`.

---

## Atribuição e autor

**Autor:** Fabio Garcia — CTO, Head de Tecnologia, autor da obra **Inteligência Aumentada**.
**LinkedIn:** [linkedin.com/in/falercia](https://linkedin.com/in/falercia)
**Issues e contato editorial:** [github.com/falercia/inteligencia-aumentada-recursos/issues](https://github.com/falercia/inteligencia-aumentada-recursos/issues)

---

> *"Código no repositório. Método no livro. Número no apêndice datado. Quem mistura os três paga em manutenção; quem separa os três opera com vantagem que escala."*
