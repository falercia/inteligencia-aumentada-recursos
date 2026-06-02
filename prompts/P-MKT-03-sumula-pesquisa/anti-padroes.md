# Anti-padrões observados — P-MKT-03

## Súmula de pesquisa de mercado

Comportamentos do modelo que comprometem a qualidade da saída.
Cada anti-padrão foi observado em uso real ou em teste contra o
golden set, e deve ser mitigado pela constituição, pelo prefill,
pelo self-critique, ou pela combinação dos três.

---

- Modelo extrapola resultados para escopo nacional sem base
- Modelo emite recomendação estratégica
- Modelo invente número não declarado
- Modelo reporta cross-tab com n pequeno como percentual estatístico
- Modelo omite vínculo de interesse do patrocinador da pesquisa

---

## Métrica de qualidade

Fidelidade numérica de cem por cento no golden set, e identificação de pelo menos uma ressalva metodológica em todos os casos com metodologia frágil. Em relatórios com patrocínio, mudança metodológica ou previsão de longo prazo, exigência adicional de ressalva explícita em cem por cento dos casos.
