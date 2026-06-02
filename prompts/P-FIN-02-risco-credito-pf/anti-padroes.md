# Anti-padrões observados — P-FIN-02

## Classificação de risco de crédito PF

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo decide aprovação por conta própria, ultrapassa escopo
- Modelo justifica com "perfil parece bom" sem citar variável observável
- Modelo considera tempo de relacionamento como suficiente para ignorar comprometimento

---

## Métrica de qualidade

Concordância com analista sênior em pelo menos oitenta e cinco por cento das classificações, com tolerância de uma faixa em casos limítrofes.
