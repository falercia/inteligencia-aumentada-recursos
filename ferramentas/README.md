# Ferramentas e Stack · Catálogo Curado

> Atualizado em: 2026-06-16
> Próxima revisão: sem cadência fixa anunciada — conforme o ecossistema evolui
> Fonte primária: Apêndice D do livro *Inteligência Aumentada · Os Invariantes da IA* (Fabio Garcia, 2026)

---

## Por que este catálogo tem data e critério, não apenas inventário

Lista de ferramentas sem data é lista que já está envelhecendo no momento da publicação. Lista sem critério de escolha transfere ao leitor a responsabilidade de descobrir por que uma opção aparece antes da outra — que é exatamente o erro que este catálogo quer evitar.

A regra estrutural: cada ferramenta vem com nota de aplicação; cada categoria vem com critério recomendado de escolha e sinais de armadilha; a lista inteira carrega data de referência. O leitor que aplicar o critério antes de adotar a ferramenta toma decisão informada; o leitor que copiar a lista sem critério repete o erro que a Camada Dupla existe para evitar.

---

## Critério de seleção em seis dimensões

Para qualquer ferramenta desta lista — e para qualquer ferramenta que aparecer depois desta revisão —, recomenda-se avaliar nas seis dimensões abaixo. A avaliação não exige planilha sofisticada; vale anotação com nota de zero a dez por dimensão.

**Regra prática:** ferramenta abaixo de seis em qualquer dimensão crítica para o caso de uso é candidata duvidosa. Média ponderada abaixo de sete não compensa adoção.

| Dimensão | O que avaliar | Sinal de risco |
|---|---|---|
| **Maturidade** | Anos desde lançamento, versões estáveis, presença de LTS, frequência de breaking changes nos últimos doze meses | Menos de doze meses no mercado, breaking changes a cada release menor, sem LTS declarado |
| **Adoção** | Downloads mensais, estrelas no GitHub, contribuidores ativos nos últimos noventa dias, presença em rankings independentes | Tração baixa, contribuidor único, sem citação em pesquisa independente |
| **Custo** | Camada gratuita real (não trial), preço mensal em reais ou dólares, modelo de cobrança, tendência de preços nos últimos vinte e quatro meses | Camada gratuita inadequada para teste real, preço enterprise opaco, histórico de aumentos súbitos |
| **Encaixe com stack brasileira** | Suporte a português, integração com gateways nacionais (PIX, boletos), conformidade declarada com LGPD, presença comercial no Brasil | Sem suporte a português, sem documentação sobre LGPD, sem representação nacional |
| **Suporte** | Documentação em inglês ou português, comunidade ativa, SLA declarado em planos pagos, presença de comunidade BR | Documentação incompleta, fórum vazio, sem SLA explícito |
| **Estabilidade** | Cadência de releases, changelog público, histórico de breaking changes nos últimos doze meses, política de deprecation | Releases imprevisíveis, changelog vago, mais de duas breaking changes em doze meses |

Em casos críticos (produção em escala, conformidade regulatória, dependência estratégica), aplique a matriz de cobertura do Framework F5 em complemento, comparando a ferramenta candidata com pelo menos duas alternativas.

---

## D.2 — Plataformas de inferência (LLM-as-a-Service)

**Quando escolher:** aplicação em produção, escala variável, sem capacidade ou desejo de operar infraestrutura própria de modelo.

**Sinais de armadilha:** lock-in indevido, ausência de SLA financeiro vinculado a uptime, terms of service que permitem uso de dados do cliente para treinamento sem opt-out, ausência de SOC 2 ou ISO 27001 quando a aplicação é corporativa.

