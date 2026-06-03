# `/agents` — Agentes de Referência Educacional

> **Aplicação rodável dos conceitos de agente do livro.** Cada agente aqui resolve um problema concreto e declara, em código, o nível de autonomia em que opera, os gates de promoção, o kill switch e o procedimento de rollback.

---

## Para quem é esta pasta

| Se você é... | Vai sair daqui com... |
|---|---|
| **CTO ou head de tecnologia** avaliando proposta de agente do seu time | Critério executivo para decidir em qual nível de autonomia o agente pode operar hoje, e o que falta para promover. A02 é a leitura obrigatória. |
| **AI Engineer** começando a construir agente de produção | Esqueleto de código que você lê em uma sessão e adapta direto: loop reasoning-acting, tracing JSONL, gates, kill switch, rollback documentado. |
| **Comitê de governança** validando se a operação aguenta um agente novo | Demonstração instrumentada de cada nível F3, com pré-condições explícitas e teste mensal de rollback rodável. |
| **Profissional de outra área** querendo entender o que é agente sem mistério | A01 em modo seco (sem gastar token) mostra na tela a diferença entre chatbot e agente em quinze minutos. |

---

## Por que esta pasta existe

A pasta carrega o que o Capítulo 12 ensina como conceito e o Framework F3 organiza como decisão. Em vez de descrever em abstrato como um agente funciona, o leitor abre o arquivo, lê o `system_prompt.md`, executa o `agent.py` em modo seco, e vê na prática o loop de raciocínio e ação. Quando estiver pronto para gastar token, configura a `ANTHROPIC_API_KEY` e roda contra a API real, com tracing local em JSONL que serve como insumo para o eval do próximo capítulo (C21).

A escolha de implementação é deliberada: **Python puro com o SDK oficial da Anthropic, sem framework de orquestração**. Frameworks como LangGraph, CrewAI e AutoGen são úteis para produção, mas escondem a mecânica do loop atrás de abstrações que envelhecem com cada release. Aqui o objetivo é o leitor entender a mecânica em código que ele consegue ler do começo ao fim em uma sessão, e que continua válido mesmo quando o framework do trimestre for substituído. Camada Dupla aplicada à própria escolha de stack.

---

## O que vive aqui

| Agente | Padrão | Nível F3 demonstrado | Status |
|---|---|---|---|
| [`a01-react-simples`](./a01-react-simples/) | ReAct (Reasoning + Acting em loop) | Co-piloto (executa com confirmação) | ✅ Completo |
| [`a02-escala-propriedade`](./a02-escala-propriedade/) | Mesmo agente em 4 níveis F3 | Assistente → Co-piloto → Supervisionado → Autônomo regulado | ✅ Completo |
| [`a03-orquestrador-especialistas`](./a03-orquestrador-especialistas/) | Multiagente em estrela, reusa prompts de `/prompts` | Supervisionado | 🚧 Stub |
| [`a04-multiagente-debate`](./a04-multiagente-debate/) | Dois agentes argumentam, juiz decide | Supervisionado | 🚧 Stub |

A separação entre **completo** e **stub** é declarada, conforme Princípio 5 (Honestidade Temporal). Cada stub tem `README.md` explicando o problema que resolve e o que vai entrar quando for implementado.

---

## Como cada agente está estruturado

```
agente-nome/
├── README.md           ← O que é, qual padrão, qual nível F3, como rodar
├── agent.py            ← Implementação Python (~100-200 LOC, comentada)
├── system_prompt.md    ← Constituição do agente em linguagem natural
├── tools/              ← Schemas das tools, com permissão por nível
├── exemplos/           ← Casos rodáveis de entrada e saída esperada
└── kill_switch.py      ← Como desligar o agente em menos de 30 segundos
```

A estrutura é a mesma para todos os agentes desta pasta. Quem entendeu um, leu o esqueleto dos outros. Quem está construindo o próprio agente da empresa copia o esqueleto e adapta.

---

## O esqueleto compartilhado (`_common/`)

