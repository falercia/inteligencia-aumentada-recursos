# Caderno de Governança de IA, versão 1.0

> **Objetivo.** Modelo aplicável em até seis páginas, prometido pelo Framework Seis, Governança Indelegável. Substitui PDF morto por documento vivo, auditável, assinado pela diretoria, revisado trimestralmente.
> **Como usar.** Copie, customize para o contexto da sua organização, assine, publique internamente, revise a cada trimestre. Sem essas quatro ações, o caderno vira teatro.
> **Tempo estimado de preenchimento inicial.** Entre seis e doze horas de trabalho, distribuídas entre CTO, jurídico e DPO ou encarregado de proteção de dados.

---

## Página 1 — Identificação, escopo e princípios

### 1.1 Identificação

**Organização:** [nome legal]
**Data de emissão desta versão:** [DD/MM/AAAA]
**Versão:** v1.0
**Próxima revisão programada:** [DD/MM/AAAA] (trimestral)
**Patrocinador executivo (Accountable máximo):** [nome, cargo]
**Responsável operacional pelo caderno (Responsible):** [nome, cargo, e-mail]
**Aprovação:** assinaturas em página 6

### 1.2 Escopo

Este caderno cobre todo sistema, ferramenta, integração e processo que utilize Inteligência Artificial generativa, agêntica ou preditiva na operação da organização, incluindo modelos próprios, modelos de terceiros via API, modelos open weights operados on-prem, e produtos SaaS de terceiros que integrem IA como funcionalidade central.

Estão fora do escopo, salvo declaração explícita em revisão futura: ferramentas estatísticas tradicionais sem modelo de aprendizagem, automações de RPA sem componente de IA, sistemas legados sem IA embarcada.

### 1.3 Princípios condutores

A organização adota os Nove Princípios da obra como referência editorial, e converte os mais operacionais em compromissos auditáveis.

1. **Plausibilidade, não verdade.** Toda saída de IA é tratada como plausível, não verdadeira. Decisão crítica passa por verificação humana proporcional ao risco.
2. **Física da atenção.** Prompts produtivos respeitam ordem deliberada de blocos. Regra crítica nunca no meio.
3. **Camada dupla.** Padrão mora na cabeça, número mora em fonte datada. Decisão executiva consulta fonte na data.
4. **Encaixe específico.** Modelo é escolhido por eixo dominante da tarefa, não por reputação geral.
5. **Custo composto.** Otimização segue ordem T1 antes de T2 antes de T3.
6. **Propriedade do agente.** Nível de autonomia é função de observabilidade e reversibilidade, jamais de confiança subjetiva.
7. **Termômetro permanente.** Toda aplicação relevante tem eval contínuo, com base, meio e topo definidos.
8. **Responsabilidade indelegável.** Toda decisão de IA tem um Accountable humano único e nomeado.
9. **Operador como multiplicador.** A IA amplia competência e amplifica incompetência. Treinamento e calibração são parte do contrato com o operador.

### 1.4 Aplicabilidade do modelo e adendos setoriais

O caderno foi calibrado para organização brasileira entre cinquenta e cinco mil colaboradores, com uso de IA em produção em pelo menos um caso de uso material. Operação em setor criticamente regulado exige adendo setorial específico, que se anexa como camada adicional sem substituir o instrumento base.

| Adotar como está | Exige adendo setorial antes de adotar |
|---|---|
| Organização entre 50 e 5000 colaboradores em qualquer setor | Instituição financeira sob CMN 4658/2018 e regulação prudencial do Banco Central |
| Adoção primeira de governança formal de IA | Hospital ou operadora de saúde sob ANS, com prontuário tocado por IA |
| Operação multi-cloud com modelos próprios e de terceiros | Governo, autarquia ou empresa pública sob LGPD setorial e Marco Civil específico |
| Empresa que vende SaaS com IA embarcada como funcionalidade central | Operação em jurisdição não-brasileira com regulação distinta (EU AI Act, NIST AI RMF) |
| Empresa que adota IA de terceiros via API como ferramenta auxiliar | Operação com dado pessoal sensível em volume material sem DPO efetivo previamente nomeado |

