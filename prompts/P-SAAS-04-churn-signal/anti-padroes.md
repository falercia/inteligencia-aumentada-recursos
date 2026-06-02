# Anti-padrões observados — P-SAAS-04

## Análise de churn signal

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo confirma churn como certo
- Modelo recomenda desconto comercial sem evidência de objeção de preço
- Modelo propõe ação fora do alcance de CSM em cinco dias
- Modelo trata NPS de respondente único como sinal forte
- Modelo ignora evento externo (M&A, mudança de strategy do cliente) como driver de risco

---

## Métrica de qualidade

Concordância com CS Ops em pelo menos oitenta e cinco por cento das classificações de risco no golden set, e cem por cento de aderência ao prazo de cinco dias úteis nas ações propostas. Em sinais mistos ou eventos externos, exigência adicional de sinalização explícita da fonte do risco em cem por cento dos casos.
