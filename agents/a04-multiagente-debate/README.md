# A04 — Multiagente Debate

> **Multiagente adversarial.** Proponente defende tese A, oponente defende tese B, juiz decide contra rubrica estruturada integrável a `/evals`. A tensão entre os agentes é o produto — não há cooperação, e essa é a fonte da qualidade.

---

## Que problema este agente resolve

Toda decisão arquitetural não-trivial em IA tem mais de uma resposta razoável, e a escolha entre elas depende de exposição honesta dos trade-offs. **Quando o operador pergunta "qual a melhor opção?" para UM agente, recebe a resposta enviesada pelo treinamento do modelo** — RAG vence quase sempre, fine-tuning é apresentado como complemento, deploy próprio é descrito como "para quem tem capacidade". A pergunta certa quase nunca é "qual a melhor"; é "quais os trade-offs concretos no MEU contexto, e qual posição sustenta o escrutínio adversarial".

A solução amadora é "pesquisar mais" — ler dois artigos, ouvir um podcast, perguntar a um colega. A solução madura é **debate adversarial estruturado**: um proponente defende a tese A com o máximo de rigor, um oponente defende a tese B com o mesmo rigor, um juiz arbitra contra rubrica explícita. A qualidade da decisão sobe materialmente, porque os pontos fracos de cada tese aparecem sob ataque honesto, e os pontos cegos comuns aos dois aparecem no parecer do juiz.

**A04 resolve isso na prática.** Três agentes com system prompts distintos, integração ao pipeline de `/evals` via rubrica em `eval_config.json`, transcript completo gravado em `outbox/` para auditoria posterior.

**Para quem é útil:** o CTO que precisa decidir RAG vs fine-tuning para um produto crítico; o comitê de arquitetura que está dividido entre deploy próprio e API e quer instrumentar a discussão; o time de produto que precisa apresentar trade-off honesto ao conselho em vez de pitch enviesado; o auditor interno que precisa documentar por que UMA opção foi escolhida sobre a outra com critério defensável.

**O que você sai sabendo após rodar:** como funciona o padrão adversarial em código, por que steel-manning (atacar a versão FORTE do adversário) é critério editorial não-negociável, como integrar judge LLM a uma rubrica em JSON, e por que empate técnico honesto é decisão legítima do juiz — mais defensável do que vitória forçada.

---

## Ficha técnica

| Campo | Valor |
|---|---|
| **Padrão** | Multiagente adversarial (proponente × oponente + juiz) |
| **Nível F3 declarado** | Supervisionado (sem efeito colateral; output é parecer escrito) |
| **Modelo dos três agentes** | Sonnet (default) — debate exige raciocínio, juiz exige calibração |
| **Dono nominal** | O leitor que está executando |
| **Tracing** | Ativo por padrão em `../_common/traces/` |
| **Kill switch** | `kill_switch.py` testável (padrão A01/A02/A03) |
| **Persistência do debate** | Transcript JSON em `outbox/debate-*.json` por execução |
| **Rubrica de arbitragem** | `eval_config.json` (5 critérios ponderados; integrável a `/evals`) |
| **Custo estimado** | 1 rodada: ~0,04 USD com Sonnet; 2 rodadas: ~0,08 USD |

---

## Como rodar

### Pré-requisitos

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"
```

### Modo seco

```bash
python agent.py --dry-run
```

Em dry-run, cada agente devolve resposta simulada. Use com `agent.py` aberto para entender o fluxo proponente → oponente → juiz sem gastar token.

### Modo real — caso default (RAG vs fine-tuning, escritório jurídico de M&A)

```bash
python agent.py --verbose
```

O agente carrega a pergunta default (M&A com 50 advogados, 20 mil docs, citação verificável), tese A pró-RAG, tese B pró-fine-tuning. Em ~30 segundos o debate inteiro acontece em 1 rodada com parecer arbitral.

### Modo real — caso customizado

```bash
python agent.py \
  --question "Sua pergunta aqui" \
  --thesis-a "Tese A" \
  --thesis-b "Tese B" \
  --rounds 2 \
  --verbose
