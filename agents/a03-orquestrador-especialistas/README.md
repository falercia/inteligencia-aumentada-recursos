# A03 — Orquestrador-Especialistas

> **Multiagente em estrela.** Um orquestrador classifica a consulta do usuário, despacha para o especialista certo, e consolida a resposta. Cada especialista é UM prompt versionado de [`/prompts`](../../prompts/) carregado como tool. Quem entendeu A01 entende este em uma sentada — é o mesmo loop, com tools que internamente fazem outra chamada LLM.

---

## Que problema este agente resolve

Toda central de atendimento sofisticada esbarra no mesmo limite arquitetural: **uma consulta de cliente pode envolver domínios distintos, e nenhum operador humano único cobre todos com a mesma profundidade**. A clínica que recebe "torci o tornozelo no trabalho e meu chefe não quer abrir CAT" precisa de competência clínica E trabalhista. O SaaS que recebe "fui cobrado errado e a fatura não bate com meu contrato" precisa de competência técnica E jurídica.

A solução amadora é construir UM agente generalista enorme, com prompt de cinco páginas tentando cobrir todos os domínios — e o resultado é o mesmo: respostas medianas em tudo, ótimas em nada. A solução madura é **multiagente em estrela**: um coordenador que reconhece o domínio e despacha para o especialista certo, com cada especialista profundamente calibrado em UM domínio. **A03 resolve isso na prática**, reusando os prompts profissionais já versionados em [`/prompts`](../../prompts/) (P-LEG-01 cláusula CLT, P-MED-01 triagem clínica, P-SUP-01 suporte técnico SaaS) como cérebros dos especialistas — sem reescrever cada um do zero.

**Para quem é útil:** o time de produto que está construindo central de atendimento multidomínio e não sabe se deve treinar um modelo único ou orquestrar vários; o CTO que precisa decidir entre prompt monolítico e arquitetura modular; o auditor que precisa entender por que despacho explícito é mais defensável do que classificação implícita dentro de um único prompt; o time de M&A, jurídico corporativo ou FP&A que precisa produzir parecer integrado a partir de múltiplas leituras especialistas.

**O que você sai sabendo após rodar:** como funciona o padrão estrela em código real, por que reusar prompts versionados é aplicação direta da Camada Dupla ao próprio agente, como instrumentar fan-out para conter custo composto (F7), e por que recusar atender fora de escopo é uma das competências mais importantes (e mais subestimadas) em sistemas multiagente.

---

## Ficha técnica

| Campo | Valor |
|---|---|
| **Padrão** | Multiagente em estrela (orquestrador + N especialistas) |
| **Especialistas reusados** | P-LEG-01 (jurídico trabalhista), P-MED-01 (triagem clínica), P-SUP-01 (suporte técnico) |
| **Nível F3 declarado** | Supervisionado (sem gate por subtarefa, com kill switch + fan-out limit + trace consolidado) |
| **Modelo do orquestrador** | Sonnet (decisão de classificação + consolidação) |
| **Modelo dos especialistas** | Haiku (resposta especialista, custo otimizado) |
| **Dono nominal** | O leitor que está executando |
| **Tracing** | Ativo por padrão em `../_common/traces/` |
| **Kill switch** | `kill_switch.py` testável (mesmo padrão de A01/A02) |
| **Fan-out limit** | 3 especialistas por execução (configurável via `--max-fan-out`) |
| **Custo estimado** | Tarefa de UM despacho: ~0,01 USD; multidomínio com 2 despachos: ~0,02 USD |

---

## Como rodar

