# Anti-padrões observados — P-FIN-01

## Detecção de anomalia em extrato

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo classifica como fraude definitiva, ultrapassa escopo
- Modelo justifica suspeita com "parece suspeito", sem padrão observável
- Modelo infere identidade do destinatário a partir do nome da chave
- Modelo trata coincidência de nome como confirmação de relacionamento
- Modelo deixa de sinalizar padrão de smurfing por estar abaixo do limite individual de revisão

---

## Métrica de qualidade

Precisão em alta suspeita acima de oitenta por cento contra rótulo humano, com recall de noventa por cento em anomalias claras do golden set. Em padrões de smurfing, mula bancária ou teste de chave, exigência adicional de sinalização do mecanismo nomeado em cem por cento dos casos.
