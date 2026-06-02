# Seção 5 — Plano de incidente e severidades

> Edição independente. Responsável: segurança em conjunto com jurídico.
> Quando preenchida, vai para a página 5 do `00-modelo-caderno-completo.md`.

---

## 5.1 Classificação de severidade

| Severidade | Definição operacional | Tempo máximo de detecção | Tempo máximo de resposta | Quem responde |
|---|---|---|---|---|
| **SEV-1 crítica** | Dano material em curso a cliente, vazamento de dado pessoal sensível, geração massiva de conteúdo proibido, ataque ativo contra a infraestrutura | 15 minutos | 1 hora | On-call + CTO + DPO + Jurídico + Comunicação |
| **SEV-2 alta** | Degradação de qualidade que afeta cliente, drift relevante em produção, custo descontrolado em loop de agente | 1 hora | 4 horas | On-call + AI Engineer responsável + CTO |
| **SEV-3 média** | Degradação contida, alerta de drift sem impacto em cliente, falha de eval em release | 4 horas | 24 horas | AI Engineer responsável |
| **SEV-4 baixa** | Tema técnico de melhoria, débito conhecido | 1 semana | 30 dias | Backlog do produto |

### 5.1.1 Como customizar a classificação ao SLA do negócio

Os tempos máximos acima são piso para organização de porte médio sem SLA estendido a cliente. Empresa com SLA contratual estrito de quinze minutos para incidente material precisa reduzir o tempo máximo de resposta de SEV-1 a alinhamento contratual, com decisão registrada em ata do Comitê de IA.

Empresa sob regulação setorial (financeiro, saúde) precisa cruzar a classificação com a definição setorial de incidente material, e adotar o tempo mais restritivo dos dois.

---

## 5.2 Playbook resumido por classe

### SEV-1 crítica

1. **Ativar canal de incidente** (chat dedicado, conf call) em até cinco minutos da detecção
2. **Acionar kill switch** se a fonte do dano for sistema de IA, conforme controle 3
3. **Comunicar DPO e Jurídico** em até trinta minutos
4. **Comunicar cliente afetado** em até duas horas, com primeira nota mesmo que parcial
5. **Notificar ANPD** em até setenta e duas horas quando se aplicar o Artigo 48 da LGPD
6. **Reunir comitê de crise** em até uma hora
7. **Postmortem sem culpa** em até cinco dias úteis após contenção
8. **Atualização do caderno** em até dez dias úteis, com revisão de controles aplicáveis

### SEV-2 alta

1. **Ativar canal de incidente** em modo reduzido
2. **Investigar causa raiz** com tracing distribuído (controle 5)
3. **Aplicar rollback** do prompt, do modelo ou da feature, conforme F7 e controle 4
4. **Postmortem sem culpa** em até dez dias úteis
5. **Atualização do eval em CI** em até cinco dias (controle 6)

### SEV-3 média

1. Investigação assíncrona pelo AI Engineer responsável
2. Registro em ferramenta de incidentes
3. Correção em release subsequente
4. Sem postmortem formal, salvo padrão recorrente

### SEV-4 baixa

1. Backlog do produto, priorização normal

---

## 5.3 Simulado

Simulado de SEV-1 ocorre semestralmente, com cenário inédito comunicado a poucos membros do Comitê de IA. Avalia:

- Tempo de detecção
- Tempo de resposta
- Qualidade da comunicação interna e externa
- Aderência ao playbook
- Atualização do caderno pós-simulado

Relatório do simulado fica disponível à diretoria e é fonte de evidência para a maturidade do controle 3 e do controle 9.

### 5.3.1 Cenários típicos de simulado

- Vazamento simulado de dado pessoal sensível via output não-sanitizado de modelo
- Geração massiva de conteúdo violando AUP por jailbreak novo descoberto
- Custo de inferência multiplicado por dez em loop não-controlado de agente
- Drift súbito de qualidade em prompt crítico após atualização silenciosa de modelo
- Comprometimento de credencial de API de provedor de modelo

A escolha do cenário cabe ao Comitê de IA, com objetivo de revezar tipos de incidente e manter o time fora da zona de conforto.

---

## 5.4 Comunicação externa

Comunicação externa em SEV-1 segue política única, com a regra de **"primeiro contato em até duas horas, mesmo que parcial, e nunca mentir, omitir ou minimizar"**. Nota pública é assinada por porta-voz designado em ata do Comitê de IA.

A nota inclui:

- O que aconteceu, em descrição factual
- Quem foi afetado e em que extensão conhecida
- O que a organização fez nas primeiras horas
- O que será comunicado em atualização seguinte, com janela temporal

Não inclui:

- Especulação sobre causa antes da investigação concluída
- Atribuição de culpa a fornecedor, modelo ou cliente
- Compromisso de prazo de resolução sem base técnica

A política de comunicação externa é coordenada com Marketing, Comunicação Corporativa e RI quando aplicável.

---

## 5.5 Postmortem sem culpa

O postmortem segue o modelo padrão do setor, com cinco seções:

1. **Linha do tempo** com timestamps detalhados
2. **Causa raiz** com análise de cinco porquês ou equivalente
3. **Impacto** com clientes afetados, dado exposto, custo gerado
4. **O que funcionou e o que falhou** em controles e processo
5. **Ações corretivas** com responsável e prazo, e gate de fechamento

A regra do "sem culpa" é editorial: o postmortem não atribui culpa a pessoa, atribui falha a sistema, processo ou controle, e gera ação corretiva sobre o sistema. Pessoa só entra no postmortem se houve violação dolosa da AUP, e nesse caso é matéria separada conduzida por RH.

---

*Seção 5 do Caderno de Governança v1.0. Edição independente por segurança em conjunto com jurídico. Integra-se ao `00-modelo-caderno-completo.md` no momento da consolidação.*
