# A03 — Orquestrador-Especialistas (🚧 STUB)

> **Status atual: stub estrutural.** Implementação completa prevista para um release futuro. Este README declara o que vai entrar e por quê, conforme Princípio 5 — Honestidade Temporal.

---

## Que problema este agente vai resolver

Existe uma família inteira de tarefas executivas que **excede a capacidade de um único agente**, não porque o modelo é fraco, mas porque a tarefa exige especialização em domínios diferentes ao mesmo tempo. Análise de viabilidade de aquisição precisa de leitura jurídica de contrato, análise financeira de balanço e análise comercial de carteira de clientes — três disciplinas que, em humanos, ficam em três cargos distintos com cinco a quinze anos de trabalho focado cada um.

Forçar um único agente generalista a fazer as três análises produz três respostas medianas. A solução clássica é **multiagente em estrela**: um coordenador decompõe a tarefa, delega cada parte a um sub-agente especialista, e consolida no final. **A03 vai resolver isso usando os próprios prompts profissionais já versionados em `/prompts`** como cérebros dos especialistas, sem reescrever cada um do zero.

**Caso de uso canônico que vai estar implementado:** parecer executivo de uma página para o conselho avaliar aquisição de uma empresa-alvo, com decomposição em três análises paralelas. **Para quem vai ser útil:** time de M&A, jurídico corporativo, FP&A, qualquer área que precise produzir parecer integrado a partir de múltiplas leituras especialistas em prazo curto.

---

## O que este agente será

Sistema multiagente em padrão **estrela** (orquestrador-especialistas): um agente coordenador recebe uma tarefa complexa, decompõe em subtarefas, delega cada subtarefa a um sub-agente especializado, e consolida as respostas em uma saída final coesa. Os sub-agentes especializados reusam, sem reescrever, os prompts profissionais da pasta [`/prompts`](../../prompts/) deste mesmo repositório.

A demonstração canônica vai ser uma análise jurídico-financeira combinada:

> Cliente solicitou análise de viabilidade para aquisição de empresa-alvo. Avalie em paralelo: (1) cláusulas críticas do contrato de aquisição [especialista jurídico, reusa P-LEG-02], (2) saúde financeira da empresa-alvo a partir do balanço anexo [especialista financeiro, reusa P-FIN-01], (3) risco de continuidade contratual com clientes-chave [especialista comercial, reusa P-SAA-02]. Consolide em parecer executivo de uma página para o conselho.

---

## Por que padrão estrela e por que reusar prompts

A escolha de padrão estrela em vez de pipeline sequencial é deliberada: permite **paralelismo real** quando as subtarefas são independentes, e centraliza a consolidação em um único ponto auditável (o orquestrador). Padrões mais sofisticados — debate (A04), grafos com ciclos, hierarquia profunda — ficam para releases futuros.

A escolha de reusar prompts profissionais da pasta `/prompts` em vez de definir prompts ad hoc dentro do agente é a aplicação da **Camada Dupla** ao código: o prompt é ativo durável versionado em `/prompts/P-LEG-02/`; o agente é o consumidor descartável. Mudar a versão do prompt não exige refatorar o agente, e o golden set associado ao prompt continua valendo como eval.

---

## Estrutura prevista

```
a03-orquestrador-especialistas/
├── README.md                          ← este arquivo
├── agent.py                           ← entry point com CLI
├── system_prompt_orquestrador.md      ← constituição do coordenador
├── especialistas/
│   ├── juridico.py                    ← wrapper que carrega P-LEG-02 e expõe como tool
│   ├── financeiro.py                  ← wrapper que carrega P-FIN-01 e expõe como tool
│   └── comercial.py                   ← wrapper que carrega P-SAA-02 e expõe como tool
├── consolidador.py                    ← lógica de merge das respostas dos especialistas
├── exemplos/
│   ├── caso-aquisicao.md              ← caso completo, com input e saída esperada
│   └── caso-due-diligence.md          ← variação para due diligence simplificada
├── eval/
│   └── golden-set.jsonl               ← compilação dos golden sets dos prompts reusados
└── kill_switch.py
```

---

## Nível F3 esperado

**Supervisionado.** Operação em lote, sem gate por subtarefa, mas com:
- Trace consolidado por subtarefa (cada especialista produz um span)
- Eval automatizado contra o golden set unificado
- Kill switch que aborta toda a operação a qualquer momento
- Limite de fan-out para proteger custo (máx. 5 especialistas por execução)

---

## Por que NÃO está pronto em v1.2.0

A implementação exige decisões adicionais que merecem sessão dedicada de design, em vez de serem improvisadas:

1. **Como passar contexto do orquestrador para o especialista sem inflar tokens** (uso de IDs de referência em vez de duplicar conteúdo — aplicação direta do C18 Economia de Tokens)
2. **Como o consolidador identifica contradições entre especialistas** (sinaliza para revisão humana em vez de mascarar)
3. **Como o golden set unificado combina os golden sets individuais** dos prompts reusados (sem inflar nem perder cobertura)
4. **Como o kill switch propaga para sub-agentes em execução** (cancelamento limpo vs. interrupção abrupta)

Cada decisão acima vale uma seção do README final, e cada decisão tomada às pressas vira anti-padrão didático em vez de exemplo de referência. Estamos seguindo a regra do livro: melhor stub honesto declarado do que implementação rasa com aparência de completa.

---

## Conexão com o livro (a ser ampliada no release final)

- 🔗 [Capítulo 12 — Agentes de IA](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C12-agentes.md), seção sobre padrões multiagente
- 🔗 [Framework F3 — Escala de Propriedade](../../../Livro-1-Os-Invariantes/03-frameworks/L1-F3-agente-prop.md)
- 🔗 [Pasta `/prompts`](../../prompts/) — fonte dos especialistas reusados
- 🔗 [Capítulo 18 — Economia de Tokens](../../../Livro-1-Os-Invariantes/02-capitulos/L1-C18-economia-tokens.md) — disciplina obrigatória para padrão estrela

---

> *Stub é declaração honesta do que existe e do que ainda não existe. Quando a implementação ficar pronta, este README é substituído por documentação completa do agente em operação.*
