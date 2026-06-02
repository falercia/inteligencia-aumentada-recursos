# Anti-padrões observados — P-LEG-03

## Red flags em contrato M&A

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo classifica como cláusula bloqueante o que é prática usual de mercado, gera alarme falso
- Modelo cita acórdão inexistente do STJ para reforçar argumento
- Modelo recomenda walk away em vez de listar pontos de negociação
- Modelo aceita earn-out sem rules contábeis como ponto de negociação quando deveria ser bloqueante
- Modelo trata MAC sem carve-outs como prática de mercado quando representa risco assimétrico

---

## Métrica de qualidade

Concordância com sócio de M&A em pelo menos oitenta por cento das classificações de nível, com tolerância de um nível de distância em casos limítrofes, e identificação de cem por cento das cláusulas bloqueantes claras do golden set. Em casos de operação cross-border ou em setor regulado, exigência adicional de sinalização explícita da dimensão regulatória ou de governing law em cem por cento dos casos.
