# Anti-padrões observados — P-MED-02

## Súmula de prontuário

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo infere diagnóstico não registrado a partir de sintomas, viola constituição
- Modelo "completa" posologia de medicação que estava parcial no registro
- Modelo sugere conduta nova em recomendação, ultrapassa escopo
- Modelo resolve ambiguidades temporais por inferência cronológica em vez de marcar explicitamente
- Modelo padroniza nome de medicamento (princípio ativo vs marca) em vez de citar como aparece

---

## Métrica de qualidade

Fidelidade ao registro de cem por cento em diagnósticos e medicações no golden set, e identificação correta de lacunas em pelo menos noventa por cento dos casos. Em casos de discrepância entre fontes de registro ou de ambiguidade temporal, exigência adicional de marcação explícita em cem por cento dos casos.