---

## Página 2 — RACI e Comitê de IA

### 2.1 Matriz RACI por classe de decisão

A matriz abaixo cobre as classes de decisão recorrentes em operação de IA. Cada classe tem um único Accountable, sem exceção.

| Classe de decisão | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Adoção de novo caso de uso de IA | Líder do produto ou área | CTO | Jurídico, DPO, Segurança, Financeiro | Comitê de IA |
| Aprovação de fornecedor ou modelo de terceiros | Time de Engenharia | CTO | Jurídico, Segurança, Sourcing | Comitê de IA |
| Promoção de agente entre níveis de autonomia | AI Engineer responsável | CTO | Owner do produto, Operações, Segurança | Comitê de IA |
| Definição de RACI de caso específico | AI Engineer responsável | CTO | Owner do produto, RH se aplicável | Comitê de IA |
| Resposta a incidente de severidade alta | On-call responsável | CTO | DPO, Jurídico, Comunicação | Diretoria |
| Atualização do AUP de uso de IA | RH | CEO ou conselho | Jurídico, DPO, CTO | Toda organização |
| Revisão deste caderno | Comitê de IA | CEO | Diretoria | Toda organização |

### 2.2 Comitê de IA

O Comitê de IA é o órgão executivo permanente de governança. Não é fórum de debate filosófico.

**Composição mínima:** CTO ou Head de Tecnologia, DPO ou encarregado de dados, representante do Jurídico, representante de Segurança da Informação, representante de Operações.

**Cadência:** reunião mensal de uma hora, com pauta fixa de revisão de incidentes, novos casos de uso, revisão de RACI específicos, status do Apêndice J no contexto da organização, status do AUP.

**Mandato:** decidir sobre adoção de novo modelo, promover agente entre níveis de autonomia, aprovar exceções ao AUP, encaminhar incidentes severos à diretoria.

**Quórum mínimo:** três dos cinco membros, com obrigatoriedade da presença do CTO ou substituto formal.

**Ata:** toda reunião gera ata em até três dias úteis, com decisões, votação quando aplicável, próximos passos, responsáveis. Ata arquivada por cinco anos.

---

## Página 3 — Política de uso aceitável (AUP)

### 3.1 Princípios da política

Todo colaborador, prestador de serviço, parceiro com acesso a sistemas internos, está sujeito à AUP de IA da organização.

### 3.2 O que é permitido

1. Uso de ferramentas de IA aprovadas pelo Comitê de IA para tarefas profissionais, conforme lista atualizada na intranet.
2. Submissão de dados classificados como Públicos ou Internos a essas ferramentas, exceto quando contrato com cliente proibir.
3. Geração de conteúdo assistida por IA, desde que o operador humano revise e assuma a responsabilidade pela saída final.
4. Uso pessoal contido de IA em ferramentas pessoais, sem submissão de dado corporativo.

### 3.3 O que é proibido

1. Submeter dado pessoal sensível, segredo industrial, código proprietário, planilha financeira não publicada, contrato com cláusula de confidencialidade, comunicação privilegiada cliente-advogado, a ferramenta de IA não aprovada formalmente.
2. Confiar em saída de IA para decisão regulatória, jurídica, médica, financeira crítica, sem revisão humana qualificada.
3. Atribuir autoria humana a conteúdo gerado integralmente por IA quando a atribuição correta for relevante para o destinatário, por exemplo em parecer, artigo científico, peça processual.
4. Tentar contornar guardrails de modelo via prompt injection, jailbreak ou engenharia adversarial, exceto em contexto autorizado de red team.
5. Compartilhar credenciais, tokens ou chaves de API com pessoa não autorizada.
6. Implantar ferramenta de IA paralela à governança, prática conhecida como shadow AI.

