# `/notebooks` — Notebooks Fundacionais Executáveis

> **Quatro notebooks Python rodáveis que tornam tangível, na tela, o que o livro descreve em texto.** Tokenização, janela de contexto, embeddings e prompt caching — os quatro conceitos que mais aparecem em decisão técnica e em conta de fim de mês, e os que mais sofrem com explicação só verbal.

---

## Para quem é esta pasta

| Se você é... | Vai sair daqui com... |
|---|---|
| **Profissional de tecnologia** que opera IA mas nunca viu por dentro | Modelo mental concreto do que acontece quando você manda um texto para um LLM. Você sai sabendo por que "Internacionalização" custa mais que "Internationalization", por que o início e o fim do prompt importam mais que o meio, e por que prompt caching é a maior alavanca de custo composto. |
| **CTO ou líder técnico** validando proposta de orçamento de IA | Cálculo em código do custo composto real, com os quatro multiplicadores aparecendo na conta. A planilha do fornecedor mostra preço por token; este notebook mostra a fatura. |
| **AI Engineer** começando a construir | Esqueleto de código para tokenização real (tiktoken), reprodução do experimento Lost in the Middle, geração de embeddings e cálculo de similaridade, instrumentação de prompt caching. |
| **Professor** preparando aula | Material rodável em laboratório, com narrativa didática célula a célula, sem dependência pesada (instala em três minutos). |

---

## Que problema esta pasta resolve

Os capítulos 3, 4, 5 e 18 do livro descrevem com rigor conceitos que **só ficam realmente fixados quando o leitor vê acontecendo na própria máquina**. "Token é unidade subpalavra" é uma frase; ver `"Internacionalização"` virar quatro tokens e `"cat"` virar um é compreensão. "O meio do contexto morre" é um princípio; ver a curva de recall caindo conforme a informação se afasta das extremidades é evidência. "Prompt caching reduz custo" é promessa; ver a fatura cair 60% em um exemplo controlado é decisão de adoção.

**Cada notebook desta pasta resolve esse gap entre saber e ver.** Roda em ambiente padrão Python, em três minutos de setup, sem GPU, sem download massivo, sem mistério.

---

## O que vive aqui

| Notebook | Capítulo-âncora | O que demonstra na prática | Tempo de execução |
|---|---|---|---|
| [`n01-tokenizacao.ipynb`](./n01-tokenizacao.ipynb) | **C3 — Tokens** · Inv. 5 Custo Composto | Como BPE quebra texto em tokens; por que português custa 30-50% mais que inglês; como contar tokens antes de enviar | ~30s |
| [`n02-janela-contexto.ipynb`](./n02-janela-contexto.ipynb) | **C4 — Janela de Contexto** · Inv. 2 Extremidades | Reprodução do experimento Lost in the Middle: agulha enterrada no meio do prompt some; nas extremidades é encontrada | ~2-5min (chama API) |
| [`n03-embeddings.ipynb`](./n03-embeddings.ipynb) | **C5 — Embeddings** · Inv. 3 Camada Dupla | Geração de embeddings, cálculo de similaridade coseno, visualização 2D em scatter plot, busca semântica básica | ~1-3min (chama API) |
| [`n04-prompt-caching.ipynb`](./n04-prompt-caching.ipynb) | **C18 — Economia de Tokens** · Inv. 5 Custo Composto | Mesma consulta com e sem caching; demonstra economia composta de tokens em conversa multi-turno | ~1-2min (chama API) |

---

## Como rodar

### Setup único (uma vez)

```bash
pip install -r requirements.txt
```

### Rodar localmente

```bash
jupyter notebook
# ou
jupyter lab
```

Abre o navegador. Clique no notebook que quer executar. Execute célula a célula com **Shift+Enter**.

### Para os notebooks que chamam API (N02, N03, N04)

```bash
export ANTHROPIC_API_KEY="sua-chave"
```

Sem a chave, esses notebooks têm uma célula de **modo demo** que carrega resultados pré-computados em arquivo local, para você ver a conclusão sem gastar token. Não substitui a execução real, mas funciona para sala de aula offline.

### Notebook 1 (tokenização) roda sem internet

N01 usa `tiktoken` localmente, sem chamada externa. Custo zero. Bom para começar.

---

## Sequência recomendada de leitura

1. **N01 (tokenização)** antes de tudo. É a fundação que sustenta a leitura dos outros três.
2. **N02 (janela de contexto)** depois. O experimento Lost in the Middle é a evidência que justifica a engenharia de prompt do C9 e a engenharia de contexto do C11.
3. **N03 (embeddings)** em seguida. A intuição geométrica é pré-requisito para RAG (C6) e para entender por que busca semântica funciona.
4. **N04 (prompt caching)** por último. Aplicação direta do custo composto (C18); só faz sentido depois que você sente, em N01, quanto custa cada token.

---

## Conexão com o livro

- 🔗 [**Capítulo 3 — Tokens**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C03-tokens.md)
- 🔗 [**Capítulo 4 — Janela de Contexto**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C04-janela-de-contexto.md)
- 🔗 [**Capítulo 5 — Embeddings**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C05-embeddings.md)
- 🔗 [**Capítulo 18 — Economia de Tokens**](../../Livro-1-Os-Invariantes/02-capitulos/L1-C18-economia-tokens.md)
- 🔗 [**Framework F7 — Custo Composto em Três Tempos**](../../Livro-1-Os-Invariantes/03-frameworks/L1-F7-composto-3t.md)

---

> *"Quem nunca viu um token na própria máquina opera no escuro sobre custo composto. Quatro notebooks, três minutos de setup, fim do escuro."*
