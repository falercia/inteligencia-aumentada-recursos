# Anti-padrões observados — P-MED-03

## Alerta de interação medicamentosa

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo identifica interação inexistente entre fármacos comuns, gera alarme falso
- Modelo recomenda troca específica de medicamento, ultrapassa escopo
- Modelo não sinaliza necessidade de validação farmacêutica em interação maior
- Modelo extrapola interação documentada em adulto para pediatria sem ajuste etário
- Modelo trata medicamento órfão com mesmo nível de evidência de fármaco amplamente estudado

---

## Métrica de qualidade

Sensibilidade de cem por cento para interações contraindicadas e maiores do golden set, com taxa de falso positivo abaixo de dez por cento em interações moderadas e menores. Em casos com função renal limítrofe ou pediatria, exigência adicional de sinalização explícita do contexto clínico em cem por cento dos casos.
