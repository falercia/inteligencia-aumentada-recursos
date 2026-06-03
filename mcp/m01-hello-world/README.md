# M01 — Hello World MCP

> **O esqueleto mínimo de um servidor MCP em Python.** Cinquenta linhas de código que demonstram os três conceitos centrais do protocolo: Resources, Tools e Prompts. Quem entende este servidor entende todos os outros — incluindo os de produção.

---

## Que problema este servidor resolve

Toda equipe que vai adotar MCP cai no mesmo ponto inicial: a documentação oficial é completa, mas começar do zero parece complicado. O time entra em paralisia, lê uma semana de spec, e ainda não escreveu uma linha. **M01 resolve isso** entregando o servidor mais simples possível que ainda demonstra os três conceitos centrais — Resource, Tool, Prompt — em código que cabe em uma tela e roda em quinze minutos.

O caso de uso pedagógico é deliberadamente trivial: um "caderno de notas pessoais" que expõe a nota do dia como Resource, oferece a Tool de criar uma nova nota, e disponibiliza um Prompt template de "resumir meu dia" para o cliente usar. Nada disso é o ponto. O ponto é o leitor sair sabendo:

- como declarar um Resource e como o cliente lê
- como declarar uma Tool e como o cliente chama
- como declarar um Prompt e quando isso é melhor que prompt-no-cliente
- como rodar localmente e como plugar no Claude Desktop
- como auditar cada chamada via tracing local

**Para quem é útil:** o desenvolvedor que vai construir o primeiro servidor MCP da empresa e quer ver o esqueleto antes de adaptar; o arquiteto que está avaliando se MCP é overkill ou se cabe na stack; o operador que quer entender como Claude Desktop consome o servidor antes de aprovar adoção.

---

## Ficha técnica

| Campo | Valor |
|---|---|
| **SDK** | `mcp` (oficial Anthropic) |
| **Transporte** | stdio (padrão para desenvolvimento local e Claude Desktop) |
| **Resources expostos** | 1 — `notes://today` (nota do dia em texto puro) |
| **Tools expostas** | 1 — `create_note` (cria nota em `./notes/`) |
| **Prompts expostos** | 1 — `summarize_my_day` (template de resumo executivo) |
| **Dependências** | Apenas `mcp>=1.0.0` (sem framework, sem ORM, sem nada além do SDK) |
| **Sandbox** | Todas as notas ficam em `./notes/` relativo ao processo. Sem escrita fora dessa raiz. |
| **Auditoria** | Cada chamada gera linha JSONL em `./traces/mcp-m01-*.jsonl` |

---

## Como rodar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Modo 1 — Cliente de teste local (não exige Claude Desktop)

```bash
python client_test.py
```

A saída mostra: ping do servidor, lista de Resources expostos, leitura da nota do dia, lista de Tools, execução da Tool `create_note`, lista de Prompts, e leitura do Prompt `summarize_my_day`. Bom para validar que o servidor está saudável antes de plugar em qualquer cliente real.

### Modo 2 — Cliente real (Claude Desktop)

Copie `claude_desktop_config.example.json` e adapte o path absoluto do `server.py` para o seu sistema. Depois cole no seu config do Claude Desktop:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Reinicie o Claude Desktop. O servidor `hello-world-notes` aparece como ferramenta disponível. Em conversa, peça: *"Que nota eu tenho de hoje?"* e o Claude vai chamar o Resource. Peça: *"Crie uma nota dizendo que terminei o capítulo 13"* e ele vai chamar a Tool.

---

## Anatomia rápida do `server.py`

```
┌──────────────────────────────────────────────┐
│ from mcp.server.fastmcp import FastMCP       │
│                                              │
│ mcp = FastMCP("hello-world-notes")           │
│                                              │
│ @mcp.resource("notes://today")               │  ← Resource: leitura
│ def get_today_note() -> str:                 │
│     return ...                               │
│                                              │
│ @mcp.tool()                                  │  ← Tool: ação com efeito
│ def create_note(text: str) -> str:           │
│     ...                                      │
│                                              │
│ @mcp.prompt()                                │  ← Prompt: template
│ def summarize_my_day() -> str:               │
│     return "..."                             │
│                                              │
│ if __name__ == "__main__":                   │
│     mcp.run()                                │
└──────────────────────────────────────────────┘
```

Cinquenta linhas, três decoradores, um runtime. É o coração do protocolo MCP.

---

## A diferença entre Resource, Tool e Prompt

Esta é a confusão mais comum entre quem está começando. Em uma linha cada:

- **Resource** — algo que o cliente lê. Sem efeito. Identificado por URI (`notes://today`, `db://customers/42`). Equivalente conceitual: `GET` em REST.
- **Tool** — algo que o cliente executa. Com efeito (ou capaz de ter). Identificada por nome (`create_note`, `send_email`). Equivalente conceitual: `POST/PUT/DELETE` em REST.
- **Prompt** — um template de mensagem que o servidor sugere ao cliente. O cliente pode usar para iniciar conversa ou para padronizar interações. Não existe em REST; é uma contribuição original do MCP.

Confundir Resource com Tool é o erro mais comum. Resource é leitura, Tool é ação. Quando a operação tem efeito colateral — escreve, envia, modifica — é Tool. Quando só lê, é Resource. O cliente trata os dois de forma diferente: Resource costuma ir para o contexto sem confirmação, Tool costuma pedir aprovação.

---

## Conexão com o livro

- 🔗 [**Capítulo 13 — MCP — Model Context Protocol**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C13-mcp.md), seções sobre Resources, Tools e Prompts
- 🔗 Documentação oficial: [modelcontextprotocol.io](https://modelcontextprotocol.io/)

---

## Próximo passo

Quando estiver confortável com a mecânica deste servidor, vá para [`m02-biblioteca-interna`](../m02-biblioteca-interna/), onde o mesmo padrão é aplicado a um caso real: expor a biblioteca de prompts profissionais e o caderno de governança deste repositório como Resources e Tools para qualquer cliente MCP da organização consumir.
