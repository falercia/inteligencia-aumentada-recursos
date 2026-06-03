# `/mcp` — Servidores MCP Educacionais

> **Aplicação rodável do Capítulo 13 (MCP — Model Context Protocol).** Cada servidor desta pasta é mínimo, auditável, e demonstra de forma direta como conectar uma IA a sistemas reais sem reescrever integração a cada novo cliente.

---

## Para quem é esta pasta

| Se você é... | Vai sair daqui com... |
|---|---|
| **CTO ou arquiteto** avaliando se MCP cabe na sua stack | Servidor mínimo rodando em quinze minutos, ligado ao Claude Desktop, mostrando os três conceitos centrais — Resources, Tools, Prompts — sem mistério de framework. |
| **AI Engineer** que precisa expor um sistema interno para a IA | Esqueleto de código que você adapta direto, com política de autenticação separada do código de negócio. |
| **Time de segurança** validando proposta de adoção de MCP | Demonstração instrumentada de auditoria por chamada, escopo de permissão por Tool, e padrão de sandboxing para Resources. |
| **Curioso técnico** que ouviu falar em MCP em mil reuniões | Em uma sessão você entende por que MCP virou o USB-C da IA, e por que servidor próprio é a alavanca real, não cliente bonito. |

---

## Que problema MCP resolve, em uma página

Antes do MCP, conectar uma IA generativa ao seu sistema interno exigia uma das três opções, e nenhuma escalava bem.

1. **Integração ponto-a-ponto por cliente** — escrever um adapter para cada cliente de IA que sua organização adotasse. ChatGPT, Claude, Gemini, Cursor, cada um exigia seu plugin próprio. Manutenção viraria pesadelo em três trimestres.
2. **API pública genérica** — expor o sistema interno como REST/GraphQL e esperar que cada IA descobrisse como usar. Custoso, inseguro, e cada cliente precisaria de prompt engineering específico para chamar a API direito.
3. **Tudo via prompt** — colar o conteúdo do sistema no prompt manualmente, copiando e colando. Não escala, não tem auditoria, perde contexto rápido.

**MCP propõe a quarta opção:** um protocolo padrão entre IA e sistemas, em que o servidor expõe **Resources** (dados para leitura), **Tools** (ações com efeito) e **Prompts** (templates reutilizáveis), e qualquer cliente que falar MCP consegue usar — sem código novo do lado do servidor para cada cliente. É o USB-C da IA: um conector padrão, fornecedores diferentes, compatibilidade transparente.

Os dois servidores desta pasta materializam o protocolo:

- **M01 (hello-world)** te mostra o esqueleto mínimo com um Resource, uma Tool e um Prompt — código que cabe em uma tela e que você lê em dez minutos.
- **M02 (biblioteca interna)** mostra o caso real que mais aparece em empresa: um servidor que expõe a biblioteca de prompts profissionais e o caderno de governança deste próprio repositório como Resources, e oferece Tools para listar, buscar e validar — pronto para qualquer cliente MCP da organização consumir.

---

## O que vive aqui

| Servidor | O que expõe | Quando usar | Status |
|---|---|---|---|
| [`m01-hello-world`](./m01-hello-world/) | 1 Resource (nota do dia), 1 Tool (criar nota), 1 Prompt (template de resumo) | Aprender o protocolo. Ponto de partida obrigatório. | ✅ Completo |
| [`m02-biblioteca-interna`](./m02-biblioteca-interna/) | Prompts de `/prompts` e arquivos de `/governance` como Resources; Tools para listar e buscar | Caso real de "servidor de conhecimento corporativo" que qualquer cliente MCP da organização consome | ✅ Completo |

---

## Como rodar

Os dois servidores funcionam de duas formas:

1. **Cliente de teste local em Python** (`client_test.py`) — não exige Claude Desktop, valida que o servidor responde corretamente, ideal para CI e para entender o protocolo.
2. **Cliente real (Claude Desktop)** — cada servidor inclui `claude_desktop_config.example.json` que você adapta e cola no seu config do Claude Desktop. Aí o servidor aparece como ferramenta dentro do app, e você usa em conversa normal.

Detalhes específicos no README de cada servidor.

---

## Regras inegociáveis desta pasta

A pasta opera sob quatro regras que não são negociáveis, mesmo em educacional, e que reproduzem em código a disciplina que o Capítulo 13 ensina como prática.

1. **Toda Tool com efeito declara seu escopo de permissão** no docstring e no schema. Sem essa declaração, o cliente não tem como avaliar risco antes de chamar.
2. **Toda Resource lida do disco passa por validação de sandbox** (mesmo padrão da tool `file_reader` em `/agents/_common/tools/`). Nada de `open(arbitrary_path)`.
3. **Cada chamada do servidor é logada em JSONL local** com timestamp, método, parâmetros e tamanho da resposta. Em produção, troque por seu SIEM; em educacional, JSONL no diretório local.
4. **Configuração separada do código** — nenhum servidor faz hardcode de credencial, URL ou path. Tudo via env var documentada no README.

---

## Onde isto se conecta no livro

- 🔗 [**Capítulo 13 — MCP — Model Context Protocol**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C13-mcp.md) — fundação conceitual completa
- 🔗 [**Framework F5 — Matriz de Cobertura de Integrações**](../../Livro-1-Os-Invariantes/03-frameworks/L1-F5-cobertura-integracoes.md) — quando MCP vence outras alternativas (REST, webhook, RPC)
- 🔗 [**Capítulo 12 — Agentes de IA**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md) — agentes consomem servidores MCP como tools
- 🔗 [**Pasta `/prompts`**](../prompts/) — fonte que o M02 expõe como Resources

---

> *"O modelo conversa, o servidor age. MCP é o contrato entre os dois."*
