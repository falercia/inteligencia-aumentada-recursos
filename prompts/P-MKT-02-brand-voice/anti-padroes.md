# Anti-padrões observados — P-MKT-02

## Análise de brand voice

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo reescreve a peça sem ser solicitado
- Modelo inventa diretriz de brand voice
- Modelo emite juízo estético sem critério
- Modelo classifica como desvio inconsistências por falta de critério na brand voice declarada
- Modelo trata jargão técnico necessário ou inside jokes como desvio

---

## Métrica de qualidade

Concordância com diretor de brand em pelo menos oitenta e cinco por cento das classificações de nível de desvio. Em casos de tensão entre brand voice e contexto (sensível, técnico, sazonal, internacional), exigência adicional de marcação como lacuna em vez de desvio em cem por cento dos casos.
