# PROMPTS — BIBLIOTECA DE PROMPTS TESTADOS

> Espelho rodável do Apêndice L do Livro 1. Cada prompt aqui está estruturado segundo o **F4 PROMPT-EXT** (Persona/Constituição/Contexto/Instrução/Pergunta viva) e vem acompanhado de golden set mínimo em `/evals`.

---

## CATEGORIAS

| Categoria | Status v0.1 | Caso de uso típico |
|-----------|--------------|---------------------|
| `analise-juridica/` | Stub | Due diligence, extração de cláusula, parecer estruturado |
| `due-diligence-mna/` | Stub | M&A (referência EC3 Vianna Castro) |
| `escrita-executiva/` | Stub | Memo para conselho, sumário executivo, deck de 10 slides |
| `classificacao-estruturada/` | Stub | Triagem por tier, roteamento por categoria, extração |
| `extracao-de-campos/` | Stub | OCR + extração, normalização de PII, scoring |
| `agentes-supervisionados/` | Stub | Co-piloto com confirmação humana |

---

## ESTRUTURA DE CADA PROMPT

```
nome-do-prompt/
├── prompt.txt              ← prompt aplicando F4 PROMPT-EXT
├── README.md               ← objetivo, Invariante-mãe, quando usar
├── exemplos.md             ← 3-5 exemplos de input/output esperado
└── eval-link.md            ← link para golden set em /evals
```

---

## REGRAS DE ESTRUTURA — F4 PROMPT-EXT

Todo prompt aqui segue 5 blocos posicionais:

1. **Persona e missão** (topo) — 1-3 linhas
2. **Constituição** (logo após persona) — regras invioláveis em bullets curtos
3. **Contexto** (meio) — documentos, exemplos, dados
4. **Instrução operacional + formato** (antes da pergunta) — reitera o crítico
5. **Pergunta viva** (última posição) — input sanitizado do usuário

---

## ROADMAP

| Marco | Conteúdo |
|-------|----------|
| v0.1 (atual) | Stubs com estrutura de pasta + esta documentação |
| v0.2 | 3 prompts canônicos por categoria, totalizando 18 prompts |
| v1.0 | Biblioteca completa espelhando L1-APX-L; 50+ prompts |
| v1.x | Atualização contínua com prompts da comunidade |

---

🔗 [Cap 09 Engenharia de Prompt](../../Livro-1-Os-Invariantes/02-capitulos/L1-C09-engenharia-prompt.md) · [F4 PROMPT-EXT](../../Livro-1-Os-Invariantes/03-frameworks/L1-F4-prompt-ext.md)
