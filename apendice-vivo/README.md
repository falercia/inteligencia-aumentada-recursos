# Apêndice Vivo · Ponteiro

> Atualizado em: 2026-06-16
> Próxima revisão: sem cadência fixa — acompanha o ritmo do repositório deep-claude
> Fonte: [github.com/falercia/deep-claude → apendice-vivo](https://github.com/falercia/deep-claude/tree/main/apendice-vivo)

---

## O que esta pasta é — e o que ela não é

Esta pasta não contém números. Não há tabela de modelos, não há preço de token, não há ranking de benchmark aqui.

Esta pasta é um ponteiro deliberado. A camada de números cross-vendor da série **Inteligência Aumentada** — modelos atuais, preços normalizados, benchmarks publicados, janelas de contexto, SLAs — é mantida como **fonte única** no repositório irmão:

> **github.com/falercia/deep-claude → `apendice-vivo/`**

A decisão de manter os números em um único lugar, e não replicá-los aqui, é a aplicação direta do que o livro prega no Invariante Três, a Camada Dupla. Dois lugares com o mesmo dado não é redundância útil; é garantia de inconsistência. Quando os números mudarem — e vão mudar, provavelmente antes do fim do mês — um só arquivo precisa ser atualizado, e a informação permanece coerente para o leitor de qualquer dos dois repositórios.

---

## Como navegar o Apêndice Vivo do deep-claude

O Apêndice Vivo do repositório deep-claude contém:

| Arquivo | Conteúdo |
|---|---|
| `MODELOS.md` | Famílias de modelos com estado atual: Claude, GPT, Gemini, open-source |
| `PRECOS.md` | Preços normalizados por milhão de tokens, USD e BRL |
| `BENCHMARKS.md` | SWE-bench, MMLU-Pro, GPQA, HumanEval+ e similares |
| `JANELAS-SLA.md` | Janelas de contexto, cotas por plano, SLAs declarados |
| `FONTES.md` | Fontes primárias linkadas para rastreabilidade |
| `CHANGELOG-APENDICE.md` | Histórico mensal de atualizações e errata |

Cadência de atualização: mensal, entre os dias 1 e 7 de cada mês. Mudanças fora da janela (lançamento de modelo, mudança de preço relevante) geram entrada no changelog sem esperar o ciclo.

---

## O método vendor-neutral de ler números de IA

Números de IA sem método de leitura são mais perigosos do que a ausência de números. O profissional que memoriza ranking de modelo em junho de 2026 vai tomar decisão ruim em setembro de 2026 com a mesma confiança de quem tem dado atual. O que segue não é lista para memorizar — é o que olhar e por que não confiar no que acabou de ler sem verificar a data.

### O que olhar numa comparação de modelos

**Data do snapshot.** A primeira pergunta ao abrir qualquer comparação é: quando isso foi medido? Ecossistema de modelo novo a cada três meses significa que comparação de doze meses atrás é história, não referência. Comparação sem data declarada é comparação que não merece confiança.

**Contexto do benchmark.** MMLU-Pro e GPQA medem capacidades em domínio fechado com resposta objetiva. SWE-bench mede capacidade de resolver issue real de software. Nenhum mede o que importa para o seu caso de uso específico. O ranking que posiciona modelo A acima de modelo B em MMLU-Pro diz exatamente nada sobre qual dos dois vai escrever melhor relatório financeiro em português. Teste no seu caso de uso real antes de decidir.

**Quem publicou.** Benchmark publicado pelo próprio provedor do modelo é marketing até prova em contrário. Isso não significa que é mentira — significa que a metodologia merece leitura crítica antes de citar como fonte. Benchmarks independentes (Hugging Face Open LLM Leaderboard, HELM, LMSYS Chatbot Arena) partem de metodologia mais resistente a cherry-picking.

**Configuração de teste.** Temperatura, janela usada, prompt, número de tentativas, hardware — todos afetam resultado. Dois grupos que testam o mesmo modelo com configurações diferentes chegam a números diferentes. O número sem a metodologia é dado incompleto.

### Como normalizar preço de token entre provedores

Preço de token sem normalização é armadilha. Os provedores usam unidades diferentes, aplicam descontos diferentes para diferentes volumes, e podem cobrar de formas assimétricas entre entrada e saída.

O processo mínimo de normalização tem quatro passos:

1. **Converter tudo para USD por milhão de tokens de saída.** Token de saída custa mais que token de entrada em praticamente todos os provedores. Se a sua aplicação gera respostas longas, o custo dominante é output. Comparar só input price é comparar metade do custo.

2. **Estimar a proporção entrada/saída real do seu tráfego.** Prompt de system com 2.000 tokens mais pergunta de 50 tokens mais resposta de 800 tokens tem uma proporção que você pode calcular agora. Use essa proporção para calcular custo real por chamada, não custo por token isolado.

3. **Verificar se há desconto por volume ou batch.** Anthropic, OpenAI e Google oferecem desconto em Batch API ou equivalente. Para uso assíncrono (relatórios, enriquecimento de dados), o desconto pode ser de 50% sobre o preço padrão.

4. **Converter para BRL com a cotação do dia.** Preço em USD com dólar a 5,50 é diferente de preço em USD com dólar a 6,20. Orçamento de custo em produto brasileiro que ignora câmbio vai errar a previsão consistentemente.

### Por que não memorizar ranking

Ranking de modelo muda porque modelos novos são lançados, porque versões existentes são atualizadas silenciosamente, porque benchmarks são refinados, e porque a comunidade descobre novos pontos cegos dos benchmarks existentes. O ranking de abril de 2026 pode estar invertido em outubro de 2026, com o mesmo grau de confiança que foi publicado.

O que sobrevive ao ciclo não é o ranking — é o método de avaliar: qual é a data, qual é o benchmark, quem publicou, qual é a metodologia, qual é a configuração. Isso se aplica a qualquer ranking publicado em qualquer momento.

---

## Capítulos relacionados do livro

- **Apêndice J — Trilha do Número** — referencia o Apêndice Vivo como fonte viva dos dados que mudam
- **Invariante Três — A Camada Dupla** — a tese que justifica o ponteiro em vez da duplicação
- **Invariante Cinco — Honestidade Temporal** — a postura que exige data em cada dado perecível
- **Capítulo 15 — Modelos** — framework de decisão de modelo que este apêndice alimenta com números

---

> *"O número que muda não merece ser memorizado. Merece ser consultado com data e fonte antes de qualquer decisão."*
>
> *— Inteligência Aumentada · Os Invariantes da IA*
