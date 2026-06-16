# Repositórios GitHub · Lista Curada

> Atualizado em: 2026-06-16
> Próxima revisão: conforme o ecossistema evolui — a lista envelhece, o método não
> Fonte primária: Capítulo 17 do livro *Inteligência Aumentada · Os Invariantes da IA* (Fabio Garcia, 2026)

---

## Aviso antes da lista

Esta lista é exercício de aplicação, não inventário durável. O estado de cada repositório foi observado em meados de 2026. O leitor que acessar esta lista em 2027 vai encontrar mudança em pelo menos um terço dos itens — transição de fase, mudança de governança, aparição de competidor que reorganiza o quadrante.

O ponto do Capítulo 17 do livro é exatamente esse: inventário envelhece em seis meses, método de auditoria dura uma carreira. O que segue é a lista; o método de avaliá-la está na seção abaixo.

---

## O Protocolo de 30 Minutos (o método que não envelhece)

Antes de adotar qualquer repositório desta lista — ou qualquer outro que aparecer em conferência, newsletter ou fio de rede social —, aplique os seis critérios abaixo. Cinco minutos por critério, trinta minutos no total. A decisão final tem três saídas: adoção em produção (seis critérios passando), piloto controlado em sandbox (cinco passando, encaixe parcial recuperável), descarte (dois ou mais falhando, ou qualquer dos quatro primeiros falhando em projeto que se apresenta como pronto para produção).

| Critério | Duração | Onde olhar | Sinal de passa | Sinal de falha |
|---|---|---|---|---|
| **1. Sinais de vida** | 5 min | Página inicial, Insights, Contributors | Commit recente, cadência mensal saudável, ≥3 contribuidores ativos | Sem commit há 180+ dias, contribuidor único, gráfico zerado |
| **2. Maturidade de release** | 5 min | Releases, tags, CHANGELOG.md | SemVer estrito, changelog detalhado, breaking changes documentadas | Versionamento caótico, sem changelog, breaking sem aviso |
| **3. Qualidade de código** | 5 min | Árvore do repo, README badges, aba Actions | Testes presentes, CI verde, cobertura declarada, linter ativo | CI vermelho, sem testes, sem type checking |
| **4. Documentação operacional** | 5 min | README, docs/, examples/ | Quickstart em menos de 5 min, guia de produção, exemplos que rodam | README de marketing, sem guia de produção, exemplos quebrados |
| **5. Padrão de governança** | 5 min | Raiz, .github/, Community profile | CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, política de release | Mantenedor único sem CONTRIBUTING, sem política de segurança |
| **6. Encaixe com seu contexto** | 5 min | LICENSE, dependências, canal de comunidade | Licença compatível, stack alinhada, comunidade acessível, fork viável | Licença incompatível, stack estranha, comunidade em idioma inacessível |

**Quatro armadilhas para evitar:**

- **Confiar em estrelas.** Stars medem atenção em janela, não viabilidade técnica. Projetos com cem mil estrelas e mantenedor único existem.
- **Confiar em README de marketing.** O README escrito como pitch não é documentação técnica.
- **Confiar em demonstração.** Demo funciona em condição ideal com dados curados. A operação real introduz variabilidade que a demo não captura.
- **Confiar em post de blog.** Post de quem rodou o exemplo do README é entusiasmo, não validação de produção.

---

## Lista corrente (estado observado em meados de 2026)

### Frameworks de agente e orquestração

**LangChain / LangGraph.** Fase de maturidade com sinais de manutenção. Cadência de release alta, ecossistema massivo, comunidade ativa, governança institucional formalizada via LangChain Inc. Questão crítica para adoção é encaixe: a complexidade justifica-se em equipes que operam múltiplos modelos e múltiplas tools simultaneamente; over-engineering documentado em equipes que operam um único caso de uso.

**LlamaIndex.** Fase de maturidade, foco específico em RAG, comunidade técnica séria, cadência de release saudável. Encaixe forte em organização que opera RAG como caso principal, com competição direta com Haystack e com implementação custom em equipes maduras. Documentação operacional de qualidade alta.

**CrewAI.** Em consolidação, abstração mais simples para multi-agente com hierarquia de papéis explícita. Verificar cadência de release e governança antes de adoção em produção.

