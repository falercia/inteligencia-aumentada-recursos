# Biblioteca de Prompts Profissionais — v1.0.0

Trinta prompts profissionais em qualidade plena, organizados por domínio.

## Padrão de adoção

1. **Clone o repositório.**
2. **Identifique o prompt mais próximo do seu domínio.**
3. **Copie o diretório inteiro** para seu repositório interno.
4. **Adapte a constituição** ao seu contexto.
5. **Construa seu golden set próprio** com pelo menos 20 casos do seu tráfego real.
6. **Rode `eval.py`** (a partir da release v1.1.0) antes de cada release.

## Estrutura de cada pasta

```
P-XXX-NN-slug/
├── README.md          ← ficha conceitual e instruções de uso
├── prompt.xml         ← XML completo
├── golden-set.yaml    ← 20 casos com input + saída esperada
├── anti-padroes.md    ← antipadrões observados
├── changelog.md       ← histórico do prompt
└── exemplos-saida/    ← outputs reais anonimizados
```

## Índice por domínio

### Jurídico (LEG)
- `P-LEG-01-clausula-nao-concorrencia-clt` — Revisão de cláusula de não-concorrência CLT
- `P-LEG-02-nda-lgpd-compliant` — Análise de NDA brasileiro LGPD-compliant
- `P-LEG-03-red-flags-contrato-ma` — Red flags em contrato M&A
- `P-LEG-04-parecer-compliance-lgpd` — Parecer sobre compliance LGPD

### Saúde (MED)
- `P-MED-01-triagem-sintomas` — Triagem de sintomas com recusa por escopo
- `P-MED-02-sumula-prontuario` — Súmula de prontuário
- `P-MED-03-interacao-medicamentosa` — Alerta de interação medicamentosa

### Financeiro (FIN)
- `P-FIN-01-anomalia-extrato` — Detecção de anomalia em extrato
- `P-FIN-02-risco-credito-pf` — Classificação de risco de crédito PF
- `P-FIN-03-sumula-itr` — Súmula de relatório trimestral ITR
- `P-FIN-04-analise-carteira` — Análise de carteira recomendada

### SaaS e Produto (SAAS)
- `P-SAAS-01-feature-request` — Classificação de feature request por persona
- `P-SAAS-02-sumula-nps` — Súmula de NPS qualitativo
- `P-SAAS-03-release-notes` — Geração de release notes
- `P-SAAS-04-churn-signal` — Análise de churn signal

### Suporte (SUP)
- `P-SUP-01-severidade-ticket` — Classificação de ticket em severidade
- `P-SUP-02-resposta-empatica` — Resposta empática a reclamação
- `P-SUP-03-escalonamento` — Decisão sobre escalonamento

### RH
- `P-RH-01-triagem-curriculo` — Triagem de currículo com fit
- `P-RH-02-feedback-360` — Análise de feedback 360
- `P-RH-03-descritivo-vaga` — Descritivo de vaga em linguagem inclusiva

### Marketing (MKT)
- `P-MKT-01-copy-ab` — Geração de copy A/B testável
- `P-MKT-02-brand-voice` — Análise de brand voice
- `P-MKT-03-sumula-pesquisa` — Súmula de pesquisa de mercado

### Educação (EDU)
- `P-EDU-01-plano-aula` — Geração de plano de aula
- `P-EDU-02-avaliacao-rubrica` — Avaliação rubrica-baseada
- `P-EDU-03-resposta-socratica` — Resposta socrática a dúvida do aluno

### Transversais (TR)
- `P-TR-01-extracao-json` — Extração estruturada com schema JSON
- `P-TR-02-multi-label` — Classificação multi-label
- `P-TR-03-recusa-fallback` — Recusa estruturada com fallback
