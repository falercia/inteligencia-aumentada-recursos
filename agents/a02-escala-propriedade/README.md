# A02 — Escala de Propriedade do Agente (F3 em código)

> **Mesmo agente, mesma tarefa, quatro níveis de autonomia.** Quatro arquivos lado a lado, cada um implementando uma linha do Framework F3. Quem ler os quatro em sequência sente, no terminal, a diferença operacional entre Assistente, Co-piloto, Supervisionado e Autônomo Regulado — em vez de só ler a definição no livro.

---

## Que problema este agente resolve

A pergunta que toda diretoria faz quando o time apresenta uma proposta de agente é: **"e se ele errar?"**. A resposta honesta depende de uma decisão arquitetural que quase nunca é explícita: em qual dos quatro níveis de autonomia o agente vai operar, e quais são as pré-condições operacionais que o time precisa ter instaladas para sustentar aquele nível. **A02 resolve isso na prática.**

O caso de uso pedagógico aqui é **processar um cancelamento de assinatura SaaS B2B**: ler dados do cliente, rascunhar e-mail de confirmação, enviar o e-mail, atualizar o status da assinatura. Quatro ações com gradiente de risco — da leitura inofensiva à mudança de estado com efeito comercial real. Os quatro arquivos `nivel_*.py` rodam a mesma tarefa, mas a permissão e a fricção mudam: no nível 1 o agente só rascunha e devolve plano ao humano; no nível 2 cada ação com escrita pede aprovação no terminal; no nível 3 executa em lote com humano monitorando o trace; no nível 4 opera sem supervisão, mas só depois de cumprir gates explícitos (14 dias estáveis, zero incidentes, rollback testado, dono nominal aprovado).

**Para quem é útil:** o CTO que precisa avaliar maturidade real do time para subir um agente de nível; o head de produto que está negociando com a engenharia o trade-off entre velocidade e segurança; o time que vai apresentar para o comitê de governança a justificativa de promoção de autonomia; o auditor interno que precisa entender por que cada nível exige instrumentação diferente. É o agente que substitui a discussão filosófica de "agentes autônomos são perigosos" por uma conversa instrumentada sobre **qual nível concretamente seu time sustenta hoje, e o que falta para subir um degrau**.

**O experimento que cobra honestidade:** rode os quatro em sequência. Em qual nível você ficou desconfortável? Em qual você sentiu vontade de descer? A resposta vai surpreender — a maioria das organizações que dizem operar "agentes autônomos" está operando, na prática, no nível 3 mal instrumentado. F3 é o instrumento que torna essa diferença visível.

---

## Ficha técnica

| Campo | Valor |
|---|---|
| **Padrão** | Mesmo agente em 4 níveis F3 |
| **Tarefa de demonstração** | Processar pedido de cancelamento de assinatura SaaS B2B |
| **Tools** | `customer_lookup`, `draft_cancellation_email`, `simulate_send_email`, `update_subscription` |
| **Dono nominal** | O leitor que está executando |
| **Tracing** | Ativo por padrão em `./traces/` |
| **Kill switch** | `kill_switch.py` testável (mesmo padrão do A01) |
| **Rollback** | Aplicável a partir do nível 2 — `rollback.md` documenta o procedimento |
| **Efeito colateral real** | Nenhum — `simulate_send_email` escreve em `./outbox/`, não envia de verdade |

---

## Os quatro níveis em uma página

| Nível F3 | Arquivo | O que o agente faz sozinho | Onde o humano entra |
|---|---|---|---|
| **1 — Assistente** | `nivel_1_assistente.py` | Lê dados do cliente, rascunha e-mail e proposta de update da assinatura | Humano executa **todas** as ações (envio, update). Agente nunca toca o ambiente. |
| **2 — Co-piloto** | `nivel_2_copiloto.py` | Tudo do Assistente + executa cada ação individualmente | Humano aprova **cada ação** antes da execução (gate síncrono no terminal) |
| **3 — Supervisionado** | `nivel_3_supervisionado.py` | Tudo do Co-piloto + executa em lote sem confirmação por passo | Humano **monitora o trace em tempo real** e pode parar via kill switch |
| **4 — Autônomo Regulado** | `nivel_4_autonomo_regulado.py` | Executa em produção sem supervisão direta | Humano confere por **amostragem** e via **eval automatizado**; promoção exige gates explícitos |

Cada arquivo é **autocontido e legível em uma sentada**. Há alguma duplicação calculada entre eles, deliberada: é mais didático ler quatro arquivos com diferenças explícitas do que abstrair em uma classe parametrizada que esconde a diferença real entre níveis.

---