**Pydantic AI.** Em consolidação, força em saída estruturada com tipos Python. Encaixe forte em aplicações Python-first com forte tipagem e validação.

### Inferência e serving

**vLLM.** Fase de maturidade com adoção em produção corporativa consolidada. Infraestrutura de inferência otimizada, governança em organização universitária séria, integração madura com Hugging Face. Encaixe forte em organização que opera self-hosting de modelo de fronteira.

**Ollama.** Fase de adoção real para uso local e prototipação. Experiência de desenvolvedor de qualidade alta, governança em empresa comercial dedicada, cadência de release alta. Encaixe forte em uso pessoal, prototipação e demo; encaixe duvidoso em produção corporativa de alto volume onde vLLM e TGI dominam.

**LiteLLM.** Fase de maturidade com adoção em produção. Gateway unificado para múltiplos provedores de modelo, cadência alta de release, comunidade ativa, governança em empresa comercial. Encaixe forte em organização que opera multi-provedor; questão crítica: observabilidade nativa versus integração com Langfuse ou equivalente.

### Observabilidade e MLOps

**MLflow.** Fase de manutenção em ecossistema clássico de ML, com extensão recente para LLMOps. Cadência de release saudável, governança institucional via Databricks, comunidade técnica madura. Encaixe forte em organização que já opera MLflow para modelos clássicos e quer estender para LLM; encaixe duvidoso em organização nativa de LLM sem histórico de ML clássico.

**Weights & Biases.** Fase de maturidade com componente proprietário dominante. Ferramenta de experimentação e observabilidade líder, cadência de release alta no SDK open source, modelo de negócio em camada hospedada. Encaixe forte em organização que vai operar com a camada hospedada; encaixe duvidoso em organização que precisa de operação totalmente self-hosted por restrição regulatória.

### Hubs de descoberta e curadoria

**Hugging Face.** Hub central de modelos, datasets e espaços de demonstração. Estado: infraestrutura crítica do ecossistema. Não é um repositório para auditar pelo protocolo acima — é plataforma de acesso a ativos. Referência obrigatória para qualquer pipeline de model.

**Papers with Code.** Papers com implementação verificável. Estado: maduro, mantido por Meta AI. Útil para localizar implementações antes de construir do zero.

---

## Ciclo de vida do repositório — o que observar

Em vez de memorizar o estado de cada repositório, memorize as cinco fases e seus sinais:

**Hype.** Explosão de stars em janela curta, README como pitch de produto, demonstração impressionante, ausência de uso corporativo documentado. Postura: não adotar, retornar em três a seis meses.

**Adoção real.** Posts técnicos detalhados em blog de empresa séria, integração documentada em projeto popular adjacente, primeiras issues sofisticadas de uso em escala. Postura: ativar avaliação séria com piloto controlado.

**Maturidade.** Cadência regular de release com SemVer estrito, comunidade com múltiplos contribuidores ativos, presença de variante hospedada ou empresa comercial dedicada, integrações oficiais com ferramentas adjacentes. Postura: adoção em produção com confiança calibrada.

**Manutenção.** Cadência de release reduzida com foco em patch e segurança, declaração explícita de fase de manutenção, comunidade discutindo "qual é o próximo X". Postura: manter em produção com planejamento de sucessão.

**Abandono.** Último commit há mais de cento e oitenta dias, mantenedor anunciando saída ou silenciando, comunidade migrando publicamente para alternativa, repositório sendo arquivado. Postura: migração planejada com prazo definido.

---

## Conexão com o livro

- **Capítulo 17 — Auditoria de Repositório GitHub em 30 Minutos** — fonte primária do protocolo e das armadilhas
- **Apêndice D** — catálogo de ferramentas complementar → [`/ferramentas`](../ferramentas/)
- **Capítulo 13 — MCP** — o Model Context Protocol e os servidores que a comunidade mantém
- **Capítulo 16 — Open Source** — quando adoção de open source em produção faz sentido estratégico

> *"Inventário envelhece em seis meses. Método dura uma carreira. A diferença entre o operador que vai operar com vantagem em 2030 e o que vai operar com hype em 2030 é o método, não a lista; e o método cabe em trinta minutos por repositório, com seis critérios duráveis e a coragem de descartar quatorze de cada vinte."*
>
> *— Inteligência Aumentada · Os Invariantes da IA, Capítulo 17*