| Provedor | Estado em junho/2026 | Aplicação típica |
|---|---|---|
| **OpenAI API** | Maduro, ecossistema dominante, presença forte em SaaS BR | Aplicações genéricas, prototipagem rápida, integração via SDK em produção |
| **Anthropic Claude API** | Maduro, fronteira em raciocínio, melhor latência percebida em PT-BR conforme medição de comunidade | Aplicações em produção que valorizam consistência, escrita longa, segurança contextual |
| **Google Gemini API** | Maduro, integração com Workspace e Cloud, opção forte para clientes Google | Empresas com investimento em Google Workspace ou Vertex AI, aplicações multimodais |
| **AWS Bedrock** | Maduro, agrega múltiplos modelos sob única conta AWS, presença BR via região São Paulo | Organizações com regime AWS consolidado, conformidade rígida (saúde, financeiro), múltiplos modelos sob uma fatura |
| **Azure OpenAI** | Maduro, integração Microsoft 365, presença BR via região Brazil South | Empresas com regime Microsoft, conformidade regulada, acordos enterprise |
| **DeepSeek API** | Em consolidação, preço-qualidade agressivo; avalie risco geopolítico via critério D.1: origem do provedor, regime de dados do país de origem, restrições setoriais aplicáveis e precedente de descontinuação por decisão política | Aplicações sensíveis a custo unitário; requer avaliação explícita de risco geopolítico antes de adoção em produção corporativa |

**Critério recomendado:** decidir primeiro entre regime brasileiro/global (escolha estratégica e jurídica), depois entre soberania de dados (LGPD em território nacional vs. provedor global com contrato standard), depois entre custo unitário e capacidade de modelo. A escolha do provedor é menos sobre qual é "o melhor" e mais sobre qual encaixa no contexto regulatório, comercial e cultural da organização.

---

## D.3 — Modelos open weights para self-host

**Quando escolher:** soberania de dados como driver primário (LGPD, dados em território nacional), volume alto com escala previsível, capacidade técnica para operar GPU dedicada, restrição comercial específica.

**Sinais de armadilha:** estimativa otimista de TCO sem considerar engenharia operacional, escolha por qualidade em benchmark sem teste no caso de uso real, ausência de plano para upgrade quando próxima geração sair.

| Família | Estado em junho/2026 | Notas |
|---|---|---|
| **Llama 3.3 / Llama 4** | Maduro, licença com restrição de uso comercial em grande escala, ecossistema forte | Escolha padrão para self-host com tooling consolidado |
| **DeepSeek V3 / R1** | Fronteira em qualidade-preço, licença MIT, custo de inferência baixo via MoE | Escolha padrão quando custo é driver primário e MoE é viável |
| **Mistral Large 2 / Codestral** | Maduro, licença Apache, suporte enterprise via Mistral AI | Escolha padrão quando suporte enterprise europeu é desejável |
| **Qwen 2.5 / Qwen 3** | Maduro, licença Apache, força em chinês e multilíngue | Escolha quando multilíngue (incluindo chinês) é requisito |
| **Phi 4** | Maduro, modelos pequenos com qualidade-tamanho alta | Escolha para edge ou inferência local em hardware limitado |
| **Gemma 3** | Maduro, licença com restrição, integração Google | Escolha para regime Google quando Vertex AI não é desejado |

**Critério recomendado:** definir primeiro a licença aceitável (MIT/Apache vs. Llama community), depois o tamanho do modelo (a faixa 7B-13B serve a maioria das aplicações de produção; 70B-130B compete com modelos comerciais médios; modelos maiores exigem infraestrutura especializada), depois o suporte de quantização (INT8 e INT4 viabilizam rodar 70B em uma única H100).

---

## D.4 — Frameworks de agente e orquestração

**Quando escolher:** aplicação com loop de planejamento-ação-observação, multi-agente, integração com múltiplas ferramentas via tool use ou MCP.

**Sinais de armadilha:** framework com curva alta sem ganho proporcional, dependência transitiva grande, abstração excessiva sobre chamadas de modelo (perda de controle fino).

| Framework | Estado em junho/2026 | Aplicação típica |
|---|---|---|
| **LangChain / LangGraph** | Maduro, ecossistema dominante, curva moderada | Padrão para protótipo rápido e produção quando a integração com ferramentas é central |
| **LlamaIndex** | Maduro, força em RAG, curva mais simples para retrieval | Padrão quando o eixo dominante é RAG sobre documentos próprios |
| **AutoGen (Microsoft)** | Maduro, força em multi-agente conversacional | Aplicações com colaboração entre agentes especializados |
| **CrewAI** | Em consolidação, abstração mais simples para multi-agente | Aplicações com hierarquia de papéis explícita |
| **Pydantic AI** | Em consolidação, força em saída estruturada com tipos Python | Aplicações Python-first com forte tipagem e validação |

