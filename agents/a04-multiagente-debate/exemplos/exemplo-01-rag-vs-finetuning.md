# Exemplo 1 — RAG vs Fine-tuning (caso canônico)

## Comando

```bash
python agent.py \
  --question "Devo adotar RAG ou fine-tuning como caminho principal para o meu assistente jurídico em um escritório de M&A com 50 advogados, base de conhecimento de 20 mil documentos atualizados quase diariamente, e exigência de citações verificáveis a fontes primárias?" \
  --thesis-a "RAG é o caminho dominante neste contexto." \
  --thesis-b "Fine-tuning é o caminho dominante neste contexto." \
  --rounds 1 \
  --verbose
```

## O que esperar

1. **Abertura do Proponente (RAG)** — argumenta que atualização contínua dos 20 mil documentos e citação verificável a fonte primária são satisfeitos nativamente por RAG, com custo composto sob controle quando há disciplina de chunking + reranking + caching.
2. **Abertura do Oponente (Fine-tuning)** — ataca o custo de retrieval por chamada em volume de 50 advogados, propõe fine-tuning sobre corpus interno consolidado com periodicidade de retreinamento alinhada ao ciclo de release jurídico.
3. **Parecer do Juiz** — avaliação contra os 5 critérios da rubrica (`eval_config.json`), com nota por critério e citação dos argumentos, decisão e recomendação prática.

## Decisão esperada (em direção geral, não exata)

Em contexto descrito (atualização quase diária + citação verificável + 20 mil docs), RAG tende a vencer com folga, mas o juiz deve identificar **pontos cegos** que o debate não cobriu:

- Híbrido RAG + fine-tuning leve de estilo (não foi abordado por ninguém).
- Custo de manutenção da pipeline de RAG (chunker, reranker, índice vetorial) vs. custo de retreinamento periódico.
- Risco de drift do modelo base entre fine-tunings vs. drift do índice RAG entre rebuilds.

A qualidade do exemplo está justamente nesta camada — o juiz que só decide quem venceu, sem mapear pontos cegos, está aquém do esperado pela rubrica.

## Variação útil

```bash
python agent.py --rounds 2 --verbose
```

Adiciona uma rodada de réplica/tréplica. O custo dobra; o ganho marginal aparece quando o juiz consegue ver refinamento honesto dos dois lados em vez de só abertura.

## Modo seco para estudar

```bash
python agent.py --dry-run
```

Em dry-run, cada agente devolve resposta simulada. O exercício é ler o `agent.py` e entender o fluxo de mensagens entre proponente, oponente e juiz sem gastar token.
