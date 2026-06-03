# `/prompts` — Biblioteca de prompts profissionais executáveis

> **Espelho rodável do Apêndice L do livro.** Cada prompt aqui é ativo de produção: XML versionado, golden set categorizado, anti-padrões observados, métrica de qualidade, changelog próprio. Não é template inspiracional; é o artefato que entra no pipeline real.

---

## Que problema esta pasta resolve

A maior parte das organizações que adota IA em produção em 2026 sofre do mesmo padrão de falha: **prompts vivem em documentos soltos, no Notion da pessoa que escreveu, com versionamento manual, sem golden set, sem regressão automatizada**. Quando o modelo muda, ninguém sabe se a qualidade subiu ou caiu. Quando o autor original sai da empresa, o prompt vira propriedade órfã. Quando o domínio evolui (mudança regulatória, jurisprudência nova, atualização de produto), o prompt fica obsoleto silenciosamente e ninguém percebe até o primeiro incidente.

A solução amadora é "criar uma pasta de prompts no repositório". A solução madura é **biblioteca disciplinada com cinco peças obrigatórias por prompt**: (1) XML executável estruturado sob a Engenharia de Prompt Estendida (Framework Quatro do livro), (2) golden set categorizado em fáceis, médios e limítrofes, (3) anti-padrões observados em prática real, (4) changelog datado para arqueologia editorial, (5) README com critério de quando usar e quando NÃO usar. **Esta pasta resolve isso na prática**, com 30 prompts em qualidade plena (publicados em v1.0.0) cobrindo 9 domínios profissionais, mais 3 calibrações dedicadas (publicadas em v1.1.1) que adicionam golden sets expandidos prontos para o motor de evals.

**Para quem é útil:** o AI Engineer que vai entrar com prompt em CI/CD na próxima semana e precisa de modelo de referência calibrado; o head de produto que quer saber se o prompt da sua equipe está em padrão de produção ou em padrão de PoC; o especialista de domínio (advogado, médico, suporte sênior) que quer contribuir com calibração por painel e ver seu trabalho virar referência para a comunidade brasileira de IA.

**O que você sai sabendo após explorar 1 prompt:** como é a estrutura completa de um ativo de produção, como o golden set categoriza casos por dificuldade, onde adaptar a constituição ao seu próprio contexto, e o que o changelog versionado revela sobre a evolução editorial do prompt.

---

## Ficha técnica

| Campo | Valor |
|---|---|
| **Padrão arquitetural** | Engenharia de Prompt Estendida (Framework Quatro do livro) |
| **Estrutura de cada prompt** | XML em `prompt.xml` + golden em `golden-set.yaml` + anti-padrões + changelog + README |
| **Total publicado** | 30 prompts em qualidade plena (v1.0.0) + 3 calibrações dedicadas (v1.1.1) |
| **Cobertura por domínio** | Jurídico (4), Saúde (3), Financeiro (4), SaaS (4), Suporte (3), RH (3), Marketing (3), Educação (3), Transversais (3) |
| **Judges suportados** | substring, regex, json_schema, classification (via `/evals/eval_runner.py`) |
| **Modelos sugeridos** | Triagem em CI: Haiku · Release público: Sonnet · Auditoria editorial: Opus |
| **Licença do XML e do golden** | CC-BY 4.0 (uso comercial permitido com atribuição) |

---

## Os 30 prompts da biblioteca

### Jurídico (4)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-LEG-01-clausula-nao-concorrencia-clt`](./P-LEG-01-clausula-nao-concorrencia-clt/) | Cláusula de não-concorrência CLT | Triagem TST: temporal, geográfico, material, contraprestação, interesse legítimo |
| [`P-LEG-02-nda-lgpd-compliant`](./P-LEG-02-nda-lgpd-compliant/) | NDA com aderência à LGPD | Revisão e geração de NDA com cláusulas de tratamento de dados pessoais |
| [`P-LEG-03-red-flags-contrato-ma`](./P-LEG-03-red-flags-contrato-ma/) | Red flags em contrato M&A | Triagem de cláusulas críticas em due diligence |
| [`P-LEG-04-parecer-compliance-lgpd`](./P-LEG-04-parecer-compliance-lgpd/) | Parecer estruturado de compliance LGPD | Análise de aderência regulatória com cite de fonte primária |