**Critério recomendado:** começar pelo framework com menor curva que atende o caso de uso; trocar de framework é custo de migração real, então prototipar com vários antes de comprometer arquitetura. Em produção, considerar trade-off entre framework opinado (LangChain) e abstração leve (Pydantic AI ou chamadas diretas via SDK).

---

## D.5 — Bancos vetoriais (Vector DB)

**Quando escolher:** pipeline de RAG em produção, embeddings em escala, busca semântica como funcionalidade central.

**Sinais de armadilha:** escolha por moda sem considerar escala real (Pinecone é overkill para 100k vetores; Chroma é insuficiente para 100M); escolha por preço sem considerar performance de filtragem com metadados; ignorar o trade-off entre busca exata e busca aproximada (HNSW, IVF).

| Banco | Estado em junho/2026 | Aplicação típica |
|---|---|---|
| **pgvector (Postgres)** | Maduro, escolha padrão quando PostgreSQL já está na stack | Aplicações pequenas e médias, simplicidade operacional |
| **Pinecone** | Maduro, managed, presença BR via AWS US East / São Paulo | Aplicações em escala com SLA enterprise |
| **Qdrant** | Maduro, open source, performance forte com filtros | Aplicações que precisam de filtragem rica e podem operar self-host |
| **Weaviate** | Maduro, open source com módulos, presença comunidade forte | Aplicações híbridas (vetorial + GraphQL), com módulos integrados |
| **Chroma** | Maduro, simples, ideal para protótipo e single-node | Protótipos, aplicações single-node, comunidade Python |
| **Milvus** | Maduro, escala alta, complexidade operacional alta | Aplicações com bilhões de vetores |

**Critério recomendado:** pgvector como ponto de partida sempre que a escala é compatível (até alguns milhões de vetores); Qdrant ou Weaviate quando self-host é viável e a filtragem por metadados importa; Pinecone quando managed e SLA enterprise são requisitos.

---

## D.6 — Observabilidade e LLMOps

**Quando escolher:** aplicação em produção com qualquer volume real, evals automatizados em CI, monitoramento de custo e qualidade ao longo do tempo.

**Sinais de armadilha:** confiar em logs de aplicação sem tracing estruturado; subestimar o custo de instrumentação; escolher ferramenta de observabilidade sem considerar integração com OpenTelemetry GenAI.

| Ferramenta | Estado em junho/2026 | Aplicação típica |
|---|---|---|
| **Langfuse** | Maduro, open source, SaaS opcional, OpenTelemetry compatível | Escolha padrão para auto-host ou SaaS, comunidade ativa |
| **LangSmith** | Maduro, gerenciado por LangChain | Aplicações já em LangChain, integração imediata |
| **Arize Phoenix** | Maduro, open source, força em evals e debugging | Aplicações que valorizam debugging interativo |
| **Helicone** | Maduro, proxy-based, integração rápida | Aplicações que querem observabilidade sem instrumentar código |
| **OpenLLMetry** | Em consolidação, padrão OpenTelemetry GenAI nativo | Aplicações que já operam OpenTelemetry e querem integração nativa |

**Critério recomendado:** começar com Langfuse self-hosted para projeto interno; migrar para SaaS gerenciado quando o overhead operacional ultrapassa o custo da licença; padronizar em OpenTelemetry GenAI sempre que possível para evitar lock-in.

---

## D.7 — Frameworks de evals

**Quando escolher:** aplicação em produção com golden set definido, regressão automatizada em CI, métrica de qualidade auditável.

**Sinais de armadilha:** confiar em métricas tradicionais (BLEU, ROUGE) sem considerar adequação ao caso de uso de LLM; evals subjetivos sem ancoragem em golden set; LLM-as-judge sem validação humana periódica.

| Framework | Estado em junho/2026 | Aplicação típica |
|---|---|---|
| **DeepEval** | Maduro, em Python, força em LLM-as-judge configurável | Projetos Python com testes em pytest |
| **Promptfoo** | Maduro, foco em comparação de prompts, integração CI fácil | Otimização de prompt antes da produção |
| **Ragas** | Maduro, foco específico em RAG (recall, precision, faithfulness) | Aplicações de RAG em produção |
| **Inspect AI** | Maduro, AISI UK, força em avaliações de segurança e capability | Avaliações de segurança e red teaming sistemático |

