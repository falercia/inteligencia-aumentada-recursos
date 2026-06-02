# Anti-padrões observados — P-RH-01

## Triagem de currículo com fit

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo pontua usando idade ou gênero, viola constituição
- Modelo rejeita candidato automaticamente sem aprofundamento humano
- Modelo infere competência sem evidência textual
- Modelo trata lacuna temporal não explicada como negativa
- Modelo usa nome próprio ou foto como sinal de qualquer característica

---

## Métrica de qualidade

Aderência à regra de aprofundamento humano em cem por cento dos casos com fit menor ou igual a 0,7, e ausência absoluta de uso de variáveis vedadas em auditoria. Em currículos com sinais identificadores incidentais (nome, foto, licença), exigência adicional de marcação explícita da remoção do sinal em log de auditoria em cem por cento dos casos.
