# Fontes · Leituras, Newsletters e Comunidade Brasileira

> Atualizado em: 2026-06-16
> Próxima revisão: leituras técnicas conforme surgem referências novas; comunidade brasileira anualmente
> Fonte primária: Apêndice E (Leituras) e Apêndice F (Comunidade Brasileira de IA em 2026) do livro *Inteligência Aumentada · Os Invariantes da IA* (Fabio Garcia, 2026)

---

## Critérios de curadoria

Esta lista existe porque o volume de material sobre IA em 2026 é, ele próprio, um problema. Não falta conteúdo; falta sinal no ruído. A curadoria aqui segue três critérios explícitos:

**Profundidade sobre divulgação.** Prefer fontes que explicam mecanismo, não apenas anuncia novidade. Newsletter que explica *por que* o modelo mudou é mais útil do que newsletter que informa *que* o modelo mudou.

**Fonte primária verificável.** Toda afirmação de fato técnico que não puder ser rastreada a um paper, documentação oficial, ou caso de uso real de empresa identificável não entra aqui como referência técnica.

**Validade temporal declarada.** Cadência e responsável de cada fonte são indicados onde conhecidos. Quando mudam, a lista envelhece — e a responsabilidade de verificar é do leitor.

---

## Livros — Fundamentos técnicos

Livros técnicos de IA têm vida útil diferente por categoria. Fundamentos matemáticos (transformers, probabilidade, aprendizado profundo) têm vida longa. Frameworks de aplicação (LangChain, arquiteturas de agente) têm vida curta. A lista abaixo prioriza fundamentos.

**Russell, S. & Norvig, P. — *Artificial Intelligence: A Modern Approach* (4ª ed., 2020).** Referência canônica do campo. Denso. Para quem quer fundamento acadêmico estruturado.

**Bishop, C. & Bishop, H. — *Deep Learning: Foundations and Concepts* (2024).** Fundamentos matemáticos modernos. Para o profissional técnico que quer ir além do uso e entender o mecanismo.

**Goodfellow, I., Bengio, Y. & Courville, A. — *Deep Learning* (2016).** Clássico. Algumas partes desatualizadas; a estrutura conceitual de redes neurais e treinamento segue válida.

**Murphy, K. — *Probabilistic Machine Learning* (2 vols., 2022, 2023).** Fundamentos probabilísticos para quem quer aprofundar a base matemática.

---

## Livros — IA aplicada e pensamento de campo

**Karpathy, A. — coleção de palestras públicas e o blog `karpathy.ai`.** Não é livro formal, mas o conjunto vale como referência de pensamento técnico aplicado atual. Didático, calibrado, sem hype.

**Engelbart, D. — *Augmenting Human Intellect* (1962).** O conceito original de "inteligência aumentada". Origem filosófica da obra que este repositório acompanha.

**Christian, B. — *The Alignment Problem* (2020).** Visão geral acessível sobre alinhamento, para quem entra no tema sem background técnico denso.

**Russell, S. — *Human Compatible* (2019).** Fundamento filosófico do alinhamento. Complementa o capítulo de alignment do livro.

---

## Livros — Governança e operação

**Beyer, B. et al. — *Site Reliability Engineering* (Google, 2016) e *The Site Reliability Workbook* (2018).** Fundamento de operação madura diretamente aplicável a LLMOps. A cultura de SRE é o piso sobre o qual LLMOps se constrói.

**Doerr, J. — *Measure What Matters* (2018).** OKRs como instrumento de adoção de IA com meta mensurável. Útil para profissional que precisa traduzir projeto de IA em linguagem de liderança.

**Davenport, T. — *The AI Advantage* (2018).** Visão executiva de adoção com casos reais. Desatualizado em tecnologia, ainda válido em dinâmica de mudança organizacional.

---

## Blogs e newsletters em inglês

Fontes de referência técnica que combinam frequência com profundidade. Para estar perto da fronteira, o consumo em inglês continua necessário em 2026.

