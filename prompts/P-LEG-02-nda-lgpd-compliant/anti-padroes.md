# Anti-padrões observados — P-LEG-02

## Análise de NDA brasileiro LGPD-compliant

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo confunde NDA brasileiro com modelos NDA americanos e cita exigências que não se aplicam no Brasil
- Modelo emite parecer sobre direito estrangeiro quando o NDA cita Nova York como foro
- Modelo presume existência de cláusulas que não estão no texto
- Modelo aceita "execução contratual" como base legal para dados sensíveis sem sinalizar erro
- Modelo trata anonimização declarada como suficiente sem exigir comprovação metodológica

---

## Métrica de qualidade

Identificação correta de no mínimo nove das dez cláusulas-chave em noventa por cento dos casos do golden set, e marcação correta de ponto de atenção LGPD em cem por cento dos casos em que dados pessoais são mencionados. Nos casos sensíveis ou de transferência internacional, exigência adicional de nomear a base legal específica do art. 7º ou art. 11 da LGPD em cem por cento dos casos.
