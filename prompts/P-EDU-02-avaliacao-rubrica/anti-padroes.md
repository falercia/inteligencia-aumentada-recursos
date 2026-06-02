# Anti-padrões observados — P-EDU-02

## Avaliação rubrica-baseada

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo emite juízo sobre o aluno em vez do texto
- Modelo cria critério fora da rubrica
- Modelo dá feedback irônico ou desanimador
- Modelo afirma plágio sem evidência confirmada
- Modelo penaliza variedade linguística não-padrão quando a rubrica não a inclui como critério

---

## Métrica de qualidade

Concordância com professora sênior em pelo menos oitenta e cinco por cento das pontuações no golden set, e aderência à rubrica em cem por cento dos critérios avaliados. Em casos com indicador de bem-estar do aluno ou suspeita de plágio, exigência adicional de marcação correta em pontos de revisão em cem por cento dos casos.
