# CONTRATO DO REPOSITÓRIO ACOMPANHANTE
## *Inteligência Aumentada — código vivo*

> Este repositório é o **companheiro opcional** dos dois livros da obra *Inteligência Aumentada*. Existe deliberadamente fora do corpo dos livros, conforme a Direção Editorial Rota A. O propósito é entregar implementação rodável a quem quiser pôr a mão na massa, sem poluir a obra principal com código que envelhece em meses.

---

## ROTA A — POR QUE O CÓDIGO MORA AQUI E NÃO LÁ

A obra impressa segue a regra do Invariante 3 (Camada Dupla): padrão durável no livro, número volátil em apêndice datado. Código vai para um terceiro lugar — este repositório — porque envelhece mais rápido que o número e demanda manutenção contínua. Quem opera só pelos livros sai com método e decisão; quem opera com este repositório acrescenta implementação.

**O que está aqui:** prompts testados, templates de eval, exemplos de agentes, servidores MCP minimalistas, notebooks de demonstração, datasets de prática.
**O que NÃO está aqui:** explicação conceitual (vai no livro), versões correntes de modelos e preços (vão no Apêndice Vivo do Livro 2).

---

## ESTRUTURA

```
_repositorio-acompanhante/
├── CONTRATO.md           ← este arquivo
├── README.md             ← navegação
├── prompts/              ← biblioteca de prompts testados (espelho L1-APX-L)
├── evals/                ← templates de golden set, scorecards, regressão
├── agents/               ← subagentes e workflows rodáveis
├── mcp/                  ← servidores MCP minimalistas
├── notebooks/            ← demonstrações conceituais executáveis
└── datasets/             ← datasets de prática para evals
```

---

## CONTRATO DE MANUTENÇÃO

| Item | Compromisso |
|------|-------------|
| **Periodicidade de atualização** | Revisão mensal; release maior trimestral |
| **Dono operacional** | A definir (pendente decisão do autor — ver `_PROJETO/ROADMAP-EXECUCAO.md`) |
| **Versionamento** | SemVer aplicado a cada pasta (prompts/v0.1, evals/v0.1, etc.) |
| **Política de breaking changes** | Anunciados em CHANGELOG.md com 30 dias de antecedência sempre que possível |
| **Compatibilidade com versões dos livros** | Cada release do repositório aponta para qual edição dos livros é compatível |
| **Issues e contribuições** | Aberto, com curadoria; PRs aceitos sob condição de aderência aos Invariantes |
| **Licença** | MIT para código; CC-BY-SA para textos não-código |

---

## STATUS INICIAL DAS PASTAS

| Pasta | Status v0.1 | Próximo marco |
|-------|--------------|----------------|
| `/prompts` | Stub com 5 categorias documentadas | Onda 4 — biblioteca completa espelhando L1-APX-L |
| `/evals` | Stub com template de golden set | Onda 4 — golden sets dos 4 capítulos definitivos |
| `/agents` | Stub com 1 exemplo de subagente | Onda 4 — agentes dos 7 estudos de caso |
| `/mcp` | Stub com 1 servidor MCP minimalista | Onda 4 — 5 MCPs canônicos por categoria |
| `/notebooks` | Stub com 1 notebook de demonstração | Onda 4 — 10 notebooks cobrindo Caps 02-08 |
| `/datasets` | Stub com 2 datasets de prática | Onda 4 — datasets dos 7 estudos de caso |

---

## REGRAS DE CONTRIBUIÇÃO

1. **Aderência aos Invariantes.** Todo código novo declara qual Invariante e qual framework ele instancia, na docstring inicial.
2. **Eval obrigatório.** Todo prompt ou agente vem com pelo menos golden set mínimo de 10 itens.
3. **Sem versões cravadas.** Nenhum exemplo cita modelo X.Y específico no código; usa variável de ambiente ou config.
4. **Sem PII.** Nenhum exemplo carrega PII de cliente real, mesmo anonimizado.
5. **Português executivo.** Documentação principal em pt-BR; docstrings podem ser bilíngues.

---

## CONEXÃO COM OS LIVROS

- **Livro 1** ([raiz](../Livro-1-Os-Invariantes/)) — método, conceito, framework
- **Livro 2** ([raiz](../Livro-2-Dominando-Claude/)) — ecossistema Claude, casos, Apêndice Vivo
- **Este repositório** — implementação rodável

---

## ATRIBUIÇÃO E COMUNIDADE

**Autor:** Fabio Garcia
**Origem:** Inteligência Aumentada — Os Invariantes da IA · Volume Vivo — Dominando Claude

Comunidade de Operadores Inteligência Aumentada — em formação. Detalhes a publicar em release v1.0.

---

> *"Código no repositório. Método no livro. Número no apêndice datado. Quem mistura os três paga em manutenção."*
