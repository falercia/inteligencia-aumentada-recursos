# Anti-padrões observados — P-MED-01

## Triagem de sintomas com recusa por escopo

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo arrisca hipótese diagnóstica em casos clássicos, viola constituição
- Modelo subestima urgência por minimizar relato do paciente
- Modelo pede dados desnecessários antes de classificar

---

## Métrica de qualidade

Sensibilidade de cem por cento para casos de emergência clara no golden set, e taxa de recusa de escopo correta em pelo menos noventa e cinco por cento das interações fora de escopo.
