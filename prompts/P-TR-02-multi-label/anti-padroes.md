# Anti-padrões observados — P-TR-02

## Classificação multi-label

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo inventa rótulo fora da taxonomia
- Modelo força rótulo único quando há múltiplos válidos
- Modelo atribui confiança alta sem evidência citada
- Modelo não usa "rotulos_considerados_e_descartados" como artefato de auditoria
- Modelo usa "outros" como rótulo padrão sem testar especificidade

---

## Métrica de qualidade

Aderência à taxonomia em cem por cento, F1 multi-label acima de limiar declarado contra rotulagem humana, e fallback correto em ambíguos do golden set. Em conteúdos com termos ambíguos ou intenção divergente, exigência adicional de marcação em descartados em cem por cento dos casos.
