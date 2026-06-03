# A04 — Multiagente Debate (🚧 STUB)

> **Status atual: stub estrutural.** Implementação completa prevista para um release futuro. Este README declara o que vai entrar e por quê, conforme Princípio 5 — Honestidade Temporal.

---

## Que problema este agente vai resolver

Toda decisão executiva de alto risco — adotar IA em domínio sensível, conceder ou negar crédito automaticamente, escolher diagnóstico em medicina assistida, contratar ou demitir com auxílio de algoritmo — sofre do mesmo viés operacional: **a primeira resposta plausível tende a ser aceita**. O segundo argumento, o contraditório, o ponto cego, raramente aparece com força suficiente para mudar a decisão. Em humanos, isso é o que justifica órgão colegiado, comitê de risco, segunda opinião médica.

**A04 vai resolver isso em agentes** com o padrão debate adversarial: dois agentes argumentam de lados opostos (pró e contra), e um terceiro agente atua como juiz, decidindo com base na qualidade dos argumentos apresentados pelos dois lados. O resultado é uma recomendação com nuance, não com confiança vazia, e com auditabilidade de qual argumento ganhou peso.

**Caso de uso canônico que vai estar implementado:** decisão de adoção de triagem automatizada de currículos por IA, com pró-adoção argumentando ganho operacional, contra-adoção argumentando viés algorítmico e responsabilidade indelegável, e juiz consolidando a recomendação executiva. **Para quem vai ser útil:** comitês de IA, áreas de governança e compliance, conselhos de ética em IA, qualquer decisão que pareça óbvia mas mereça contraditório antes de virar política. Custa três vezes mais em tokens do que uma consulta simples — e por isso só vale para decisões em que o custo do erro paga essa conta com folga.

---

## O que este agente será

Padrão **debate adversarial**: dois agentes argumentam de lados opostos sobre uma mesma questão de alto risco, e um terceiro agente (juiz) decide com base na qualidade dos argumentos apresentados. O padrão é especialmente útil quando o custo do erro é alto e o ganho de uma segunda perspectiva crítica supera o custo extra de tokens.

A demonstração canônica vai ser uma decisão de adoção de IA em domínio sensível:

> A diretoria está avaliando substituir a triagem manual de currículos por um sistema de IA. Argumente a favor [agente Pró-adoção], argumente contra [agente Contra-adoção], e decida a recomendação executiva [juiz], considerando viés algorítmico, custo composto, responsabilidade indelegável e ganho operacional.

---

## Por que debate em vez de orquestrador

Debate é mais caro que orquestrador (no mínimo 3x o custo de tokens em comparação com uma chamada simples), e por isso só compensa quando:

1. **A questão é genuinamente controversa** — não tem resposta óbvia
2. **O custo do erro é alto** — decisão que afeta pessoas, balanço, compliance, direito de terceiros
3. **A organização tem capacidade de absorver a recomendação** — debate gera nuance, e nuance só ajuda quem decide com critério; quem decide por instinto vai ignorar a nuance e usar só a conclusão do juiz

O padrão é coberto na literatura por Du et al. (2023) *Improving Factuality and Reasoning in Language Models through Multiagent Debate* e ganhou tração na prática para decisões de alta consequência. A implementação aqui vai mostrar o padrão funcionando e os limites operacionais que ele tem.

---

## Estrutura prevista

```
a04-multiagente-debate/
├── README.md                       ← este arquivo
├── agent.py                        ← entry point com CLI
├── system_prompt_pro.md            ← constituição do agente pró
├── system_prompt_contra.md         ← constituição do agente contra
├── system_prompt_juiz.md           ← constituição do juiz
├── debate_loop.py                  ← lógica de turnos e parada
├── exemplos/
│   ├── caso-triagem-cv.md          ← decisão de adoção de IA em RH
│   ├── caso-medico-diagnostico.md  ← decisão clínica de alto risco
│   └── caso-credito.md             ← negação automática de crédito
├── eval/
│   └── golden-set.jsonl            ← validação contra decisões revisadas por humano
└── kill_switch.py
```

---

## Nível F3 esperado

**Supervisionado.** O resultado do debate é recomendação, não execução; a decisão final permanece com o humano em todos os exemplos. O kill switch existe para abortar o debate em qualquer rodada se o trace mostrar argumentação descambando para retórica vazia.

---

## Por que NÃO está pronto em v1.2.0

Quatro decisões de design precisam ser tomadas com cuidado:

1. **Quantas rodadas de debate antes de parar** (limites de qualidade vs. custo composto)
2. **Como evitar que os agentes se "alinhem" no meio do debate** (problema documentado: agentes que veem o argumento do outro tendem a convergir, perdendo o valor adversarial)
3. **Como o juiz declara que a decisão é insuficientemente clara** (em vez de forçar veredicto quando os dois lados têm mérito)
4. **Como capturar a nuance no resultado final** (sem virar relatório de 10 páginas que ninguém lê)

A integração com a pasta `/evals` deste repositório também vai exigir um eval de **calibração do juiz** — golden set onde a decisão correta é conhecida (por humano revisor) e o juiz é avaliado pela taxa de concordância. Isso é trabalho próprio, com cadência própria.

---

## Conexão com o livro (a ser ampliada no release final)

- 🔗 [Capítulo 12 — Agentes de IA](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md), seção sobre debate
- 🔗 [Capítulo 21 — Evals](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C21-evals.md) — calibração do juiz
- 🔗 [Capítulo 18 — Economia de Tokens](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C18-economia-tokens.md) — debate é caro; quando vale
- 🔗 Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., Mordatch, I. *Improving Factuality and Reasoning in Language Models through Multiagent Debate* (2023)

---

> *Stub é declaração honesta do que existe e do que ainda não existe. Debate adversarial é padrão útil em domínio certo; sem instrumentação de eval calibrado, é teatro caro. Por isso a implementação espera o ciclo que comporta o eval junto.*
