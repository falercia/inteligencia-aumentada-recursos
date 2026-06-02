# Anti-padrões observados — P-SAAS-01

## Classificação de feature request por persona

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo promete entrega ao classificar, ultrapassa escopo
- Modelo funde pedidos distintos
- Modelo atribui severidade alta por linguagem emocional do cliente
- Modelo classifica pedido de regulação como funcionalidade discricionária
- Modelo ignora duplicidade aparente entre clientes do mesmo segmento

---

## Métrica de qualidade

Concordância com PM sênior em pelo menos oitenta por cento da classificação multidimensional no golden set. Em pedidos aglomerados ou de origem regulatória, exigência adicional de marcação correta da categoria em cem por cento dos casos.