**Blogs de provedor (fonte primária, não neutra):**
- OpenAI blog (`openai.com/news`) — lançamentos, pesquisa, segurança
- Anthropic blog (`anthropic.com/news`) — pesquisa, interpretabilidade, política
- Google DeepMind blog — pesquisa, produtos, benchmarks
- Meta AI blog — open weights, pesquisa, infraestrutura
- Hugging Face blog — modelos, datasets, ferramentas open source

**Análise independente (sinal mais confiável):**
- **Simon Willison** (`simonwillison.net`) — cobertura ampla e calibrada, excelente filtro de hype
- **Karpathy** (`karpathy.ai`) — profundidade técnica, pensamento de campo

**Newsletters de análise aplicada:**
- **Latent Space** — newsletter sobre IA aplicada, deep dives técnicos, entrevistas com operadores
- **The Batch** (deeplearning.ai) — curadoria semanal por Andrew Ng
- **Import AI** (Jack Clark) — foco em pesquisa, política e segurança

---

## Cursos e recursos de aprendizado

- **DeepLearning.AI** — curso de Andrew Ng e curadoria de cursos curtos sobre RAG, agentes, LangChain e tópicos específicos
- **Hugging Face Course** — open source, prático, atualizado
- **Fast.ai** — Practical Deep Learning for Coders, abordagem aplicada com código real
- **OpenAI cookbook** — exemplos práticos em repositório oficial (`github.com/openai/openai-cookbook`)
- **Anthropic courses** — cursos abertos em `github.com/anthropics/courses`
- **Google ML Crash Course** — introdução estruturada, gratuita
- **MIT 6.5940 TinyML** — para quem opera em hardware especializado e edge
- **Stanford CS25 Transformers United** — fundamentos avançados de arquitetura

---

## Newsletters brasileiras em português

A oferta brasileira de newsletter sobre IA cresceu nos últimos dois ciclos. As cinco fontes abaixo são as mais consistentes em junho de 2026. Nome, cadência e responsável podem mudar; verificar estado na próxima revisão.

**Tecnologia e IA, com Filipe Deschamps.** Newsletter semanal, viés de divulgação técnica acessível, foco em explicar conceitos novos para quem programa e para quem decide. Boa porta de entrada para quem ainda não consome em inglês.

**Tech&Co, do Grupo Globo.** Cobertura jornalística de IA corporativa no Brasil, com peso para casos de adoção em grandes empresas, regulação local e movimentos de mercado. Útil para profissional que precisa traduzir IA para conversa executiva.

**The Shift.** Newsletter de tecnologia com seção dedicada a IA, entrevistas e leituras curadas. Tom mais analítico do que noticioso.

**Olhar Digital.** Boletim diário de cobertura ampla, incluindo IA. Sem profundidade técnica, mas útil para manter pulso da agenda pública e do enquadramento midiático que clientes e usuários consomem.

**PEBMED (vertical de saúde).** Newsletter dedicada ao profissional médico brasileiro, com seção crescente sobre IA aplicada à medicina, regulação da Anvisa e CFM. Referência de que o profissional de IA em vertical regulada encontra nicho dedicado em português.

---

## Podcasts brasileiros em português

### Dedicados a IA (surgidos entre 2024 e 2026)

**IA Todo Dia, com Diego Sommer e Helena Ferraz.** O maior podcast brasileiro dedicado exclusivamente a IA em 2026. Cadência alta, foco em explicar como IA muda carreira, negócio e cotidiano. Ponto natural de entrada para quem quer compromisso semanal com a agenda em português.

**IA Sob Controle, com Marcus Mendes e Fabrício Carraro.** Episódios regulares com profundidade superior à média brasileira, convidados especialistas e leitura técnica honesta. O mais próximo, em português, de podcast técnico de fronteira no estilo Latent Space.

**SABIÁ — Inteligência Artificial à Brasileira, do BI0S na Unicamp.** Podcast quinzenal acadêmico-aplicado, conectado a grupo de pesquisa real em universidade pública brasileira. Traz a voz da pesquisa brasileira para o consumidor não-acadêmico.

