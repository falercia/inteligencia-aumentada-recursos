# Anti-padrões observados — P-LEG-04

## Parecer sobre compliance LGPD em processamento de dados

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo afirma adequação completa quando faltam informações, em vez de declarar indeterminado
- Modelo cita inciso inexistente do artigo 7 da LGPD
- Modelo confunde controlador e operador na atribuição de responsabilidades
- Modelo aceita "anonimização declarada" como suficiente sem exigir comprovação metodológica
- Modelo trata "legítimo interesse" como base legal universal sem exigir teste de balanceamento

---

## Métrica de qualidade

Identificação correta da base legal aplicável em cem por cento dos casos do golden set, e concordância com DPO sênior em pelo menos oitenta e cinco por cento das classificações por dimensão. Em casos envolvendo dados sensíveis, transferência internacional ou decisão automatizada, exigência adicional de nomear o artigo específico da LGPD aplicável (art. 11, art. 33, art. 20) em cem por cento dos casos.
