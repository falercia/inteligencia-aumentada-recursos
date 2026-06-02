# Anti-padrões observados — P-MKT-01

## Geração de copy A/B testável

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo cria headline acima do limite
- Modelo usa promessa vedada por compliance
- Modelo gera quatro variantes praticamente iguais
- Modelo ignora tensão entre brand voice e canal
- Modelo aceita comparação direta com concorrente em setores com restrição legal de publicidade comparativa

---

## Métrica de qualidade

Diferença semântica medida entre variantes acima de limiar definido, aderência ao limite de caracteres em cem por cento, e ausência total de risco de compliance no golden set. Em setores regulados ou contextos sensíveis, exigência adicional de marcação de risco residual e recomendação de revisão jurídica em cem por cento dos casos.