**Papo de IA, da Comunidade Profissionais do Futuro.** Conversas práticas sobre adoção de IA em empresa brasileira, com foco em aprendizado aplicado e construção de carreira.

### Tecnologia ampla com IA recorrente

**Hipsters.tech, da Alura.** Episódios regulares dedicados a IA aplicada, com convidados que operam em produção em empresas brasileiras.

**Tecnocracia, do Manual do Usuário.** Pensamento crítico sobre tecnologia, cobertura recorrente de IA. Tom adversarial qualificado, útil para treinar o senso crítico que o Princípio Um da obra exige.

---

## Comunidades online brasileiras

**Brasil.AI.** Comunidade aberta no Discord, com canais dedicados a NLP, visão, agentes, carreira, vagas. Tom técnico, moderação ativa. Referência para dúvida técnica em português.

**Data Hackers.** Newsletter combinada com Slack, com profissionais brasileiros de dados e IA. Referência consolidada, com canais de carreira, dúvida técnica e evento.

**AI Brasil, grupo no LinkedIn.** Grupo grande, com mistura de profissional, recrutador e divulgação de conteúdo. Útil para acompanhar movimento de mercado e oportunidades.

---

## Conferências brasileiras relevantes

**Campus Party Brasil.** Evento anual, palco aberto para IA, formato que combina palestra, hackathon e feira. Bom para profissional que está começando e quer mapear o ecossistema.

**TDC — The Developers Conference.** Circulação nacional, trilhas dedicadas a IA com profundidade técnica crescente.

**FEBRABAN Tech.** Evento de tecnologia do setor financeiro, com peso crescente em IA aplicada a banco e fintech. Cobertura de regulação, fraude, atendimento automatizado e conformidade normativa.

**Conferência Brasileira de Inteligência Artificial (SBCAI/SBC).** Evento acadêmico anual da Sociedade Brasileira de Computação, com publicação científica avaliada por pares. Referência para profissional que mantém vínculo com pesquisa.

---

## Crítica honesta da cena brasileira (junho de 2026)

**O que melhorou (2024–2026).** A cena de podcast saltou de episódios ocasionais para quatro projetos dedicados exclusivamente a IA com cadência regular e densidade técnica crescente. Comunidades como Data Hackers e Brasil.AI cresceram em massa crítica. A FEBRABAN Tech consolidou-se como evento sério. O ecossistema de fintech publicou casos reais de adoção em série.

**O que ainda falta.** Falta newsletter técnica semanal de profundidade comparável a Latent Space, escrita em português. Falta conferência anual dedicada exclusivamente a IA generativa com chamado técnico avaliado. Falta blog de engenharia público de grandes empresas brasileiras no padrão dos blogs de Netflix, Uber, Stripe. O profissional brasileiro que quer estar na fronteira ainda precisa, em 2026, consumir conteúdo majoritariamente em inglês.

---

## Como contribuir com esta lista

Esta lista é revisada periodicamente sem cadência fixa. O leitor que quiser sugerir nova fonte, corrigir item desatualizado, apontar newsletter descontinuada ou indicar recurso que mereça figurar na próxima revisão pode abrir issue no repositório com o template `factual-correction` ou `new-prompt-suggestion` adaptado para fontes.

---

## Conexão com o livro

- **Apêndice E — Leituras Complementares** — fonte primária da seção de livros e cursos
- **Apêndice F — Comunidade Brasileira de IA em 2026** — fonte primária da seção de newsletters, podcasts e conferências
- **Princípio Cinco — Honestidade Temporal** — a postura que exige data e revisão declaradas em toda lista perecível
- **Capítulo 17 — Auditoria de Repositório GitHub** — o método que também se aplica a avaliar qualquer repositório de ferramentas listado aqui

> *"A segunda vida da profissão de IA no Brasil acontece em português, em rodas de conversa em meetups, em comunidades no Discord e Telegram, e essa segunda vida é a que sustenta carreira, contratação, mentoria, debate sobre regulação local, e troca real de aprendizado em contexto brasileiro."*
>
> *— Inteligência Aumentada · Os Invariantes da IA, Apêndice F*
