# Anti-padrões observados — P-EDU-01

## Geração de plano de aula

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo soma tempos das etapas que excedem duração total
- Modelo cria competência não declarada
- Modelo promete que aluno aprenderá X ao final, ultrapassa escopo
- Modelo prescreve conduta clínica para alunos com necessidades específicas
- Modelo opina sobre controvérsias políticas ou religiosas dentro do plano

---

## Métrica de qualidade

Coerência entre soma dos tempos e duração total em cem por cento dos casos, e concordância com coordenador em pelo menos noventa por cento da adequação pedagógica. Em casos com heterogeneidade de turma, necessidades específicas ou conteúdo sensível, exigência adicional de marcação em "Pontos que necessitam adaptação" em cem por cento dos casos.
