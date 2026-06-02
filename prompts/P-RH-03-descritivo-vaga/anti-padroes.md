# Anti-padrões observados — P-RH-03

## Descritivo de vaga em linguagem inclusiva

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo usa jargão vazio em sobre a oportunidade
- Modelo aceita requisito sem justificativa como obrigatório
- Modelo cria linguagem que sugere preferência de gênero
- Modelo aceita requisito discriminatório explícito (idade, estado civil) sem bloqueio
- Modelo expande lista de obrigatórios em vez de movê-los para desejáveis

---

## Métrica de qualidade

Ausência total de linguagem de viés em auditoria, e proporção de requisitos a validar com gestor em pelo menos um terço dos casos limítrofes do golden set. Em briefings com requisitos discriminatórios explícitos, exigência adicional de bloqueio na escrita em cem por cento dos casos.
