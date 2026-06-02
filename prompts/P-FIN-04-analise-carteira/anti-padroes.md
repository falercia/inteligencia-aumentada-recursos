# Anti-padrões observados — P-FIN-04

## Análise de carteira recomendada

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo recomenda diretamente ao leitor "compre este ativo"
- Modelo afirma rentabilidade futura como certa
- Modelo classifica perfil do investidor, função reservada a suitability
- Modelo infere probabilidade de cenário não declarada pelo relatório
- Modelo normaliza expectativa de retorno em média ponderada autoral

---

## Métrica de qualidade

Ausência absoluta de recomendação direta no golden set, e identificação correta de pelo menos noventa por cento das lacunas esperadas. Em relatórios com estruturados, ilíquidos ou alavancados, exigência adicional de marcação do risco material declarado em cem por cento dos casos.