Para evitar repetir infraestrutura básica em cada agente, três peças vivem em `_common/`:

| Arquivo | Função |
|---|---|
| `_common/anthropic_client.py` | Wrapper fino do SDK oficial, com leitura de `ANTHROPIC_API_KEY` por env var e modo seco (dry-run) que imprime a chamada sem executar |
| `_common/tracing.py` | Tracing local em JSONL, sem dependência externa, escrevendo cada chamada do agente com input, output, tokens, latência e custo estimado. Serve como input para `/evals` |
| `_common/tools/` | Tools compartilhadas e seguras para rodar local: `calculator` (eval matemático seguro), `file_reader` (leitura limitada a `./data/`), `fake_web_search` (resultados canned para demonstração sem internet) |

Quem estiver construindo o próprio agente da empresa pode trocar `_common/` por sua infraestrutura interna sem mexer no código dos agentes em si.

---

## Como rodar em 60 segundos

```bash
# A partir da raiz do repositório
cd agents/a01-react-simples

# Instalar dependências mínimas
pip install -r requirements.txt

# 1. Modo seco — imprime as chamadas que faria, sem gastar token
python agent.py --dry-run --task "Calcule 18% de R$ 12.450 e me diga se ultrapassa R$ 2.000"

# 2. Modo real — exige ANTHROPIC_API_KEY configurada
export ANTHROPIC_API_KEY="sua-chave-aqui"
python agent.py --task "Calcule 18% de R$ 12.450 e me diga se ultrapassa R$ 2.000"
```

Cada agente tem um conjunto de exemplos prontos em `exemplos/`, com a saída esperada documentada. Rode os exemplos primeiro; só depois invente sua própria task.

---

## Regras inegociáveis desta pasta

A pasta opera sob cinco regras que não são negociáveis em nenhum agente desta biblioteca, e que reproduzem em código o que o livro ensina como prática. Quem vai adaptar para a empresa precisa manter as cinco, mesmo que adapte a stack inteira.

1. **Todo agente declara o nível F3 em que opera**, e o nível está nomeado no `README.md` da pasta. Pular essa declaração é violar a primeira regra do F3.
2. **Todo agente declara um dono humano nominal** no `README.md`. Em ambiente educacional o dono é "o leitor que está executando"; em produção é nome e cargo. Princípio 8 — Responsabilidade Indelegável.
3. **Tracing por chamada é ativado por padrão**, escrito em JSONL local. Quem quer desligar precisa passar flag explícita. Princípio 7 — Termômetro.
4. **Kill switch existe e é testável** em todo agente, com tempo de resposta declarado e teste rodável incluído. Princípio 6 — Autonomia Proporcional.
5. **Rollback documentado e testado** quando o agente tem efeito colateral. Em agentes educacionais sem efeito colateral, esta regra fica explicitamente marcada como "não aplicável" no `README.md`, em vez de omitida.

---

## Onde isto se conecta no livro

- 🔗 [**Capítulo 12 — Agentes de IA**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md) — fundação conceitual: anatomia, padrões, níveis de autonomia
- 🔗 [**Capítulo 14C — Spec-Driven Development**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C14C-spec-driven-development.md) — quando o agente gera código, opera sob disciplina de spec executável
- 🔗 [**Capítulo 22 — LLMOps**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C22-llmops.md) — operação de agentes em produção: observabilidade, gates, deploy progressivo
- 🔗 [**Framework F3 — Escala de Propriedade do Agente**](../../Livro-1-Os-Invariantes/03-frameworks/L1-F3-agente-prop.md) — a matriz que cada agente desta pasta instancia em código
- 🔗 [**Framework F4 — Engenharia de Prompt Estendida**](../../Livro-1-Os-Invariantes/03-frameworks/L1-F4-prompt-ext.md) — anatomia do `system_prompt.md` de cada agente

---

> *"Autonomia sem rollback testado é passivo no balanço. Cada agente desta pasta declara, em código, o que se compromete a fazer e o que não promete."*
