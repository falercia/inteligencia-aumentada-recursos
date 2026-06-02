# Anti-padrões observados — P-FIN-03

## Súmula de relatório trimestral ITR

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo emite recomendação de compra implícita ao usar adjetivos como "excelente trimestre"
- Modelo arredonda números de forma a distorcer comparação
- Modelo infere guidance não declarado a partir do tom da carta
- Modelo normaliza câmbio ou base contábil sem o release fornecer a normalização
- Modelo extrapola comentário em call para implicação de mercado sem dado no release principal

---

## Métrica de qualidade

Fidelidade numérica de cem por cento ao release no golden set, e cobertura de todos os sete blocos quando informação está disponível, com ausência explícita sinalizada nos demais casos. Em releases com one-off, mudança contábil ou segmentação nova, exigência adicional de marcação da quebra de comparabilidade em cem por cento dos casos.