### Pré-requisitos

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"   # ou use --dry-run
```

### Modo seco (sem token, ideal para estudar a mecânica)

```bash
python agent.py --dry-run
```

A saída mostra cada iteração do orquestrador, qual especialista seria chamado, e qual consulta seria despachada. Use com `agent.py` e `especialistas.py` abertos em paralelo para acompanhar o fluxo.

### Modo real — caso default (consulta jurídica CLT)

```bash
python agent.py
```

O agente recebe um caso ilustrativo embutido (cláusula de não-concorrência abusiva) e despacha automaticamente.

### Modo real — caso multidomínio

```bash
python agent.py --task "Tive um acidente em horário de trabalho e meu chefe não quer abrir CAT. Posso forçar?" --verbose
```

O orquestrador identifica clínico + jurídico, despacha duas vezes e consolida em parecer único.

### Apertando o orçamento

```bash
python agent.py --task "..." --max-fan-out 1
```

Limita a UMA chamada de especialista por execução. Em multidomínio, força o orquestrador a escolher o domínio mais crítico OU devolver parecer parcial.

---

## Exemplos prontos

| Exemplo | O que demonstra |
|---|---|
| [`exemplos/exemplo-01-juridico.md`](./exemplos/exemplo-01-juridico.md) | Despacho único ao especialista jurídico trabalhista (caso de cláusula CLT) |
| [`exemplos/exemplo-02-multidominio.md`](./exemplos/exemplo-02-multidominio.md) | Despacho duplo (clínico + jurídico) numa consulta integrada de acidente de trabalho |
| [`exemplos/exemplo-03-fora-de-escopo.md`](./exemplos/exemplo-03-fora-de-escopo.md) | Recusa explícita sem despacho (consulta sobre investimento financeiro, fora dos domínios atendidos) |

---

## Anatomia da pasta

```
a03-orquestrador-especialistas/
├── README.md                       ← este arquivo
├── agent.py                        ← entry point (CLI + loop do orquestrador)
├── especialistas.py                ← wrappers que viram prompts em tools
├── system_prompt_orquestrador.md   ← constituição do coordenador
├── exemplos/
│   ├── exemplo-01-juridico.md
│   ├── exemplo-02-multidominio.md
│   └── exemplo-03-fora-de-escopo.md
├── kill_switch.py                  ← parada testável em <30s
└── requirements.txt                ← anthropic>=0.40.0
```

---

## A escolha arquitetural: estrela, não pipeline

A escolha de padrão **estrela** em vez de pipeline sequencial é deliberada:

- **Estrela** = um orquestrador no centro chamando N especialistas em paralelo (ou sequência curta), com consolidação centralizada num único ponto auditável.
- **Pipeline** = fluxo linear A→B→C→D em que cada etapa só vê o output da anterior.

Estrela ganha quando as subtarefas são **independentes** (clínico não depende de jurídico para responder), quando o consolidador precisa **comparar respostas** (e não apenas encadear), e quando se quer **paralelismo real**. Pipeline ganha quando há dependência sequencial forte (e o output de B é input de C). Em produção, é comum compor — pipeline interno em cada especialista, estrela no orquestrador.

**Padrões mais sofisticados** — debate adversarial, grafos com ciclos, hierarquia profunda — ficam para o A04 (debate) e expansões futuras. Cada nível de sofisticação compra capacidade, mas custa observabilidade. Começar simples e subir quando o ROI justificar é a regra dura do F3.

---

## Por que reusar prompts em vez de definir inline

A escolha de reusar prompts profissionais de `/prompts/<id>/` em vez de definir prompts ad hoc dentro do agente é a aplicação da **Camada Dupla** ao código:

- **O prompt é ativo durável** versionado em `/prompts/<id>/`, com golden set, eval config, changelog e calibração editorial. Sobrevive à troca de modelo.
- **O agente é o consumidor descartável** que orquestra os ativos. Pode ser refatorado, reescrito ou substituído sem perda.

Mudar a versão do prompt (P-LEG-01 v1.0 → v1.1) **não exige refatorar este arquivo**. O golden set associado ao prompt continua valendo como eval, e a calibração editorial registrada em `/prompts/<id>/golden.yaml` continua sendo a fonte de verdade.

A simplificação assumida nesta versão pedagógica: `especialistas.py` carrega uma **constituição resumida** de cada prompt em código, em vez de carregar o XML completo de `/prompts/<id>/prompt.xml` (que pode ter centenas de linhas). Essa separação é deliberada — o agente foca no padrão estrela; o pipeline de regressão foca no eval completo. As duas camadas vivem em paralelo.

---

## Conexão com o livro

- 🔗 [**Capítulo 12 — Agentes de IA**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md) — seção sobre padrões multiagente
- 🔗 [**Capítulo 14C — Spec-Driven Development**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C14C-spec-driven-development.md) — o system prompt do orquestrador é, em essência, uma spec executável
- 🔗 [**Framework F3 — Escala de Propriedade**](../../../Livro-1-Os-Invariantes/03-frameworks/L1-F3-agente-prop.md) — este agente opera em nível Supervisionado
- 🔗 [**Framework F7 — Custo Composto**](../../../Livro-1-Os-Invariantes/03-frameworks/L1-F7-custo-composto.md) — fan-out limit aplica a alavanca de Tier ao multiplicador de chamadas
- 🔗 [**Pasta `/prompts`**](../../prompts/) — fonte dos especialistas reusados (P-LEG-01, P-MED-01, P-SUP-01)
- 🔗 [**A01 ReAct Simples**](../a01-react-simples/) — fundação que este agente herda

---

## Próximo passo

Depois de rodar A03 nos três exemplos, vá para [**A04 — Multiagente Debate**](../a04-multiagente-debate/), onde dois agentes adversariais defendem teses opostas e um juiz, integrado ao pipeline de `/evals`, decide. Você sai sabendo a diferença entre o padrão **cooperativo** deste A03 (todos remam pro mesmo lado) e o padrão **adversarial** do A04 (a tensão entre os agentes é o produto).

---

> *"Multiagente não é um modelo melhor; é um modelo estruturado em conversa entre agentes com competências distintas. Quem entender essa diferença para de comprar 'o agente que faz tudo' e começa a construir o sistema que separa o que sabe do que não sabe — e despacha cada parte para quem efetivamente pode responder."*