## A tarefa de demonstração

> Cliente Acme Industrial pediu cancelamento da assinatura SaaS no plano Enterprise. Processe o pedido: confirme o status, rascunhe e-mail de confirmação, atualize a subscription para cancelada ao fim do ciclo, registre tudo no histórico.

Esta tarefa foi escolhida porque tem **gradiente claro de risco**: ler dados do cliente é leitura pura (risco zero), rascunhar e-mail é texto descartável (risco baixo), enviar e-mail é comunicação externa (risco médio, compensável), atualizar status da subscription é mudança de estado (risco alto, compensável com fricção). Os quatro níveis instanciam, em código, a regra de F3: a autonomia que o agente recebe é exatamente a que o operador consegue medir e desfazer no contexto.

---

## Como rodar

### Modo seco para entender a mecânica

```bash
# Cada nível em modo seco
python nivel_1_assistente.py --dry-run
python nivel_2_copiloto.py --dry-run
python nivel_3_supervisionado.py --dry-run
python nivel_4_autonomo_regulado.py --dry-run
```

### Modo real (consome token)

```bash
export ANTHROPIC_API_KEY="sua-chave"
python nivel_1_assistente.py        # roda direto, agente só rascunha
python nivel_2_copiloto.py          # pede confirmação a cada ação
python nivel_3_supervisionado.py    # executa em lote, monitorar em outro terminal
python nivel_4_autonomo_regulado.py # exige gate de promoção aprovado (gates.py)
```

### Testar o kill switch

```bash
python kill_switch.py status
python kill_switch.py kill
# Em outro terminal: rode o nivel_3 — ele deve parar no início.
python kill_switch.py revive
```

### Testar o gate de promoção (nível 4)

```bash
python gates.py status         # mostra estado atual dos gates
python gates.py simulate-day   # simula um dia de operação e atualiza gates
python gates.py promote        # tenta promover para nível 4; falha se gates não estiverem ok
```

---

## O experimento do leitor

A leitura útil deste agente é **rodar os quatro em sequência** e responder, sem consultar o livro:

1. Em qual nível você ficou desconfortável pela primeira vez?
2. Em qual nível você sentiu vontade de descer (rebaixar)?
3. Quais das quatro tools você jamais delegaria ao nível 4 na sua organização atual? Por quê?
4. Quanto custou cada nível em tokens? (`Tracer.summary()` no fim de cada execução)

O ponto de F3 não é "qual nível é melhor" — é "qual é o nível **máximo defensável dado a observabilidade e a reversibilidade que você efetivamente tem instaladas hoje**". Se você se assustou com o nível 4, ele provavelmente não está pronto para a sua organização — e isso é exatamente a informação que o F3 entrega.

---

## Os arquivos

| Arquivo | Função |
|---|---|
| `system_prompt_base.md` | Constituição compartilhada pelos quatro níveis (o agente é o mesmo; só muda o contrato de execução) |
| `tools_simuladas.py` | Quatro tools que reproduzem o padrão de risco crescente (read-only → write com efeito) |
| `nivel_1_assistente.py` | Implementação do Assistente (sem efeito colateral) |
| `nivel_2_copiloto.py` | Implementação do Co-piloto (gate síncrono por ação) |
| `nivel_3_supervisionado.py` | Implementação do Supervisionado (lote + monitoramento de trace) |
| `nivel_4_autonomo_regulado.py` | Implementação do Autônomo Regulado (sem gate por ação; com gates de promoção e kill switch verificado a cada iteração) |
| `gates.py` | Lógica e CLI dos gates de promoção entre níveis |
| `kill_switch.py` | Switch testável de parada em <30s |
| `rollback.md` | Procedimento testado de rollback para níveis 2-4 |
| `exemplos/comparativo.md` | Mesma tarefa rodada nos quatro níveis, lado a lado |

---

## Conexão com o livro

- 🔗 [**Framework F3 — Escala de Propriedade**](../../../Livro-1-Os-Invariantes/03-frameworks/L1-F3-agente-prop.md) — fundação direta deste agente
- 🔗 [**Capítulo 12 — Agentes de IA**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md) — anatomia dos níveis canônicos
- 🔗 [**Capítulo 22 — LLMOps**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C22-llmops.md) — operação dos níveis 3 e 4 em produção
- 🔗 [**Capítulo 24 — Governança**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C24-governanca.md) — o nível 4 só é defensável com governança nominal (Invariante 8)

---

> *"Autonomia sem rollback testado é passivo no balanço. Este agente faz a tese caminhar em quatro arquivos: leia os quatro, escolha qual sua organização suporta hoje, e instale o que falta para subir um nível."*