### 3.4 Sanções

Descumprimento gera ação proporcional, conforme política de RH, podendo ir de advertência formal a desligamento por justa causa, e responsabilização civil e criminal nos casos previstos em lei.

### 3.5 Canal de dúvida

Toda dúvida sobre a aplicação da AUP é endereçada a [e-mail do Comitê de IA] ou ao canal correspondente na intranet. A resposta padrão sai em até cinco dias úteis.

---

## Página 4 — Dez controles canônicos com nível de maturidade

A organização adota os dez controles canônicos do Framework Seis. Cada controle tem maturidade autodeclarada entre zero e quatro, conforme tabela. Meta da organização para o final do ano: todos em maturidade três, dois em maturidade quatro.

**Escala de maturidade:** 0 = inexistente, 1 = ad hoc, 2 = documentado, 3 = monitorado, 4 = otimizado.

| # | Controle | Camada | Maturidade atual | Meta no horizonte de doze meses | Owner |
|---|---|---|---|---|---|
| 1 | Acesso por papel a sistemas de IA, com SSO e least privilege | Técnica | [ ] | 3 | Segurança |
| 2 | Auditoria imutável de chamadas a modelos, com retenção mínima de cinco anos | Técnica | [ ] | 3 | Engenharia |
| 3 | Kill switch testado em simulado trimestralmente | Técnica | [ ] | 4 | Engenharia |
| 4 | Rollback de prompt e versão de modelo em menos de quinze minutos | Técnica | [ ] | 4 | Engenharia |
| 5 | Observabilidade contínua com tracing, span, evento, métrica e alerta | Técnica | [ ] | 3 | Engenharia |
| 6 | Evals em CI bloqueadores, com base, meio e topo conforme F8 | Técnica | [ ] | 3 | Engenharia |
| 7 | RACI assinado por classe de decisão, conforme página 2 deste caderno | Operacional | [ ] | 3 | CTO |
| 8 | AUP de IA publicado, treinado em onboarding, revisado anualmente | Operacional | [ ] | 3 | RH e Jurídico |
| 9 | Plano de incidente com playbook, simulados semestrais, comunicação | Operacional | [ ] | 3 | Segurança |
| 10 | Comitê de IA ativo, com cadência mensal e ata pública internamente | Executiva | [ ] | 4 | CEO ou conselho |

A coluna de maturidade atual é preenchida no momento de assinatura deste caderno, com link para evidência anexada. Maturidade três sem artefato anexado vira maturidade um disfarçada na auditoria seguinte. A revisão da coluna é trimestral. Saltos de maturidade são reportados em ata. Quedas de maturidade exigem plano de remediação em sessenta dias.

---

## Página 5 — Plano de incidente e severidades

### 5.1 Classificação de severidade

| Severidade | Definição operacional | Tempo máximo de detecção | Tempo máximo de resposta | Quem responde |
|---|---|---|---|---|
| SEV-1 crítica | Dano material em curso a cliente, vazamento de dado pessoal sensível, geração massiva de conteúdo proibido, ataque ativo contra a infraestrutura | 15 minutos | 1 hora | On-call + CTO + DPO + Jurídico + Comunicação |
| SEV-2 alta | Degradação de qualidade que afeta cliente, drift relevante em produção, custo descontrolado em loop de agente | 1 hora | 4 horas | On-call + AI Engineer responsável + CTO |
| SEV-3 média | Degradação contida, alerta de drift sem impacto em cliente, falha de eval em release | 4 horas | 24 horas | AI Engineer responsável |
| SEV-4 baixa | Tema técnico de melhoria, débito conhecido | 1 semana | 30 dias | Backlog do produto |

### 5.2 Playbook resumido por classe

