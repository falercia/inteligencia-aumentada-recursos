# Exemplo 01 — Cálculo composto com decisão binária

> **O que este exemplo demonstra:** agente usa a tool `calculator` para executar cálculo exato em vez de confiar no raciocínio aritmético do LLM, depois responde decisão binária com base no resultado. Padrão clássico de ReAct: pensa, calcula, observa, responde.

---

## Como rodar

```bash
# Modo seco (não consome token)
python agent.py --dry-run --verbose \
  --task "Calcule 18% de R$ 12.450 e me diga se ultrapassa R$ 2.000"

# Modo real
export ANTHROPIC_API_KEY="sua-chave"
python agent.py --verbose \
  --task "Calcule 18% de R$ 12.450 e me diga se ultrapassa R$ 2.000"
```

---

## Saída esperada (modo real, valores aproximados)

```
[A01] tracing em ./traces/trace-20260801-103245-12345.jsonl
[A01] tarefa: Calcule 18% de R$ 12.450 e me diga se ultrapassa R$ 2.000

--- TOOL CALLS ---
1. calculator({'expression': '12450 * 0.18'})
   → 2241

--- RESPOSTA FINAL ---
Sim, ultrapassa. 18% de R$ 12.450 é R$ 2.241,00 — R$ 241,00 acima do limite
de R$ 2.000.

--- TELEMETRIA --- iterações=2 · tools_chamadas=1 · tokens_in=823 · tokens_out=187
trace completo em: ./traces/trace-20260801-103245-12345.jsonl
```

---

## O que observar

1. **Iterações = 2**: a primeira iteração o modelo pediu a tool; a segunda ele recebeu o resultado e respondeu. Esse é o loop ReAct mínimo.
2. **O modelo não fez a conta de cabeça**, mesmo sendo trivial. O `system_prompt.md` instrui explicitamente: *"em tarefas que misturam cálculo e prosa, faça o cálculo na tool"*. Esta é a primeira lição operacional do C12: a tool não é só para o que o modelo não sabe — é para o que precisa ser **auditável**.
3. **Resposta direta primeiro, justificativa depois**. O `system_prompt.md` também instrui isso. Compare com o que um modelo "padrão" responderia sem essa diretriz: provavelmente recapitularia a pergunta antes de responder.
4. **A telemetria mostra custo composto**. ~823 tokens de input para ~187 de output em uma tarefa trivial. Em escala, isso vira a aritmética que C18 (Economia de Tokens) cobra.

---

## Variações para experimentar

Rode as variações abaixo e compare a quantidade de iterações e o custo:

```bash
# Cálculo encadeado (vai exigir duas chamadas à calculadora)
python agent.py --verbose --task \
  "Quanto é 18% de R$ 12.450? E quanto sobra se descontar R$ 750 de impostos?"

# Cálculo + decisão composta
python agent.py --verbose --task \
  "Tenho R$ 50.000 para investir. Se o CDB rende 12% ao ano e a poupança 6%, quanto eu perderia em 3 anos optando pela poupança?"

# Cálculo com gate humano
python agent.py --verbose --gate --task \
  "Calcule 23 * 47 * 19 e me diga se é maior que 20.000"
```

A variação com `--gate` pede confirmação antes da chamada da calculadora. Em uma tool inofensiva como esta, a fricção parece exagero; em uma tool que envia e-mail ou move dinheiro, o gate é exatamente o que protege a operação. Esse é o ponto educacional de C12.4 e do Framework F3.