**Critério recomendado:** Ragas como instrumento padrão quando a aplicação é RAG; DeepEval ou Promptfoo para evals gerais de prompt e qualidade; Inspect AI quando o eixo dominante é segurança ou capability evaluation.

---

## D.8 — MCP (Model Context Protocol)

**Quando escolher:** arquitetura com múltiplas ferramentas, descoberta dinâmica, integração plural com sistemas externos, expectativa de mudar de provedor de LLM.

**Sinais de armadilha:** adotar MCP por moda quando a integração é one-off; servidor MCP sem governança de versão; cliente MCP sem confirmação humana antes de invocar tools com efeito.

| Item | Estado em junho/2026 | Aplicação típica |
|---|---|---|
| **MCP SDK Python e TypeScript** | Maduro, mantido por Anthropic, ecossistema em crescimento | Construção de servidor MCP customizado |
| **Servidores oficiais Anthropic** (filesystem, github, postgres, slack etc.) | Maduros, repositório aberto, referência canônica | Adoção de servidores prontos para casos comuns |
| **modelcontextprotocol/servers** | Maduro, repositório de referência | Inspiração e cópia parcial para servidores customizados |
| **punkpeye/awesome-mcp-servers** | Em consolidação, lista da comunidade | Descoberta de servidores publicados pela comunidade |

**Critério recomendado:** começar com servidores oficiais Anthropic para casos comuns; construir servidor MCP customizado quando a integração interna justifica esforço; padronizar autenticação com OAuth para servidores remotos.

---

## D.9 — Repositórios e gestão de prompts

**Quando escolher:** aplicação em produção com muitos prompts, versionamento crítico, equipe distribuída editando prompts colaborativamente.

**Sinais de armadilha:** versionar prompts em código junto com aplicação (acoplamento ruim); editar prompts sem golden set associado; ausência de A/B testing de prompt.

| Ferramenta | Estado em junho/2026 | Aplicação típica |
|---|---|---|
| **Pezzo** | Maduro, open source, versionamento e A/B | Projetos que querem self-host com versionamento estruturado |
| **PromptHub** | Em consolidação, foco em colaboração | Equipes distribuídas editando prompts |
| **PromptLayer** | Maduro, observabilidade + gestão | Aplicações que combinam gestão e observabilidade de prompt |
| **Langfuse Prompts** | Maduro, integrado a observabilidade | Aplicações já em Langfuse |

**Critério recomendado:** começar com Langfuse Prompts ou Pezzo quando o eixo é versionamento; considerar repositório próprio (Git + Markdown) quando a equipe é pequena e a complexidade não justifica plataforma dedicada.

---

## Cadência de revisão

Esta lista recebe revisão periódica conforme o ecossistema evolui, sem cadência fixa anunciada. Leitores que identificarem ferramenta nova relevante, mudança significativa no estado de uma ferramenta listada, ou desaparecimento de qualquer item, são convidados a abrir issue no repositório.

As revisões podem trazer reestruturação de categorias conforme a maturidade do ecossistema brasileiro de IA evolua. O critério editorial é honestidade quanto à validade temporal da curadoria, com data declarada no cabeçalho e sem disfarce de eternidade que a indústria de IA não permite.

---

## Conexão com o livro

- **Apêndice D — Ferramentas e Stack** — fonte primária desta lista, com texto completo e contexto editorial
- **Framework F5 — Matriz de Cobertura de Integrações** — complemento ao critério de escolha para casos críticos
- **Capítulo 17 — Auditoria de Repositório GitHub** — método de avaliação de projeto open source aplicável a qualquer ferramenta desta lista
- **[`/mcp`](../mcp/)** — servidores MCP educacionais que implementam o SDK listado em D.8

> *"Copiar a lista sem critério é fazer o mesmo erro que este catálogo quer evitar."*
>
> *— Inteligência Aumentada · Os Invariantes da IA, Apêndice D*
