# Anti-padrões observados — P-LEG-01

## Revisão de cláusula de não-concorrência CLT

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo inventa número de acórdão do TST quando pressionado por especificidade, regra constitucional impede
- Modelo paráfrasa a cláusula em vez de citar literalmente, perde-se rastreabilidade na revisão humana
- Modelo emite veredito de invalidade, ultrapassa o escopo solicitado de análise de risco

---

## Métrica de qualidade

Concordância com parecer de advogado sênior em pelo menos oitenta e cinco por cento do golden set quanto à classificação de risco, e cem por cento quanto à identificação de elementos ausentes.
