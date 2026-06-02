# Anti-padrões observados — P-SAAS-03

## Geração de release notes

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo inventa funcionalidade não listada
- Modelo usa jargão técnico como "refatoramos o módulo X"
- Modelo promove entrega futura, viola constituição
- Modelo omite breaking change para evitar comunicação difícil
- Modelo expõe detalhes de vulnerabilidade fechada em release nota pública

---

## Métrica de qualidade

Aderência à lista de entrada de cem por cento no golden set, e identificação correta de breaking changes em cem por cento dos casos. Em mudanças com impacto contratual ou regulatório, exigência adicional de sinalização para alinhamento jurídico em cem por cento dos casos.