### Saúde (3)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-MED-01-triagem-sintomas`](./P-MED-01-triagem-sintomas/) | Triagem clínica básica (Manchester) | Classificação de urgência em 4 tiers azul/verde/amarelo/vermelho |
| [`P-MED-02-sumula-prontuario`](./P-MED-02-sumula-prontuario/) | Súmula estruturada de prontuário | Extração de história clínica + exames + condutas em formato auditável |
| [`P-MED-03-interacao-medicamentosa`](./P-MED-03-interacao-medicamentosa/) | Triagem de interação medicamentosa | Identificação de interações conhecidas com nível de evidência |

### Financeiro (4)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-FIN-01-anomalia-extrato`](./P-FIN-01-anomalia-extrato/) | Detecção de anomalia em extrato | Triagem de transações suspeitas com justificativa |
| [`P-FIN-02-risco-credito-pf`](./P-FIN-02-risco-credito-pf/) | Score de risco de crédito PF | Análise estruturada com pontuação e fatores explicáveis |
| [`P-FIN-03-sumula-itr`](./P-FIN-03-sumula-itr/) | Súmula de ITR (Informações Trimestrais) | Extração de números-chave + variações YoY com fonte |
| [`P-FIN-04-analise-carteira`](./P-FIN-04-analise-carteira/) | Análise consolidada de carteira | Exposição, concentração, recomendações |

### SaaS (4)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-SAAS-01-feature-request`](./P-SAAS-01-feature-request/) | Classificação de feature request | Triagem em backlog com prioridade calibrada |
| [`P-SAAS-02-sumula-nps`](./P-SAAS-02-sumula-nps/) | Súmula de NPS qualitativo | Extração de temas + sentimento + ações sugeridas |
| [`P-SAAS-03-release-notes`](./P-SAAS-03-release-notes/) | Release notes a partir de PR | Geração estruturada por audiência (cliente / interno) |
| [`P-SAAS-04-churn-signal`](./P-SAAS-04-churn-signal/) | Detecção de sinal de churn | Classificação de cliente em risco com justificativa |

### Suporte (3)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-SUP-01-severidade-ticket`](./P-SUP-01-severidade-ticket/) | Classificação de severidade de ticket | Triagem em 4 níveis com encaminhamento |
| [`P-SUP-02-resposta-empatica`](./P-SUP-02-resposta-empatica/) | Resposta empática em SAC | Geração de resposta com tom adequado |
| [`P-SUP-03-escalonamento`](./P-SUP-03-escalonamento/) | Decisão de escalonamento | Identificação de quando subir para humano sênior |

### RH (3)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-RH-01-triagem-curriculo`](./P-RH-01-triagem-curriculo/) | Triagem de currículo | Score com rubrica anti-viés calibrada |
| [`P-RH-02-feedback-360`](./P-RH-02-feedback-360/) | Consolidação de feedback 360° | Síntese de múltiplas avaliações com ações sugeridas |
| [`P-RH-03-descritivo-vaga`](./P-RH-03-descritivo-vaga/) | Descritivo de vaga padronizado | Geração com cobertura anti-viés + accessibility |

### Marketing (3)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-MKT-01-copy-ab`](./P-MKT-01-copy-ab/) | Variantes A/B de copy | Geração com justificativa de cada variante |
| [`P-MKT-02-brand-voice`](./P-MKT-02-brand-voice/) | Aderência a brand voice | Triagem de texto contra guia de marca |
| [`P-MKT-03-sumula-pesquisa`](./P-MKT-03-sumula-pesquisa/) | Súmula de pesquisa de mercado | Extração de insights + recomendações |

### Educação (3)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-EDU-01-plano-aula`](./P-EDU-01-plano-aula/) | Plano de aula estruturado | Geração com objetivos, atividades, avaliação |
| [`P-EDU-02-avaliacao-rubrica`](./P-EDU-02-avaliacao-rubrica/) | Avaliação por rubrica | Análise critério a critério antes do consolidado |
| [`P-EDU-03-resposta-socratica`](./P-EDU-03-resposta-socratica/) | Resposta socrática (não dá a resposta) | Sequência de perguntas que guia o aluno |

### Transversais (3)

| ID | Nome | Caso de uso |
|---|---|---|
| [`P-TR-01-extracao-json`](./P-TR-01-extracao-json/) | Extração de campos para JSON | Schema-first com self-critique de schema |
| [`P-TR-02-multi-label`](./P-TR-02-multi-label/) | Classificação multi-label | Cobertura simultânea de N categorias |
| [`P-TR-03-recusa-fallback`](./P-TR-03-recusa-fallback/) | Recusa elegante e fallback | Detecção de fora de escopo + encaminhamento |