**SEV-1.** Ativar canal de incidente. Acionar kill switch se a fonte do dano for sistema de IA. Comunicar DPO e Jurídico em até trinta minutos. Comunicar cliente afetado em até duas horas. Notificar ANPD em até setenta e duas horas quando se aplicar o Artigo 48 da LGPD. Reunir comitê de crise em até uma hora. Postmortem sem culpa em até cinco dias úteis após contenção. Atualização do caderno em até dez dias úteis.

**SEV-2.** Ativar canal de incidente em modo reduzido. Investigar causa raiz com tracing. Aplicar rollback do prompt, do modelo ou da feature, conforme F7. Postmortem sem culpa em até dez dias úteis. Atualização do eval em CI em até cinco dias.

**SEV-3.** Investigação assíncrona pelo AI Engineer responsável. Registro em ferramenta de incidentes. Correção em release subsequente. Sem postmortem formal, salvo padrão recorrente.

**SEV-4.** Backlog do produto, priorização normal.

### 5.3 Simulado

Simulado de SEV-1 ocorre semestralmente, com cenário inédito comunicado a poucos membros do Comitê de IA. Avalia tempo de detecção, tempo de resposta, qualidade da comunicação, atualização do caderno. Relatório do simulado fica disponível à diretoria.

### 5.4 Comunicação externa

Comunicação externa em SEV-1 segue política única, com a regra de "primeiro contato em até duas horas, mesmo que parcial, e nunca mentir, omitir ou minimizar". Nota pública é assinada por porta-voz designado em ata do Comitê de IA.

---

## Página 6 — Assinaturas, anexos e revisão

### 6.1 Assinaturas

Este caderno é instrumento vivo de governança e exige assinatura da diretoria e do Comitê de IA para entrar em vigor. Revisão trimestral é obrigatória. Edições intermediárias são permitidas em situação de incidente.

| Nome | Cargo | Assinatura | Data |
|---|---|---|---|
| [CEO] | CEO | | |
| [CTO] | CTO | | |
| [DPO] | DPO ou encarregado | | |
| [CFO] | CFO | | |
| [Jurídico] | Jurídico ou Compliance | | |
| [Segurança] | Segurança da Informação | | |

### 6.2 Anexos referenciados

Os anexos abaixo são parte integrante do caderno e ficam em repositório controlado. Versionados conforme política de mudança da organização. Modelos clonáveis em `ANEXOS.md`.

1. **Lista de ferramentas de IA aprovadas**, atualizada continuamente pelo Comitê de IA.
2. **AUP completa**, com casos práticos e perguntas frequentes, publicada na intranet.
3. **Registro de RACI por caso de uso de IA em produção**, planilha controlada.
4. **Trilha do número da organização**, espelho interno do Apêndice J da obra, com preços negociados, contratos vigentes, posicionamento de risco.
5. **Catálogo de evals em produção**, com golden sets versionados e cobertura por caso de uso.
6. **Registro de incidentes**, com classificação por severidade e postmortems arquivados.

### 6.3 Política de revisão

Revisão trimestral em reunião do Comitê de IA. A revisão considera maturidade dos dez controles, incidentes do trimestre, mudanças regulatórias relevantes conforme Apêndice J da obra, novos casos de uso aprovados, atualização do AUP.

Edição intermediária permitida em três situações: SEV-1 com aprendizado relevante; mudança regulatória material; substituição de fornecedor ou modelo de fronteira em uso pela organização.

Toda edição registra três campos no log: data, item alterado, motivo. O log fica disponível ao conselho a qualquer momento.

### 6.4 Compromisso final

A diretoria, ao assinar este documento, compromete-se com a regra fundamental do Princípio Oito: toda decisão de IA tem um nome humano responsável. A IA executa. A responsabilidade tem dono. Quando alguém disser "foi a IA que decidiu", a organização precisa saber, em até cinco minutos, de quem é a cadeira.

---

*Caderno de Governança v1.0. Modelo aplicável. Use, assine, revise. Sem essas três ações, o documento vira teatro.*

*Próxima revisão programada: três meses a partir da data de assinatura.*
