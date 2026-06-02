# Anti-padrões observados — P-SUP-01

## Classificação de ticket em severidade

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo eleva severidade por tom emocional sem indicador técnico
- Modelo promete prazo de resolução, ultrapassa escopo
- Modelo rotear para escalation por receio de cliente insatisfeito
- Modelo rebaixa S1 por ausência de detalhe técnico inicial em casos de segurança
- Modelo deixa de marcar escalonamento para áreas adjacentes (legal, CSM) em casos não puramente técnicos

---

## Métrica de qualidade

Concordância com supervisor de suporte em pelo menos oitenta e cinco por cento das classificações no golden set, e identificação correta de cem por cento dos S1. Em casos com obrigação regulatória, segurança preventiva ou sinal de churn, exigência adicional de marcação correta de escalonamento para área não técnica em cem por cento dos casos.