### Calibrações dedicadas (v1.1.1)

Três prompts publicados em v1.0.0 receberam, em v1.1.1, calibrações dedicadas com golden sets expandidos prontos para o motor de evals do repositório:

| Pasta | Conteúdo |
|---|---|
| [`P-LEG-01/`](./P-LEG-01/) | `eval.config.yaml` + `golden.yaml` (20 casos calibrados) — calibração editorial inicial do autor para uso em `eval_runner.py` |
| [`P-MED-01/`](./P-MED-01/) | `eval.config.yaml` + `golden.yaml` (20 casos calibrados) |
| [`P-SUP-01/`](./P-SUP-01/) | `eval.config.yaml` + `golden.yaml` (20 casos calibrados) |

As pastas com nomenclatura curta (`P-LEG-01`, `P-MED-01`, `P-SUP-01`) coexistem com as pastas descritivas (`P-LEG-01-clausula-nao-concorrencia-clt` etc.) porque servem propósitos diferentes: a pasta descritiva carrega o XML completo + golden inicial + anti-padrões + changelog; a pasta curta carrega a configuração de eval + golden expandido para execução automatizada via `/evals/eval_runner.py`. Em release futuro, as duas serão consolidadas em estrutura unificada.

---

## Como usar um prompt em 60 segundos

```bash
# 1. Entre na pasta do prompt do seu interesse (use a versão descritiva)
cd prompts/P-LEG-01-clausula-nao-concorrencia-clt/

# 2. Inspecione os artefatos
cat README.md             # dor que resolve, quando usar, quando NÃO usar
head -100 prompt.xml      # XML executável (persona, constituição, contexto, formato, prefill, self-critique)
head -50 golden-set.yaml  # golden set categorizado
cat anti-padroes.md       # padrões de falha observados + métrica
cat changelog.md          # arqueologia editorial

# 3. Para rodar contra o motor de evals (use a pasta de calibração curta)
cd ../..
python evals/eval_runner.py --prompt P-LEG-01 --model claude-haiku-4-5

# 4. Resultado fica em evals/reports/ com nota por critério, tabela e CSV exportável
```

A partir daqui, três caminhos:
- **Quero entender o método antes de adotar** → leia o `README.md` da pasta do prompt + a ficha conceitual correspondente no APX-L do livro.
- **Quero adotar este prompt na minha organização** → copie a pasta inteira (descritiva) para o seu repositório interno, adapte a constituição ao seu contexto, construa golden próprio com casos representativos do seu tráfego real, rode `eval_runner.py` antes de cada release.
- **Quero contribuir com calibração especialista** → abra issue com `golden-set-calibration` no template e descreva o caso limítrofe que você identificou.

---

## Anatomia do XML — Framework Quatro

Todo prompt aqui segue cinco blocos posicionais obrigatórios, na ordem exata:

| Bloco | Função | Por que está nesta posição |
|---|---|---|
| `<persona>` | Define quem o modelo é, com tom e padrão profissional | Primeiro porque ancora vocabulário e nível de exigência da resposta inteira |
| `<constituicao>` | Regras invioláveis do prompt | Cedo no contexto porque modelos priorizam instruções recentes em outputs longos; reiteradas no fim quando crítico |
| `<contexto>` | Variáveis nomeadas com o dado dinâmico da chamada | No meio porque é o que muda a cada chamada; o modelo precisa do dado depois das regras |
| `<tarefa>` | O que se pede ao modelo, com escopo explícito | Depois do contexto porque a tarefa opera sobre o dado disponível |
| `<formato_saida>` | Schema da saída, em markdown ou JSON | Por último porque é o "como devolver", aplicado ao que foi pedido |

Dois blocos adicionais aparecem nos prompts em qualidade plena:

- **`<prefill>`** — ancora o início da resposta no formato esperado, reduzindo divagação. Ganho mensurável em outputs JSON e em fluxos com schema fechado.
- **`<self_critique>`** — força rodada explícita de revisão contra a constituição antes do output final. Recupera aderência em casos limítrofes onde o output direto fugiria do escopo.

