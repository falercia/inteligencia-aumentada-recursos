# Anti-padrões observados — P-SUP-03

## Decisão sobre escalonamento

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo escala por tom emocional do cliente
- Modelo deixa de escalar por receio de incomodar área superior
- Modelo cria critério inexistente nas regras
- Modelo confunde risco comercial (churn, renovação) com critério técnico de escalonamento
- Modelo escala defensivamente em casos limítrofes em vez de propor ação intermediária

---

## Métrica de qualidade

Aderência a critério explícito em cem por cento das decisões no golden set, e concordância com coordenador em pelo menos noventa por cento. Em casos com risco de segurança, regulatório ou padrão sistêmico, exigência adicional de escalonamento correto para a área certa em cem por cento dos casos.