```

`--rounds 2` adiciona uma rodada extra de réplica + tréplica. Cada rodada extra adiciona ~50% de custo; o ganho marginal cai rápido depois da segunda.

---

## Exemplos prontos

| Exemplo | O que demonstra |
|---|---|
| [`exemplos/exemplo-01-rag-vs-finetuning.md`](./exemplos/exemplo-01-rag-vs-finetuning.md) | Debate canônico em contexto bem definido — caso em que o proponente tende a vencer com folga |
| [`exemplos/exemplo-02-modelo-proprio-vs-api.md`](./exemplos/exemplo-02-modelo-proprio-vs-api.md) | Caso borderline em fintech regulada — empate técnico honesto com recomendação prática faseada |
| [`exemplos/exemplo-03-agente-autonomo-vs-supervisionado.md`](./exemplos/exemplo-03-agente-autonomo-vs-supervisionado.md) | Decisão de promoção F3 com gates próximos do limiar — exemplo de quando o "ponto cego" do juiz importa mais que a decisão final |

---

## Anatomia da pasta

```
a04-multiagente-debate/
├── README.md                            ← este arquivo
├── agent.py                             ← orquestra o debate (proponente → oponente → juiz)
├── system_prompt_proponente.md          ← constituição do defensor da tese A
├── system_prompt_oponente.md            ← constituição do contraditor (tese B)
├── system_prompt_juiz.md                ← constituição do árbitro editorial
├── eval_config.json                     ← rubrica com 5 critérios ponderados (integrável a /evals)
├── exemplos/
│   ├── exemplo-01-rag-vs-finetuning.md
│   ├── exemplo-02-modelo-proprio-vs-api.md
│   └── exemplo-03-agente-autonomo-vs-supervisionado.md
├── outbox/                              ← transcripts gravados por execução
├── kill_switch.py
└── requirements.txt
```

---

## Por que adversarial, não cooperativo

A diferença entre **estrela cooperativa** (A03) e **debate adversarial** (A04) é a fonte da qualidade:

- **Cooperativa** = especialistas em domínios DIFERENTES, somando competências para um resultado integrado. O orquestrador consolida sem tensão. Caso típico: triagem multidomínio (jurídico + clínico + suporte).
- **Adversarial** = agentes no MESMO domínio com posições OPOSTAS, expondo trade-offs sob pressão. O juiz arbitra. Caso típico: decisão arquitetural com mais de uma resposta razoável (RAG vs fine-tuning, API vs deploy, promover vs manter nível).

Tentar usar A03 onde A04 é certo (forçar consenso quando há trade-off real) esconde o conflito, e o conflito escondido reaparece em incidente depois. Tentar usar A04 onde A03 é certo (forçar adversarialidade onde há colaboração legítima) gera teatro retórico em vez de output útil. Saber qual padrão usar quando é parte da disciplina arquitetural que separa o operador maduro do entusiasta de multiagente.

---

## Integração com /evals

O `eval_config.json` deste agente é **compatível com o motor de evals** do repositório (`evals/eval_runner.py`):

1. **Judge `classification`** sobre decisão final ("Proponente vence" / "Oponente vence" / "Empate") permite medir concordância com humano sênior.
2. **Judge `llm-as-judge` calibrado** pode avaliar a nota por critério do parecer arbitral contra rubrica externa, com gate de qualidade em 0,75 de concordância.
3. **Golden set mínimo** de 20 debates calibrados por humano sênior em 3 verticais distintos (jurídico, financeiro, técnico) habilita a aceitação editorial do juiz como instrumento auditável.

A construção do golden set é o caminho natural de evolução do A04 — quem usar o agente em produção contribui debates calibrados de volta ao golden set público, e a qualidade do juiz sobe com a comunidade.

---

## Conexão com o livro

- 🔗 [**Capítulo 12 — Agentes de IA**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md) — fundação de padrões multiagente
- 🔗 [**Capítulo 21 — Evals**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C21-evals.md) — rubrica de arbitragem como caso de uso de LLM-as-judge
- 🔗 [**Capítulo 25 — Trade-offs Estratégicos**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C25-trade-offs.md) — o exercício do C25 é EXATAMENTE o que A04 instrumenta
- 🔗 [**Framework F8 — Pirâmide de Avaliação**](../../../Livro-1-Os-Invariantes/03-frameworks/L1-F8-piramide-aval.md) — `eval_config.json` aplica os três níveis da pirâmide
- 🔗 [**A03 Orquestrador-Especialistas**](../a03-orquestrador-especialistas/) — o par cooperativo deste padrão adversarial

---

> *"Decisão arquitetural sem debate é decisão por inércia. O proponente sozinho fala bem demais; o oponente sozinho ataca demais. Os dois juntos, sob arbitragem de critério explícito, expõem o trade-off real e devolvem ao operador a base para decidir como adulto — ou para reconhecer honestamente que faltam dados para decidir."*
