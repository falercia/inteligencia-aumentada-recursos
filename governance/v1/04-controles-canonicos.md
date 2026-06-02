# Seção 4 — Dez controles canônicos com nível de maturidade

> Edição independente. Responsável: CTO em conjunto com segurança.
> Quando preenchida, vai para a página 4 do `00-modelo-caderno-completo.md`.

---

## 4.1 Escala de maturidade

A organização adota os dez controles canônicos do Framework Seis. Cada controle tem maturidade autodeclarada na escala abaixo, com **evidência anexada obrigatória** para autodeclaração acima do nível 1.

| Nível | Nome | Definição operacional |
|---|---|---|
| 0 | Inexistente | Controle não existe na organização |
| 1 | Ad hoc | Controle aplicado por iniciativa individual, sem padrão definido |
| 2 | Documentado | Controle descrito em política escrita, com responsável formal |
| 3 | Monitorado | Controle aplicado com métrica observável, com revisão periódica programada |
| 4 | Otimizado | Controle aplicado com automação, com melhoria contínua e meta de evolução |

Meta da organização para o final do ano: todos os controles em maturidade 3, com pelo menos dois controles em maturidade 4.

---

## 4.2 Os dez controles canônicos

| # | Controle | Camada | Maturidade atual | Meta em 12 meses | Owner | Evidência anexada |
|---|---|---|---|---|---|---|
| 1 | Acesso por papel a sistemas de IA, com SSO e least privilege | Técnica | [ ] | 3 | Segurança | [link] |
| 2 | Auditoria imutável de chamadas a modelos, com retenção mínima de cinco anos | Técnica | [ ] | 3 | Engenharia | [link] |
| 3 | Kill switch testado em simulado trimestralmente | Técnica | [ ] | 4 | Engenharia | [link] |
| 4 | Rollback de prompt e versão de modelo em menos de quinze minutos | Técnica | [ ] | 4 | Engenharia | [link] |
| 5 | Observabilidade contínua com tracing, span, evento, métrica e alerta | Técnica | [ ] | 3 | Engenharia | [link] |
| 6 | Evals em CI bloqueadores, com base, meio e topo conforme F8 | Técnica | [ ] | 3 | Engenharia | [link] |
| 7 | RACI assinado por classe de decisão, conforme seção 2 | Operacional | [ ] | 3 | CTO | [link] |
| 8 | AUP de IA publicado, treinado em onboarding, revisado anualmente | Operacional | [ ] | 3 | RH e Jurídico | [link] |
| 9 | Plano de incidente com playbook, simulados semestrais, comunicação | Operacional | [ ] | 3 | Segurança | [link] |
| 10 | Comitê de IA ativo, com cadência mensal e ata pública internamente | Executiva | [ ] | 4 | CEO ou conselho | [link] |

---

## 4.3 Detalhamento dos controles técnicos

### Controle 1 — Acesso por papel a sistemas de IA

**Definição.** Toda ferramenta de IA aprovada tem acesso controlado por SSO corporativo, com least privilege e segregação por papel. Acesso individual sem SSO é exceção registrada em ata.

**Evidência para maturidade 3.** Lista de ferramentas com integração SSO confirmada, política de acesso documentada, relatório trimestral de revisão de acessos.

### Controle 2 — Auditoria imutável de chamadas a modelos

**Definição.** Toda chamada a modelo em produção, tanto inferência quanto fine-tuning, gera log imutável com timestamp, identificador do chamador, hash do prompt, hash da resposta, modelo e versão. Retenção mínima de cinco anos.

**Evidência para maturidade 3.** Schema de auditoria documentado, política de retenção, exemplo de query auditável produzida para conselho.

### Controle 3 — Kill switch testado em simulado trimestralmente

**Definição.** Mecanismo que pausa imediatamente um sistema de IA em produção, com tempo máximo de execução de cinco minutos do acionamento à parada efetiva. Testado em simulado a cada trimestre.

**Evidência para maturidade 3.** Procedimento operacional escrito, registro de simulado com data e tempo medido, ata do Comitê de IA aprovando o relatório do simulado.

**Evidência para maturidade 4.** Tudo acima, mais kill switch automatizado por alerta de SEV-1 sem intervenção humana, com canal de aprovação pós-acionamento.

### Controle 4 — Rollback de prompt e modelo em menos de quinze minutos

**Definição.** Capacidade de reverter prompt em produção ou versão de modelo a estado anterior conhecido em menos de quinze minutos.

**Evidência para maturidade 3.** Sistema de versionamento documentado, procedimento de rollback escrito, registro de teste com tempo medido.

**Evidência para maturidade 4.** Tudo acima, mais rollback automatizado por gate de eval com falha crítica.

### Controle 5 — Observabilidade contínua

**Definição.** Sistema de IA em produção emite tracing distribuído com span por chamada de modelo, métrica de latência, custo e qualidade, evento de erro e alerta automatizado por desvio.

**Evidência para maturidade 3.** Dashboard ativo, política de alerta documentada, exemplo de incidente detectado e respondido com base em alerta automático.

### Controle 6 — Evals em CI bloqueadores

**Definição.** Pipeline de release contém suite de evals que bloqueia merge ou deploy quando o resultado regride abaixo do limiar declarado, conforme F8 Pirâmide da Avaliação.

**Evidência para maturidade 3.** Pipeline de CI documentado, suite de evals versionada, log de bloqueio com decisão registrada.

---

## 4.4 Detalhamento dos controles operacionais

### Controle 7 — RACI assinado por classe de decisão

**Definição.** Matriz RACI da seção 2 assinada e em vigor. Cada caso de uso de IA em produção tem RACI específico em anexo.

**Evidência para maturidade 3.** Matriz assinada, lista de casos de uso com RACI específico, taxa de cobertura nominal.

### Controle 8 — AUP publicado, treinado, revisado

**Definição.** AUP da seção 3 publicado, treinado em onboarding, revisado anualmente pelo Comitê de IA, com registro de aprovação por colaborador.

**Evidência para maturidade 3.** AUP em vigor com data de publicação, lista de treinamentos do ano, registro de aprovações.

### Controle 9 — Plano de incidente com playbook

**Definição.** Plano da seção 5 em vigor, com playbook por severidade, simulado semestral de SEV-1 executado, política de comunicação externa declarada.

**Evidência para maturidade 3.** Plano em vigor, registro do último simulado, ata do Comitê de IA aprovando o relatório.

---

## 4.5 Controle executivo

### Controle 10 — Comitê de IA ativo

**Definição.** Comitê da seção 2.3 com cadência mensal cumprida, ata em até três dias úteis, mandato escrito vigente.

**Evidência para maturidade 4.** Atas dos últimos doze meses arquivadas e disponíveis, lista de decisões deliberadas, taxa de quórum cumprido.

---

## 4.6 Política de saltos e quedas de maturidade

Saltos de maturidade são reportados em ata do Comitê de IA na reunião seguinte ao salto. Quedas de maturidade entre revisões trimestrais exigem plano de remediação em sessenta dias, com responsável nomeado e gate de retorno declarado.

Anti-padrão: organização que reporta o mesmo quadro de maturidade trimestre após trimestre sem alteração está sinalizando ou estagnação real, ou autodeclaração descalibrada. Em ambos os casos, é matéria de revisão pelo Comitê de IA.

---

*Seção 4 do Caderno de Governança v1.0. Edição independente pelo CTO em conjunto com segurança. Integra-se ao `00-modelo-caderno-completo.md` no momento da consolidação.*
