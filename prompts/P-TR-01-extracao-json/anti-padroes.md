# Anti-padrões observados — P-TR-01

## Extração estruturada com schema JSON

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo inventa CNPJ quando o documento não traz
- Modelo preenche string vazia em vez de nulo
- Modelo converte data sem instrução
- Modelo cria campo novo no JSON que não está no schema
- Modelo completa palavras parcialmente legíveis ou parcialmente impressas

---

## Métrica de qualidade

Fidelidade ao texto fonte em cem por cento, ausência total de invenção em auditoria, e marcação correta de ambiguidade em todos os casos do golden set. Em documentos com OCR fragmentado, edição visível ou inconsistência declarativa, exigência adicional de marcação em "_auditoria" em cem por cento dos casos.
