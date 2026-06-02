# Seção 3 — Política de uso aceitável (AUP)

> Edição independente. Responsável: RH em conjunto com jurídico, revisada pelo Comitê de IA.
> Quando preenchida, vai para a página 3 do `00-modelo-caderno-completo.md`.
> AUP completa, com casos práticos e FAQ, é publicada na intranet como anexo controlado (Anexo 2).

---

## 3.1 Princípios da política

Todo colaborador, prestador de serviço, parceiro com acesso a sistemas internos, está sujeito à AUP de IA da organização. A AUP é treinada em onboarding, divulgada anualmente em campanha de reforço, e revisada pelo Comitê de IA pelo menos uma vez ao ano.

A política não substitui o bom senso profissional, ela estabelece o piso comum auditável, e o operador maduro opera acima do piso porque entende o porquê de cada item.

---

## 3.2 O que é permitido

1. **Uso de ferramentas de IA aprovadas pelo Comitê de IA** para tarefas profissionais, conforme lista atualizada na intranet (Anexo 1).
2. **Submissão de dados classificados como Públicos ou Internos** a essas ferramentas, exceto quando contrato com cliente proibir.
3. **Geração de conteúdo assistida por IA**, desde que o operador humano revise e assuma a responsabilidade pela saída final.
4. **Uso pessoal contido de IA em ferramentas pessoais**, sem submissão de dado corporativo.

### 3.2.1 Exemplos práticos de uso permitido

- Rascunhar e-mail corporativo com IA e revisar antes de enviar
- Resumir reunião pública gravada em transcrição
- Gerar primeira versão de proposta comercial sobre informação pública do cliente
- Traduzir conteúdo público de marketing para outro idioma
- Apoio à programação em código aberto ou não-sensível com Copilot, Cursor, Claude Code, conforme lista aprovada

---

## 3.3 O que é proibido

1. **Submeter dado sensível a ferramenta não aprovada.** Dado pessoal sensível na acepção da LGPD, segredo industrial, código proprietário, planilha financeira não publicada, contrato com cláusula de confidencialidade, comunicação privilegiada cliente-advogado, em ferramenta de IA não aprovada formalmente.
2. **Confiar em saída de IA para decisão crítica sem revisão humana qualificada.** Decisão regulatória, jurídica, médica, financeira crítica, decisão de RH com impacto material em colaborador, decisão judicial.
3. **Atribuir autoria humana a conteúdo gerado integralmente por IA** quando a atribuição correta for relevante para o destinatário, por exemplo em parecer técnico, artigo científico, peça processual, prova acadêmica.
4. **Tentar contornar guardrails de modelo** via prompt injection, jailbreak ou engenharia adversarial, exceto em contexto autorizado de red team com escopo formal.
5. **Compartilhar credenciais, tokens ou chaves de API** com pessoa não autorizada.
6. **Implantar ferramenta de IA paralela à governança** sem submeter ao Comitê, prática conhecida como shadow AI.

### 3.3.1 Exemplos práticos de uso proibido

- Colar cláusula contratual com nome do cliente em ChatGPT pessoal para reescrever
- Submeter código proprietário inteiro em ferramenta gratuita pública
- Usar IA pessoal não-aprovada para responder ticket de suporte com dado de cliente
- Atribuir parecer jurídico gerado por IA como produzido por advogado sem revisão e ciência
- Configurar agente autônomo em produção sem submeter ao Comitê

---

## 3.4 Sanções

Descumprimento gera ação proporcional, conforme política de RH, podendo ir de:

| Gravidade | Sanção típica |
|---|---|
| Violação por desconhecimento, primeira ocorrência | Reforço de treinamento e advertência verbal registrada |
| Violação repetida ou por negligência | Advertência formal por escrito |
| Violação consciente com risco material | Suspensão e revisão de acesso a sistemas |
| Violação dolosa, com dano material ou exposição regulatória | Desligamento por justa causa e responsabilização civil e criminal nos casos previstos em lei |

A classificação da gravidade considera intenção, conhecimento prévio (treinamento documentado), magnitude do dano potencial ou realizado, e cooperação na resposta a incidente.

---

## 3.5 Canal de dúvida

Toda dúvida sobre a aplicação da AUP é endereçada a **[e-mail do Comitê de IA]** ou ao canal correspondente na intranet. A resposta padrão sai em até cinco dias úteis. Dúvida não-resolvida em cinco dias escala para o CTO automaticamente.

---

## 3.6 Treinamento

A AUP é treinada nas seguintes ocasiões obrigatórias:

- Onboarding de todo colaborador novo, no primeiro mês de casa
- Reforço anual de toda a organização, com aprovação registrada
- Treinamento adicional pós-incidente de SEV-1 ou SEV-2 que envolva uso indevido de IA

A trilha de treinamento e o registro de aprovações ficam em anexo controlado pelo RH.

---

*Seção 3 do Caderno de Governança v1.0. Edição independente por RH em conjunto com jurídico. Integra-se ao `00-modelo-caderno-completo.md` no momento da consolidação.*
