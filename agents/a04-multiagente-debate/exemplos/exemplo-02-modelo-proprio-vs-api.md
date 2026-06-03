# Exemplo 2 — Modelo próprio vs API (debate executivo C-level)

## Comando

```bash
python agent.py \
  --question "Em uma fintech regulada brasileira de 800 colaboradores, com pipeline de IA gastando hoje USD 35 mil/mês em API da Anthropic, devo migrar para deploy próprio de Llama 3.3 em GPU H100 alugada na AWS, ou manter a API?" \
  --thesis-a "Manter a API é o caminho dominante (custo + tempo até valor)." \
  --thesis-b "Migrar para deploy próprio é o caminho dominante (controle + custo unitário a longo prazo)." \
  --rounds 2 \
  --verbose
```

## O que este debate cobra

Este é o debate clássico de comitê arquitetural em 2026. O proponente da API foca em:
- Velocidade de adoção (zero infraestrutura nova)
- Acesso à fronteira (Sonnet 4.6, Opus quando precisa, mudança de modelo sem refazer pipeline)
- Compliance maduro (a Anthropic tem DPA, certificações, contratos com cláusula brasileira)

O oponente do deploy próprio foca em:
- Custo composto a longo prazo (USD 35k/mês × 12 = USD 420k/ano; a H100 paga em 4-6 meses)
- Controle de dados sensíveis em jurisdição regulada (BACEN, LGPD, ANPD)
- Independência de fornecedor (não fica refém de mudança de preço ou de descontinuação de modelo)

## Decisão esperada (em direção geral)

A 35 mil/mês, fintech regulada de 800 pessoas, a decisão é genuinamente borderline. O juiz NÃO deveria decidir vitória decisiva — é exatamente o tipo de caso em que **empate técnico com recomendação prática** é a saída honesta.

A recomendação prática típica nesse cenário:
- Fase 1 (6 meses): manter API, instrumentar custo composto por feature, identificar onde o gasto se concentra.
- Fase 2 (6-12 meses): se 70%+ do gasto estiver em features de alta-volume com qualidade Haiku-suficiente, migrar essas features para deploy próprio Llama 3.3.
- Fase 3 (12-24 meses): manter API para features que exigem fronteira (Sonnet/Opus) e produção própria para volume comoditizado.

## Pontos cegos que o juiz deve sinalizar

- Custo do time de infra para operar deploy próprio (não é só GPU; é SRE, observabilidade, MLOps, on-call).
- Risco operacional do primeiro incidente em produção própria (a Anthropic absorve incidentes via SLA; deploy próprio absorve internamente).
- Diferencial competitivo gerado pelo controle de dados (não trabalha em todo setor, mas em fintech regulada pode justificar custo extra).

## Variação útil

Teste o mesmo debate trocando o tamanho da fintech:

```bash
python agent.py \
  --question "Em uma fintech regulada brasileira de 80 colaboradores [...] USD 4 mil/mês [...]" \
  --thesis-a "..." --thesis-b "..." --rounds 1
```

Em escala 10× menor, a decisão deveria pender claramente para API. O juiz que NÃO identifica essa sensibilidade ao tamanho está perdendo a parte mais importante do debate.
