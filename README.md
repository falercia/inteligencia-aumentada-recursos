# Inteligência Aumentada · Recursos

> O número que muda. A Camada Dupla aplicada na prática.
> Companheiro executável do livro **Inteligência Aumentada · Os Invariantes da IA** (Fabio Garcia, 2026).

> 📖 **Os livros são gratuitos.** Baixe nos Releases: [Livro 1 — Os Invariantes da IA](https://github.com/falercia/inteligencia-aumentada-recursos/releases/latest) · [Livro 2 — Deep Claude](https://github.com/falercia/deep-claude/releases/latest)
>
> 💡 **Dica — leia com IA:** jogue os PDFs no **[NotebookLM](https://notebooklm.google.com)** (grátis). Você conversa com os livros, pede resumo por capítulo e gera um *audio overview* pra ouvir no trânsito. Vira um tutor particular da obra.

[![Licença código](https://img.shields.io/badge/c%C3%B3digo-MIT-blue)](#licença)
[![Licença conteúdo](https://img.shields.io/badge/conte%C3%BAdo-CC--BY%204.0-lightgrey)](#licença)

---

## Por que este repositório existe

A obra **Inteligência Aumentada** opera sob o Invariante Três, a Camada Dupla, que afirma que conhecimento em IA vive em dois andares, o padrão que dura e o número que muda. O livro carrega o padrão — frameworks, arquiteturas, anti-padrões, vocabulário durável. Este repositório carrega o número — XML versionado de prompts, golden sets executáveis, scripts de regressão, changelog versionado, exemplos rodáveis, agentes e servidores MCP educacionais.

Sem o livro, este repositório é catálogo sem mapa, com receitas que o operador desentendido aplicará no contexto errado. Sem o repositório, o livro é vocabulário sem executável, com método que o operador entendeu mas não consegue colocar em produção sem reescrever cada artefato do zero. Juntos, os dois materializam a tese central da obra, com o leitor que opera com os dois saindo com modelo mental sólido e ativos prontos para entrar em pipeline.

---

## Para quem é

**Para o leitor do livro.** Você terminou o APX-L e quer baixar os 30 prompts em qualidade de produção, com golden set executável, prefill, self-critique e changelog datado. Está no lugar certo. Comece em [`/prompts`](./prompts/).

**Para o CTO, Tech Lead ou AI Engineer em adoção real.** Você precisa instrumentar avaliação de prompts em CI/CD, estabelecer cadência de regressão, construir biblioteca interna versionada. Está no lugar certo. Comece em [`/evals`](./evals/) e leia o [CONTRATO.md](./CONTRATO.md).

**Para o especialista do domínio que quer contribuir.** Você é advogado, médico, analista financeiro, RH, professor, e identificou caso limítrofe que o golden set atual não cobre. Sua contribuição é o que faz este repositório virar referência calibrada por painel, não por autor único. Veja [Como contribuir](#como-contribuir).

---

## O que vive aqui

| Pasta | Conteúdo | Capítulos relacionados |
|---|---|---|
| 📚 [`/prompts`](./prompts/) | 30 prompts profissionais em XML versionado, com golden set, prefill, self-critique, changelog e métrica de qualidade por prompt | Cap 9 Engenharia de Prompt · F4 Engenharia de Prompt Estendida · APX-L Biblioteca de Prompts |
| 🏛️ [`/governance`](./governance/) | Caderno de Governança v1.0 em Camada Dupla — 6 seções fatiadas, modelo de 6 pg para imprimir e assinar, anexos clonáveis | Cap 24 Governança · F6 Governança Indelegável · APX-O Caderno de Governança |
| 🔬 [`/evals`](./evals/) | `eval_runner.py` executável, `compile_golden_sets.py`, judges integrados, gate de CI | Cap 21 Evals · F8 Pirâmide da Avaliação |
| 📦 [`/datasets`](./datasets/) | Golden sets em JSONL compilados a partir dos YAML originais, prontos para CI | Cap 21 Evals · Cap 23 Alignment (adversarial sets) |
| 🤖 [`/agents`](./agents/) | Quatro agentes educacionais em Python puro — A01 ReAct Simples, A02 Escala de Propriedade nos 4 níveis F3 lado a lado, A03 Orquestrador-Especialistas (multiagente cooperativo em estrela reusando `/prompts`) e A04 Multiagente Debate (adversarial com juiz integrável a `/evals`), com tracing, gates, kill switch e exemplos rodáveis | Cap 12 Agentes · Cap 14C SDD · Cap 21 Evals · Cap 22 LLMOps · Cap 25 Trade-offs · F3 Escala de Propriedade · F8 Pirâmide da Avaliação |
| 🔌 [`/mcp`](./mcp/) | Servidores MCP educacionais — M01 Hello World e M02 Biblioteca Interna que expõe `/prompts` e `/governance` para qualquer cliente MCP | Cap 13 MCP · F5 Matriz de Cobertura de Integrações |
| 📓 [`/notebooks`](./notebooks/) | 4 notebooks fundacionais executáveis — tokenização, janela de contexto/Lost in the Middle, embeddings com visualização 2D, prompt caching | Cap 3 Tokens · Cap 4 Janela de Contexto · Cap 5 Embeddings · Cap 18 Economia de Tokens |
| 🔗 [`/apendice-vivo`](./apendice-vivo/) | Ponteiro para a fonte única de números cross-vendor da série (modelos, preços, benchmarks, janelas de contexto) mantida no repo deep-claude, com método vendor-neutral de ler comparações de modelo e preço de token | APX-J Trilha do Número · Invariante Três Camada Dupla · Cap 15 Modelos |
| 🛠️ [`/ferramentas`](./ferramentas/) | Catálogo de ferramentas e stack extraído do APX-D — plataformas de inferência, modelos open weights, frameworks de agente, bancos vetoriais, observabilidade, evals, MCP e gestão de prompts — com critério de seleção em seis dimensões e data de revisão | APX-D Ferramentas e Stack · Framework F5 Matriz de Cobertura · Cap 17 Auditoria de Repositório |
| 📦 [`/repos-curados`](./repos-curados/) | Lista de repositórios GitHub do Cap 17, com o Protocolo de 30 Minutos (seis critérios duráveis), as quatro armadilhas clássicas e o ciclo de vida do repositório como cabeçalho — a lista envelhece, o método não | Cap 17 Auditoria de Repositório · Cap 13 MCP · Cap 16 Open Source |
| 📚 [`/fontes`](./fontes/) | Leituras (APX-E) e comunidade brasileira (APX-F) fundidas — livros de fundamento técnico, livros de governança, blogs e newsletters em inglês, newsletters e podcasts brasileiros, conferências e comunidades online, com critérios de curadoria e data de revisão | APX-E Leituras · APX-F Comunidade Brasileira de IA · Invariante Cinco Honestidade Temporal |

Cada pasta tem seu próprio `README.md` com instruções específicas, padrões de uso e exemplos práticos.

---

## Como começar em 60 segundos

```bash
git clone https://github.com/falercia/inteligencia-aumentada-recursos.git
cd inteligencia-aumentada-recursos
```

Três caminhos a partir daqui, conforme seu objetivo:

**1. Quero entender antes de usar.** Abra [`/prompts/P-LEG-01/`](./prompts/) e leia o `README.md` da pasta, depois compare com a ficha conceitual correspondente no APX-L do livro. Em quinze minutos você terá o mapa mental completo de como livro e repositório se costuram.

**2. Quero colocar em produção rápido.** Pegue o prompt mais próximo do seu domínio, copie o diretório inteiro para o seu repositório interno, adapte a constituição ao seu contexto, construa seu golden set próprio com pelo menos vinte casos representativos do seu tráfego real, e rode `eval.py` antes de cada release. O atalho está em [Padrão de adoção](./prompts/README.md).

**3. Quero contribuir.** Leia [CONTRATO.md](./CONTRATO.md) e abra uma issue com a categoria sugerida. Contribuições qualificadas com fonte primária são incorporadas em revisões futuras do repositório, com atribuição quando o contribuidor autoriza.

---

## Estado atual

**Biblioteca de prompts completa, com infraestrutura executável de evals, agentes educacionais, servidores MCP e notebooks fundacionais disponíveis.** Os artefatos são revisados quando a calibração exige, e não em cadência fixa pré-anunciada.

### Biblioteca de prompts — status por domínio

| Domínio | Prompts | Em qualidade plena |
|---|---|---|
| Jurídico | 4 | ✅ 4/4 |
| Saúde | 3 | ✅ 3/3 |
| Financeiro | 4 | ✅ 4/4 |
| SaaS | 4 | ✅ 4/4 |
| Suporte | 3 | ✅ 3/3 |
| RH | 3 | ✅ 3/3 |
| Marketing | 3 | ✅ 3/3 |
| Educação | 3 | ✅ 3/3 |
| Transversais | 3 | ✅ 3/3 |
| **Total** | **30** | **30/30** |

**Qualidade plena** significa: golden set com 20 casos categorizados em fáceis, médios e limítrofes, prefill ancorando o início da resposta, self-critique calibrado contra a constituição, anti-padrões observados e métrica quantitativa de qualidade. Os 30 prompts foram calibrados pelo autor com base em prática profissional do domínio, e estão abertos a contribuição de especialistas via templates de issue.

Esta postura segue o que a obra prega no Invariante Cinco, a Honestidade Temporal: a biblioteca chega ao público em estado fechado, mas com cadência pública declarada de revisão e contribuição. Cada caso do golden set carrega data de calibração, e cada prompt tem changelog próprio para registrar a iteração.

### Outras pastas

| Pasta | Estado |
|---|---|
| `/governance` | **Executável** · Caderno de Governança em Camada Dupla, 10 arquivos (artefato do APX-O) |
| `/evals` | **Executável** · `eval_runner.py` rodável, `compile_golden_sets.py`, judges integrados, gate de CI |
| `/datasets` | **Estrutura definida** · esquema JSONL documentado, compilação a partir de YAML, 60 golden sets calibrados em 3 domínios |
| `/agents` | **Executável — 4 agentes completos** · A01 ReAct Simples, A02 Escala de Propriedade nos 4 níveis F3 lado a lado, A03 Orquestrador-Especialistas (cooperativo em estrela, reusando `/prompts` como especialistas) e A04 Multiagente Debate (adversarial proponente × oponente com juiz integrável a `/evals`) |
| `/mcp` | **Executável** · M01 Hello World e M02 Biblioteca Interna completos, com `claude_desktop_config.example.json` e cliente de teste local |
| `/notebooks` | **Executáveis** · 4 notebooks fundacionais (tokenização, janela de contexto, embeddings, prompt caching) com narrativa didática célula a célula |
| `/apendice-vivo` | **Ponteiro** · Redireciona para a fonte única de números cross-vendor no repo deep-claude, com método vendor-neutral de leitura |
| `/ferramentas` | **Catálogo datado** · APX-D completo — 8 categorias, critério de seleção em 6 dimensões, data de referência junho/2026 |
| `/repos-curados` | **Catálogo datado** · Lista do Cap 17 com Protocolo de 30 Minutos, armadilhas e ciclo de vida do repositório como cabeçalho |
| `/fontes` | **Catálogo datado** · APX-E + APX-F fundidos — livros, blogs, newsletters, podcasts, conferências e comunidades brasileiras |

---

## Filosofia editorial

**Por que XML.** Modelos da família Claude foram treinados para reconhecer tags como delimitadores semânticos fortes, com aderência mensurável superior a markdown em testes A/B. Se você opera com outra família, substitua XML por marcadores equivalentes, mas mantenha a separação clara entre instrução e dado, que é a propriedade arquitetural que importa.

**Por que golden set.** Trocar prompt porque "ficou melhor" sem golden set é torcida, não decisão. O golden set é o equivalente da bateria de testes automatizados que qualquer engenheiro sênior exige antes de promover código, aplicado a saídas de IA que são não-determinísticas e por isso ainda mais perigosas sem instrumento de medida.

**Por que prefill.** Ancora o início da resposta no formato esperado, reduzindo a chance de o modelo divagar antes de entregar o conteúdo estruturado. O ganho é mensurável especialmente em saídas JSON e em fluxos com schema fechado.

**Por que self-critique.** Modelos longos perdem peso relativo das regras do início conforme a resposta cresce. Forçar uma rodada explícita de revisão antes de devolver o output recupera aderência à constituição em casos limítrofes onde o output direto fugiria do escopo.

**Por que repositório separado do livro.** O livro entrega o método que sobrevive à próxima geração de modelos. Este repositório entrega os artefatos que materializam o método em produção. Os dois evoluem em ritmos diferentes — o método dura anos, os artefatos são revisados quando a calibração exige —, e separar fisicamente os dois é a aplicação direta da Camada Dupla.

---

## Como contribuir

Três tipos de contribuição são bem-vindos, em ordem decrescente de impacto:

**1. Calibração especialista do golden set.** Você é profissional sênior no domínio (advogado, médico, analista, RH, professor) e identifica caso limítrofe que o golden atual não cobre, ou divergência entre a saída esperada do golden e a prática profissional do seu campo. Abra issue com o template `golden-set-calibration` e descreva o caso, a saída esperada conforme sua prática, e a fonte primária quando aplicável.

**2. Correção de fato ou referência.** Você identificou referência jurisprudencial inexata, artigo de lei mal citado, paper com identificador errado, número de benchmark desatualizado. Abra issue com o template `factual-correction` e cite a fonte primária correta.

**3. Sugestão de novo prompt para a biblioteca.** Você identifica caso de uso recorrente que não está coberto pelos 30 prompts atuais. Abra issue com o template `new-prompt-suggestion` e descreva a dor, o domínio, e por que a biblioteca atual não resolve.

Todas as contribuições qualificadas com fonte primária ou validação por especialista são incorporadas em revisões futuras, com atribuição em `CONTRIBUTORS.md` quando o contribuidor autoriza.

Antes de qualquer contribuição, leia [CONTRATO.md](./CONTRATO.md) para entender o escopo de manutenção, a política de versionamento e o direito autoral.

---

## Conexão com o livro

Este repositório só faz sentido pleno em conjunto com a obra **Inteligência Aumentada · Os Invariantes da IA**, especialmente com:

- **Apêndice L · Biblioteca de Prompts Profissionais** — entrega a ficha conceitual de cada um dos 30 prompts, com a dor que resolve, anatomia, anti-padrões e critério de uso. Cada ficha aponta para o diretório correspondente neste repositório.
- **Apêndice J · Trilha do Número** — referencia este repositório como fonte viva dos números (modelos, preços, benchmarks, papers, regulação) que mudam mensalmente.
- **Framework Quatro · Engenharia de Prompt Estendida** — entrega a anatomia em cinco blocos XML que estrutura cada prompt aqui.
- **Framework Oito · Pirâmide da Avaliação** — entrega o método que sustenta os golden sets e os scripts de regressão da pasta `/evals`.

> *"Quem só lê o livro sai com método. Quem usa este repositório acrescenta implementação. Quem opera só com este repositório sem ler o livro opera no escuro."*

---

## Licença

| Componente | Licença |
|---|---|
| Código (scripts Python, notebooks, exemplos de agente, servidores MCP, `eval.py`) | [MIT](./LICENSE-MIT) |
| Conteúdo editorial (prompts em XML, golden sets, anti-padrões, métricas, documentação) | [CC-BY 4.0](./LICENSE-CC-BY) |

Você pode usar comercialmente, modificar, redistribuir e construir produtos derivados, desde que mantenha a atribuição a Fabio Garcia e à obra Inteligência Aumentada. A licença CC-BY 4.0 não exige share-alike, ou seja, o seu trabalho derivado pode ser proprietário.

---

## Sobre o autor

**Fabio Garcia** é CTO, Head de Tecnologia, autor da obra **Inteligência Aumentada** e operador brasileiro de IA em produção. Atua na intersecção entre engenharia de software, dados, IA, governança e liderança técnica, com foco em transformar caos em resultado através de pessoas, dados e tecnologia.

A obra **Inteligência Aumentada · Os Invariantes da IA** foi escrita como referência executiva em português para CTOs, AI engineers, executivos e operadores que precisam navegar a IA moderna sem cair nas armadilhas clássicas do hype. O livro entrega o método que sobrevive à próxima geração de modelos; este repositório entrega os artefatos que materializam o método em produção.

🔗 **Livros (grátis):** [Livro 1 — Os Invariantes da IA](https://github.com/falercia/inteligencia-aumentada-recursos/releases/latest) · [Livro 2 — Deep Claude](https://github.com/falercia/deep-claude/releases/latest)
🔗 **LinkedIn:** [linkedin.com/in/falercia](https://linkedin.com/in/falercia)
🔗 **Issues e contato editorial:** [github.com/falercia/inteligencia-aumentada-recursos/issues](https://github.com/falercia/inteligencia-aumentada-recursos/issues)

---

*Versão dos artefatos: junho de 2026.*
