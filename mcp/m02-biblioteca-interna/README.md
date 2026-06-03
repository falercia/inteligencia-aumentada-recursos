# M02 — Biblioteca Interna MCP

> **Servidor MCP que entrega prompts profissionais versionados e caderno de governança a qualquer cliente da organização.** Reusa `/prompts` e `/governance` deste mesmo repositório como fonte da verdade — o servidor não duplica conteúdo, só serve.

---

## Que problema este servidor resolve

Toda organização que adota IA com seriedade chega ao mesmo problema operacional dentro de seis meses: **prompts profissionais e políticas de governança ficam espalhados em Notion, Confluence, Drive, Slack, na cabeça de uma pessoa, e em um README de algum repo perdido.** Cada AI Engineer reinventa o prompt de revisão jurídica. Cada equipe nova de produto reescreve a constituição de copiloto. O caderno de governança fica em PDF não pesquisável. A consistência morre na primeira renovação de time.

**M02 resolve isso entregando uma fonte única, versionada e legível por qualquer cliente MCP da organização.** O servidor expõe:

- **Cada prompt profissional da pasta `/prompts` como Resource** — `prompt://P-LEG-01/manifest`, `prompt://P-MED-01/manifest`, etc. Qualquer Claude Desktop, Cursor ou agente customizado da empresa lê do mesmo lugar.
- **Cada seção do caderno de governança como Resource** — `governance://accountability-raci`, `governance://politica-incidente`, etc. Auditor abre Claude Desktop, pede "me mostre a política de incidente", o cliente lê via MCP e devolve, com a versão.
- **Tools para buscar e listar** — `list_prompts(domain="juridico")`, `search_governance("LGPD")`. O usuário descobre o que existe sem precisar navegar pelo filesystem.
- **Um Prompt template** — `apply_prompt_to_task` — que carrega um prompt profissional e o aplica a uma tarefa específica, com o cliente preenchendo os campos.

**Para quem é útil:** times de AI Engineering que querem padronizar prompts entre squads; áreas de governança que precisam tornar o caderno acessível dentro da própria IA; arquitetos que querem mostrar à diretoria como MCP elimina silos sem migração massiva; auditores internos que precisam consultar política durante uma revisão sem trocar de aba.

**O caso ilustrativo desta entrega:** o AI Engineer da fintech está revisando um caso de contratos. Em vez de procurar o prompt P-LEG-01 no Confluence, ele pergunta ao Claude Desktop: *"Liste prompts jurídicos disponíveis"*. O Claude chama `list_prompts(domain="juridico")` via MCP, devolve a lista, o engenheiro escolhe `P-LEG-01`, e pede *"Aplique o P-LEG-01 a este contrato em anexo"*. O Claude lê o Resource `prompt://P-LEG-01/manifest`, monta a constituição, e processa o documento — tudo com a mesma versão que o time inteiro está usando.

---

## Ficha técnica

| Campo | Valor |
|---|---|
| **SDK** | `mcp` (oficial Anthropic) |
| **Transporte** | stdio |
| **Resources expostos** | Dinâmicos — um por prompt em `/prompts` + um por arquivo `.md` em `/governance/v1/` |
| **Tools expostas** | `list_prompts(domain)`, `search_governance(term)` |
| **Prompts expostos** | `apply_prompt_to_task` (template para o cliente carregar prompt e aplicar a uma tarefa) |
| **Sandbox** | Leitura limitada às pastas `prompts/` e `governance/v1/` do repo |
| **Auditoria** | Cada chamada gera linha JSONL em `./traces/mcp-m02-*.jsonl` |

---

## Como rodar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

O servidor lê dois diretórios relativos à raiz do repo, então você precisa configurar a env var apontando para onde o repositório está:

```bash
export REPO_ROOT="/caminho/absoluto/para/inteligencia-aumentada-recursos"
```

### Modo 1 — Cliente de teste local

```bash
python client_test.py
```

A saída lista todos os Resources expostos (prompts e seções de governança), chama `list_prompts` com filtro por domínio, chama `search_governance` por termo, e lê um Resource específico. Valida que o servidor está enxergando os dois diretórios e respondendo corretamente.

### Modo 2 — Cliente real (Claude Desktop)

Copie `claude_desktop_config.example.json`, ajuste os paths absolutos do `server.py` e do `REPO_ROOT`, e cole no seu config do Claude Desktop. Reinicie. O servidor `biblioteca-interna` aparece como ferramenta. Em conversa, pergunte:

- *"Que prompts profissionais estão disponíveis na biblioteca?"* → ele chama `list_prompts()`
- *"Liste os prompts da área jurídica"* → `list_prompts(domain="juridico")`
- *"Me mostre a política de governança sobre incidentes"* → ele lê o Resource correspondente
- *"Aplique o prompt P-LEG-01 a este contrato"* → ele usa o Prompt `apply_prompt_to_task`

---

## Diferenças importantes em relação ao M01

| Aspecto | M01 (Hello World) | M02 (Biblioteca Interna) |
|---|---|---|
| Resources | 1 estático (`notes://today`) | Dinâmicos, descobertos do filesystem |
| Tools | 1 (`create_note`) | 2 (`list_prompts`, `search_governance`) |
| Estado | Escreve em `./notes/` local | Apenas leitura — sem efeito colateral |
| Sandbox | `./notes/` | `prompts/` + `governance/v1/` do repo |
| Caso de uso | Aprender o protocolo | Servir conhecimento corporativo real |
| Adoção real | Demonstração | Pronto para colocar em produção interna |

M01 ensina o protocolo. M02 mostra o padrão real que vai aparecer na sua organização. O código de M02 é o que você vai adaptar quando precisar expor `<sistema interno X>` para a IA na sua empresa.

---

## Onde adaptar para o seu caso

Se você quer expor outro sistema da sua organização, mude três coisas em `server.py`:

1. **O loader dos Resources** (função `_load_prompt_manifests` no código) — em vez de ler arquivos do filesystem, conecte ao seu CMS, banco, API interna.
2. **O schema das Tools** — adapte `list_prompts` e `search_governance` para os filtros e termos que fazem sentido no seu domínio.
3. **O Prompt template** — mude `apply_prompt_to_task` para o template padronizado da sua organização.

Tudo o mais (auditoria, transporte stdio, ciclo de vida do servidor, integração com Claude Desktop) continua igual. Esse é o ponto do MCP.

---

## Conexão com o livro

- 🔗 [**Capítulo 13 — MCP — Model Context Protocol**](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C13-mcp.md), seção sobre servidores corporativos
- 🔗 [**Framework F5 — Matriz de Cobertura de Integrações**](../../../Livro-1-Os-Invariantes/03-frameworks/L1-F5-cobertura-integracoes.md), onde MCP vence webhook e REST
- 🔗 [**Pasta `/prompts`**](../../prompts/) — fonte que este servidor expõe
- 🔗 [**Pasta `/governance`**](../../governance/) — fonte que este servidor expõe

---

> *"Servidor MCP próprio é a alavanca real da adoção. Cliente bonito é commodity."*
