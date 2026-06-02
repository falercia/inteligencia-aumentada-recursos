# Inteligência Aumentada · Recursos

> O número que muda. A Camada Dupla aplicada na prática.
> Companheiro executável do livro **Inteligência Aumentada · Os Invariantes da IA** (Fabio Garcia, 2026).

[![Status](https://img.shields.io/badge/vers%C3%A3o-v1.0.0-success)](#estado-atual)
[![Licença código](https://img.shields.io/badge/c%C3%B3digo-MIT-blue)](#licença)
[![Licença conteúdo](https://img.shields.io/badge/conte%C3%BAdo-CC--BY%204.0-lightgrey)](#licença)
[![Cadência](https://img.shields.io/badge/cad%C3%AAncia-mensal-success)](#cadência-pública-de-expansão)

---

## Por que este repositório existe

A obra **Inteligência Aumentada** opera sob o Princípio Três, a Camada Dupla, que afirma que conhecimento em IA vive em dois andares, o padrão que dura e o número que muda. O livro carrega o padrão — frameworks, arquiteturas, anti-padrões, vocabulário durável. Este repositório carrega o número — XML versionado de prompts, golden sets executáveis, scripts de regressão, changelog público mensal, exemplos rodáveis.

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
| 🔬 [`/evals`](./evals/) | Scripts de regressão executáveis, calibração de LLM-as-judge, padrões para CI/CD de prompts | Cap 39 Evals · F8 Pirâmide da Avaliação |
| 📦 [`/datasets`](./datasets/) | Golden sets em YAML/JSONL, prontos para serem carregados pelos scripts de eval | Cap 39 Evals · Cap 41 Alignment (adversarial sets) |
| 🤖 [`/agents`](./agents/) | Exemplos de agentes que compõem prompts da biblioteca em fluxos práticos | Cap 12 Agentes · Cap 40 LLMOps · F3 Escala de Propriedade do Agente |
| 🔌 [`/mcp`](./mcp/) | Servidores MCP de referência, minimalistas e auditáveis | Cap 13 MCP · F5 Matriz de Cobertura de Integrações |
| 📓 [`/notebooks`](./notebooks/) | Notebooks Python reproduzíveis para conceitos fundacionais | Cap 2 Como Modelos Funcionam · Cap 3 Tokens · Cap 4 Janela de Contexto |

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

**3. Quero contribuir.** Leia [CONTRATO.md](./CONTRATO.md) e abra uma issue com a categoria sugerida. Contribuições qualificadas com fonte primária são incorporadas na revisão mensal seguinte, com atribuição quando o contribuidor autoriza.

---

## Estado atual

**Versão v1.0.0 · publicada em junho de 2026.** Biblioteca completa com os 30 prompts em qualidade plena. A cadência mensal continua como compromisso público declarado, agora orientada à expansão das demais pastas (evals, datasets, agents, mcp, notebooks).

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

Esta postura segue o que a obra prega no Princípio Cinco, a Honestidade Temporal: a biblioteca chega ao público em estado fechado, mas com cadência pública declarada de revisão e contribuição. Cada caso do golden set carrega data de calibração, e cada prompt tem changelog próprio para registrar a iteração.

### Outras pastas

| Pasta | Estado |
|---|---|
| `/evals` | Stub estrutural · script `eval_runner.py` chega na v1.1.0 |
| `/datasets` | Stub estrutural · golden sets dos 30 prompts compilados em JSONL na v1.1.0 |
| `/agents` | Stub estrutural · primeiros agentes compostos na v1.3.0 |
| `/mcp` | Stub estrutural · primeiro servidor de referência na v1.4.0 |
| `/notebooks` | Stub estrutural · notebooks fundacionais na v1.2.0 |

---

## Cadência pública de expansão

O compromisso editorial é publicar release com nota datada **toda primeira semana do mês**, nos primeiros doze meses pós-lançamento da obra. A partir do décimo terceiro mês, a cadência passa a trimestral, salvo emergência regulatória ou técnica que justifique release fora de janela.

| Release | Janela | Escopo planejado |
|---|---|---|
| **v1.0.0** | **jun/2026** | **Biblioteca completa: 30 prompts em qualidade plena** |
| v1.1.0 | jul/2026 | `eval_runner.py` executável · golden sets compilados em JSONL |
| v1.2.0 | ago/2026 | Notebooks fundacionais (tokenização, contexto, embeddings, caching) |
| v1.3.0 | set/2026 | Primeiros agentes compostos (triagem, due diligence, customer success) |
| v1.4.0 | out/2026 | Primeiro servidor MCP de referência |
| v1.5.0 | nov/2026 | Adversarial sets · calibração estendida do LLM-as-judge |
| v2.0.0 | dez/2026 | Reorganização para inclusão dos prompts do Livro 2 |

Cada release vem com `CHANGELOG.md` versionado, indicando mudança item por item, motivo da mudança, e impacto observado em golden set ou em produção.

---

## Filosofia editorial

**Por que XML.** Modelos da família Claude foram treinados para reconhecer tags como delimitadores semânticos fortes, com aderência mensurável superior a markdown em testes A/B. Se você opera com outra família, substitua XML por marcadores equivalentes, mas mantenha a separação clara entre instrução e dado, que é a propriedade arquitetural que importa.

**Por que golden set.** Trocar prompt porque "ficou melhor" sem golden set é torcida, não decisão. O golden set é o equivalente da bateria de testes automatizados que qualquer engenheiro sênior exige antes de promover código, aplicado a saídas de IA que são não-determinísticas e por isso ainda mais perigosas sem instrumento de medida.

**Por que prefill.** Ancora o início da resposta no formato esperado, reduzindo a chance de o modelo divagar antes de entregar o conteúdo estruturado. O ganho é mensurável especialmente em saídas JSON e em fluxos com schema fechado.

**Por que self-critique.** Modelos longos perdem peso relativo das regras do início conforme a resposta cresce. Forçar uma rodada explícita de revisão antes de devolver o output recupera aderência à constituição em casos limítrofes onde o output direto fugiria do escopo.

**Por que cadência pública declarada.** Repositório acompanhante de livro que não atualiza vira folheto promocional. A cadência mensal nos primeiros doze meses é a forma de honrar a promessa da Camada Dupla, com a obra dizendo que o número muda e mostrando que o autor reserva tempo para manter o número atualizado.

---

## Como contribuir

Três tipos de contribuição são bem-vindos, em ordem decrescente de impacto:

**1. Calibração especialista do golden set.** Você é profissional sênior no domínio (advogado, médico, analista, RH, professor) e identifica caso limítrofe que o golden atual não cobre, ou divergência entre a saída esperada do golden e a prática profissional do seu campo. Abra issue com o template `golden-set-calibration` e descreva o caso, a saída esperada conforme sua prática, e a fonte primária quando aplicável.

**2. Correção de fato ou referência.** Você identificou referência jurisprudencial inexata, artigo de lei mal citado, paper com identificador errado, número de benchmark desatualizado. Abra issue com o template `factual-correction` e cite a fonte primária correta.

**3. Sugestão de novo prompt para a biblioteca.** Você identifica caso de uso recorrente que não está coberto pelos 30 prompts atuais. Abra issue com o template `new-prompt-suggestion` e descreva a dor, o domínio, e por que a biblioteca atual não resolve.

Todas as contribuições qualificadas com fonte primária ou validação por especialista são incorporadas na revisão mensal seguinte, com atribuição em `CONTRIBUTORS.md` quando o contribuidor autoriza.

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

🔗 **Livro:** disponível em formato digital e impresso · [link para venda em breve]
🔗 **LinkedIn:** [linkedin.com/in/falercia](https://linkedin.com/in/falercia)
🔗 **Issues e contato editorial:** [github.com/falercia/inteligencia-aumentada-recursos/issues](https://github.com/falercia/inteligencia-aumentada-recursos/issues)

---

*Última atualização: junho de 2026 · Próxima janela de release: julho de 2026.*