O XML foi escolhido porque modelos da família Claude foram treinados para reconhecer tags como delimitadores semânticos fortes, com aderência mensurável superior a markdown em testes A/B. Quem opera com outra família pode substituir XML por marcadores equivalentes, desde que mantenha a separação clara entre instrução e dado — propriedade arquitetural que importa mais do que a sintaxe.

---

## Estrutura de cada pasta de prompt (descritiva)

```
P-LEG-01-clausula-nao-concorrencia-clt/  ← nomenclatura: ID + slug descritivo
├── README.md          ← dor que resolve, quando usar, quando NÃO usar, conexão com APX-L
├── prompt.xml         ← XML completo (5 blocos + prefill + self-critique)
├── golden-set.yaml    ← golden set categorizado (fáceis / médios / limítrofes)
├── anti-padroes.md    ← padrões de falha observados + métrica de qualidade
└── changelog.md       ← arqueologia editorial do prompt
```

---

## Convite à calibração por painel especialista

A obra propõe que prompts em domínio sensível (jurídico, médico, financeiro) sejam **calibrados por painel especialista**, e não apenas pelo autor. A calibração inicial dos 30 prompts foi feita pelo autor com base em prática profissional do domínio; especialistas sêniores em qualquer dos 9 domínios são convidados a:

1. **Identificar caso limítrofe** que o golden atual não cobre.
2. **Validar coerência** entre saída esperada do golden e prática profissional do seu campo.
3. **Apontar antipadrão** observado em sua operação que não está documentado.
4. **Sugerir refinamento** da constituição para cobrir nuance específica do domínio brasileiro.

Abra issue com o template `golden-set-calibration` declarando domínio, anos de experiência e tipo de contribuição. O autor coordena a revisão; trabalho aceito é creditado em [`CONTRIBUTORS.md`](../CONTRIBUTORS.md).

---

## Por que esta disciplina toda

**Por que golden set por prompt.** Trocar prompt porque "ficou melhor" sem golden set é torcida, não decisão. O golden set é o equivalente da bateria de testes automatizados que qualquer engenheiro sênior exige antes de promover código, aplicado a saídas de IA que são não-determinísticas e por isso ainda mais perigosas sem instrumento de medida.

**Por que prefill.** Ancora o início da resposta no formato esperado, reduzindo a chance de o modelo divagar antes de entregar o conteúdo estruturado. Ganho mensurável especialmente em saídas JSON e em fluxos com schema fechado.

**Por que self-critique.** Modelos longos perdem peso relativo das regras do início conforme a resposta cresce. Forçar uma rodada explícita de revisão contra a constituição recupera aderência em casos limítrofes onde o output direto fugiria do escopo.

**Por que anti-padrões documentados.** Cada anti-padrão registrado é uma cicatriz operacional convertida em conhecimento durável. O próximo operador que encontrar o mesmo problema não precisa pagar o mesmo preço.

**Por que changelog versionado.** Sem arqueologia editorial, quem chega depois não sabe por que a constituição foi reescrita, por que o golden ganhou casos, por que o prefill mudou. Com changelog, o prompt vira ativo institucional que sobrevive ao autor original.

---

## Conexão com o livro

- 🔗 [**Apêndice L — Biblioteca de Prompts Profissionais**](../../Livro-1-Os-Invariantes/04-apendices/L1-APX-L-biblioteca-prompts.md) — fichas conceituais das 30 dores resolvidas, anatomia, anti-padrões e métricas
- 🔗 [**Capítulo 9 — Engenharia de Prompt**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C09-engenharia-prompt.md) — fundação conceitual
- 🔗 [**Framework F4 — Engenharia de Prompt Estendida**](../../Livro-1-Os-Invariantes/03-frameworks/L1-F4-prompt-ext.md) — anatomia em 5 blocos que estrutura todo prompt aqui
- 🔗 [**Capítulo 21 — Evals**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C21-evals.md) — por que golden set, judges e regressão automatizada são parte do contrato
- 🔗 [**Framework F8 — Pirâmide da Avaliação**](../../Livro-1-Os-Invariantes/03-frameworks/L1-F8-piramide-aval.md) — o método que sustenta os judges integrados ao `eval_runner.py`

---

> *"Prompt sem golden set é torcida com confiança. Prompt com golden set calibrado por painel especialista é ativo que sobrevive à troca de modelo, à saída do autor e à evolução do domínio. A diferença não é técnica; é disciplina editorial aplicada a um artefato que muita gente trata como rascunho."*
