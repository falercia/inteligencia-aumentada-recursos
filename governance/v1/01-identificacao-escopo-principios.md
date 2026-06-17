# Seção 1 — Identificação, escopo e princípios

> Edição independente. Responsável: patrocinador executivo.
> Esta seção é a abertura do caderno. Quando preenchida na primeira passagem, vai para a página 1 do `00-modelo-caderno-completo.md`.

---

## 1.1 Identificação

**Organização:** [nome legal]
**CNPJ:** [00.000.000/0000-00]
**Data de emissão desta versão:** [DD/MM/AAAA]
**Versão:** v1.0
**Próxima revisão programada:** [DD/MM/AAAA] (trimestral)
**Patrocinador executivo (Accountable máximo):** [nome completo, cargo]
**Responsável operacional pelo caderno (Responsible):** [nome completo, cargo, e-mail corporativo]
**Aprovação:** assinaturas em `06-assinaturas-revisao.md`

> Anti-padrão a evitar: deixar o patrocinador executivo apenas como cargo ("CTO"). O caderno exige nome próprio. Sem nome, responsabilidade vira institucional, e institucional é eufemismo para ninguém.

---

## 1.2 Escopo

### O que este caderno cobre

Todo sistema, ferramenta, integração e processo que utilize Inteligência Artificial generativa, agêntica ou preditiva na operação da organização, incluindo:

- Modelos próprios treinados ou ajustados pela organização
- Modelos de terceiros consumidos via API (OpenAI, Anthropic, Google, Mistral, AWS Bedrock, Azure OpenAI, outros)
- Modelos open weights operados em infraestrutura própria, on-prem ou em nuvem privada
- Produtos SaaS de terceiros que integrem IA como funcionalidade central
- Agentes autônomos com qualquer nível de propriedade conforme F3
- Sistemas de classificação, ranqueamento, recomendação e detecção que usem IA

### O que está fora do escopo

Salvo declaração explícita em revisão futura:

- Ferramentas estatísticas tradicionais sem modelo de aprendizagem (planilhas, BI, modelos econométricos)
- Automações de RPA sem componente de IA
- Sistemas legados sem IA embarcada
- Componentes de IA de fornecedores que sejam pura comodity de infraestrutura (por exemplo, OCR genérico em pipeline de imagem)

### Mudanças de escopo

Mudança de escopo exige decisão registrada em ata do Comitê de IA, com justificativa, novo perímetro descrito, e atualização do caderno em até dez dias úteis.

---

## 1.3 Princípios condutores

A organização adota os Nove Invariantes da obra **Inteligência Aumentada · Os Invariantes da IA** como referência editorial, e converte os mais operacionais em compromissos auditáveis.

1. **Plausibilidade, não verdade.** Toda saída de IA é tratada como plausível, não verdadeira. Decisão crítica passa por verificação humana proporcional ao risco.
2. **Física da atenção.** Prompts produtivos respeitam ordem deliberada de blocos. Regra crítica nunca no meio.
3. **Camada dupla.** Padrão mora na cabeça, número mora em fonte datada. Decisão executiva consulta fonte na data.
4. **Encaixe específico.** Modelo é escolhido por eixo dominante da tarefa, não por reputação geral.
5. **Custo composto.** Otimização segue ordem T1 antes de T2 antes de T3.
6. **Propriedade do agente.** Nível de autonomia é função de observabilidade e reversibilidade, jamais de confiança subjetiva.
7. **Termômetro permanente.** Toda aplicação relevante tem eval contínuo, com base, meio e topo definidos.
8. **Responsabilidade indelegável.** Toda decisão de IA tem um Accountable humano único e nomeado.
9. **Operador como multiplicador.** A IA amplia competência e amplifica incompetência. Treinamento e calibração são parte do contrato com o operador.

Os invariantes não são preâmbulo decorativo. Aparecem operacionalizados em cada um dos blocos seguintes do caderno, e a auditoria do caderno se faz contra o invariante que sustenta cada controle.

---

## 1.4 Aplicabilidade do modelo e adendos setoriais

O caderno foi calibrado para organização brasileira entre cinquenta e cinco mil colaboradores, com uso de IA em produção em pelo menos um caso de uso material, e sem operação em setor criticamente regulado em que o regulador exija instrumento próprio.

| Adotar como está | Exige adendo setorial antes de adotar |
|---|---|
| Organização entre 50 e 5000 colaboradores em qualquer setor | Instituição financeira sob CMN 4658/2018 e regulação prudencial do Banco Central |
| Adoção primeira de governança formal de IA | Hospital ou operadora de saúde sob ANS, com prontuário tocado por IA |
| Operação multi-cloud com modelos próprios e de terceiros | Governo, autarquia ou empresa pública sob LGPD setorial e Marco Civil específico |
| Empresa que vende SaaS com IA embarcada como funcionalidade central | Operação em jurisdição não-brasileira com regulação distinta (EU AI Act, NIST AI RMF, regulação estadual EUA) |
| Empresa que adota IA de terceiros via API como ferramenta auxiliar | Operação com dado pessoal sensível em volume material sem DPO efetivo previamente nomeado |

O adendo setorial não substitui este caderno, ele se anexa como camada adicional sobre o instrumento base, e é o instrumento setorial que define o trecho específico, jamais o contrário, porque regulação setorial sobrescreve governança interna por princípio.

Quando o adendo setorial existir, o caderno declara o link para o instrumento em rodapé desta seção, com data da última atualização e nome do responsável operacional pelo adendo.

---

*Seção 1 do Caderno de Governança v1.0. Edição independente pelo patrocinador executivo. Integra-se ao `00-modelo-caderno-completo.md` no momento da consolidação para assinatura.*
