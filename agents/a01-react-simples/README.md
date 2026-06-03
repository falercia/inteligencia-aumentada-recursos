# A01 — ReAct Simples

> **O hello-world dos agentes.** Loop canônico de **Reasoning + Acting** em ~150 linhas de Python puro, com três tools educacionais. Quem entende este agente entende o esqueleto que todos os outros desta biblioteca compartilham.

---

## Que problema este agente resolve

Você é executivo, AI Engineer ou desenvolvedor que já ouviu falar em "agente de IA" em mil reuniões, leu o termo em cinco artigos diferentes, e ainda não consegue defender em três frases o que separa um agente de um chatbot avançado. **A01 resolve isso na prática.** Em quinze minutos lendo o código e rodando em modo seco, você vê na tela a diferença concreta entre "modelo que responde" e "modelo que pensa, age e observa o resultado em loop".

O caso de uso clássico desta categoria: você tem uma tarefa que envolve **cálculo exato, consulta a documento local e referência a fonte externa**, tudo em um único pedido. Um chatbot tentaria fazer mentalmente (e erra na conta), ou pediria que você quebrasse em três perguntas separadas. Um agente ReAct decide sozinho qual ferramenta usar para cada parte, executa em sequência, e devolve uma resposta única com cada número justificado pela ferramenta que o produziu.

**Para quem é útil:** o desenvolvedor que vai construir um agente de produção e precisa entender o motor antes de adotar framework; o CTO que vai aprovar uma proposta de agente da equipe e precisa avaliar se a complexidade prometida está justificada; o profissional curioso que quer parar de operar com mistério.

**O que você sai sabendo após rodar:** como o loop reasoning-acting realmente funciona, o que é um gate humano e quando ele protege, como ler um trace JSONL para auditar o que o agente fez, qual é o custo composto de uma tarefa simples em tokens reais.

---

## Ficha técnica

| Campo | Valor |
|---|---|
| **Padrão** | ReAct — Reasoning and Acting in Language Models |
| **Nível F3 declarado** | Co-piloto (executa com confirmação opcional via `--gate`) |
| **Tools disponíveis** | `calculator`, `file_reader` (sandboxed em `./data/`), `fake_web_search` (canned) |
| **Dono nominal** | O leitor que está executando |
| **Tracing** | Ativo por padrão em `./traces/trace-*.jsonl` |
| **Kill switch** | Ctrl+C; ou flag `--max-iterations N` |
| **Rollback** | Não aplicável — agente não tem efeito colateral externo |
| **Custo estimado** | Tarefas simples: ~0,01 USD por execução com Sonnet; modo seco: zero |

---

## Por que ReAct?

ReAct é o padrão fundador que mostra, em uma única arquitetura, como um modelo de linguagem alterna entre raciocinar sobre o problema e agir sobre o ambiente por meio de tools. O loop é simples e tem três fases por iteração:

1. **Reason** — o modelo recebe a tarefa e o histórico, e pensa no próximo passo.
2. **Act** — o modelo pede a execução de uma tool com os parâmetros que decidiu.
3. **Observe** — a tool executa, o resultado volta como nova mensagem, e o ciclo recomeça.

O agente para quando o modelo decide responder em texto puro, sem pedir nova tool. Em produção, há ainda gates de promoção, kill switch e timeout, mas a mecânica básica é só isso. Quem entende o `agent.py` deste diretório do começo ao fim, em uma sessão, entendeu o motor que está sob qualquer framework de orquestração que vier depois.

---

## Como rodar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Modo seco (sem gastar token, ideal para estudar a mecânica)

```bash
python agent.py --dry-run --task "Calcule 18% de R$ 12.450"
```

A saída mostra cada iteração do loop, qual tool seria chamada, e qual mensagem seria enviada ao modelo. Use este modo para ler o código com `agent.py` aberto em outra janela e acompanhar o fluxo.

### Modo real (consome token)

```bash
export ANTHROPIC_API_KEY="sua-chave"
python agent.py --task "Calcule 18% de R$ 12.450 e me diga se ultrapassa R$ 2.000"
```

### Modo com gate humano (Co-piloto F3 estrito)

```bash
python agent.py --task "..." --gate
```

Antes de cada execução de tool, o agente para e pede confirmação no terminal. Aceitar com `y`, recusar com `n`. Usar quando estiver testando contra ambiente com efeito colateral.

### Modo verboso

```bash
python agent.py --task "..." --verbose
```

Imprime cada chamada de tool e o resultado, em vez de só a resposta final.

---

## Exemplos prontos

| Exemplo | O que demonstra |
|---|---|
| [`exemplos/exemplo-01-calculo.md`](./exemplos/exemplo-01-calculo.md) | Tool `calculator` em cálculo de porcentagem composto |
| [`exemplos/exemplo-02-pesquisa.md`](./exemplos/exemplo-02-pesquisa.md) | Tool `fake_web_search` em consulta com encaminhamento a fonte primária |
| [`exemplos/exemplo-03-leitura.md`](./exemplos/exemplo-03-leitura.md) | Tool `file_reader` lendo arquivo da sandbox `./data/` |

Cada exemplo tem a entrada exata, a saída esperada e a observação editorial sobre o que o leitor deve notar na execução.

---

## Anatomia do agent.py

```
┌─────────────────────────────────────────────────────────┐
│ main(): parse args, monta tools, chama AnthropicClient  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ AnthropicClient.run_agent(): loop principal             │
│                                                         │
│   while iteration < max_iterations:                     │
│       response = call_api(messages, tools)              │
│       if stop_reason == "end_turn":                     │
│           return response.text                          │
│       for tool_call in response.tool_uses:              │
│           if gate and not human_approves(tool_call):    │
│               result = "bloqueado"                      │
│           else:                                         │
│               result = execute_tool(tool_call)          │
│           messages.append(tool_result)                  │
└─────────────────────────────────────────────────────────┘
```

O loop está em `_common/anthropic_client.py`. O `agent.py` deste diretório só monta tools, system prompt e chama o cliente. Quem quer entender o motor lê o cliente; quem quer entender este caso específico lê só este `agent.py`.

---

## Conexão com o livro

- 🔗 [**Capítulo 12 — Agentes de IA**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md) — fundação conceitual do padrão ReAct
- 🔗 [**Framework F3 — Escala de Propriedade**](../../../Livro-1-Os-Invariantes/03-frameworks/L1-F3-agente-prop.md) — este agente opera no nível Co-piloto, com gate humano opcional
- 🔗 [**Capítulo 9 — Engenharia de Prompt**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C09-engenharia-prompt.md) — anatomia do `system_prompt.md`
- 🔗 Yao, S., et al. *ReAct: Synergizing Reasoning and Acting in Language Models* (2022) — paper original

---

## Próximo passo

Quando estiver confortável com a mecânica deste agente, vá para [`a02-escala-propriedade`](../a02-escala-propriedade/), onde o mesmo agente é instanciado nos quatro níveis F3 lado a lado para você experimentar na pele a diferença operacional entre Assistente, Co-piloto, Supervisionado e Autônomo regulado.
