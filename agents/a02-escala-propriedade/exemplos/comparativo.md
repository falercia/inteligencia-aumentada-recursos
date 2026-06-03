# Exemplo Comparativo — Mesma tarefa nos 4 níveis

> **O ponto deste exemplo:** rodar a mesma tarefa nos quatro níveis em sequência e observar a diferença operacional na pele, em vez de ler a descrição no livro.

---

## Setup

```bash
# Resetar estado para começar limpo
python gates.py reset
python kill_switch.py revive
rm -rf outbox/ state/subscriptions.json
```

---

## Roteiro de execução

### Rodada 1 — Nível 1 (Assistente)

```bash
python nivel_1_assistente.py
```

**O que esperar:** o agente vai chamar `customer_lookup` e `draft_cancellation_email`, e devolver uma resposta com um plano explícito do que o operador humano precisa fazer manualmente (enviar e-mail, atualizar status). Nenhum arquivo em `./outbox/` ou `./state/` é criado. Custo: ~600-1000 tokens.

**Observação editorial:** este nível é frustrante para quem está acostumado a delegar; é exatamente esse o ponto. Ele te força a manter a competência operacional no time, em troca da garantia de que nenhuma ação irreversível foi tomada sem você.

---

### Rodada 2 — Nível 2 (Co-piloto)

```bash
python nivel_2_copiloto.py
```

**O que esperar:** o agente vai chamar `customer_lookup` direto, depois pedir aprovação no terminal antes de cada `draft_cancellation_email` (não — esse não pede, é só leitura/rascunho), `simulate_send_email` (pede) e `update_subscription` (pede). Recuse uma das ações com `n` e veja o agente recalibrar a resposta final reconhecendo a recusa.

**Observação editorial:** a fricção do gate é o custo da segurança. Em três aprovações é tolerável; em trezentas por dia é insustentável — e este é o sinal de que a operação precisa subir para o nível 3.

---

### Rodada 3 — Nível 3 (Supervisionado)

```bash
# Em um terminal:
tail -f ./traces/trace-*.jsonl 2>/dev/null

# Em outro terminal:
python nivel_3_supervisionado.py
```

**O que esperar:** o agente executa todas as ações em lote, sem pedir aprovação. O trace no primeiro terminal mostra cada chamada em tempo real. Para parar, vá ao primeiro terminal e rode `python kill_switch.py kill` em outra aba — se houver iteração subsequente, ela vai bloquear.

**Observação editorial:** este nível só é seguro quando a observabilidade está madura. Sem o `tail -f` rodando em janela visível, este nível é nível 4 mal disfarçado. Não pule etapas.

---

### Rodada 4 — Nível 4 (Autônomo Regulado)

```bash
# Tentativa direta — vai falhar
python nivel_4_autonomo_regulado.py
# → [NIVEL 4] gates de promoção NÃO aprovados — agente não vai iniciar.

# Caminho correto: cumprir as condições primeiro
for i in $(seq 1 14); do python gates.py simulate-day; done
python gates.py approve-owner
python gates.py record-rollback-test
python gates.py status         # confere se está tudo verde
python gates.py promote        # tenta promover

# Agora pode rodar
python nivel_4_autonomo_regulado.py
```

**O que esperar:** o agente executa em silêncio. Ao fim, o eval automatizado roda contra o resultado e relata `passed: true`. Se você editar a tarefa para algo ambíguo (ex.: `--task "Faça o que achar melhor com o cliente Acme Industrial"`), o eval costuma falhar e o agente sinaliza rebaixamento automático para nível 3.

**Observação editorial:** o nível 4 não é "mais autonomia que o nível 3". É a **mesma autonomia com instrumentação ao redor maior**. Quem promove sem cumprir os gates está pulando a parte que justifica o nível, e vai pagar quando algo der errado e a investigação descobrir que não havia eval, não havia rollback testado, não havia dono nominal.

---

## Tabela comparativa após as quatro rodadas

| Métrica | Nível 1 | Nível 2 | Nível 3 | Nível 4 |
|---|---|---|---|---|
| Tools com efeito chamadas | 0 | 2 (com gate) | 2 | 2 |
| Tempo total (humano) | curto | longo (input por ação) | curto | mínimo |
| Tempo total (modelo) | ~10s | ~15s | ~12s | ~12s |
| Arquivos criados em `./outbox/` | 0 | 1 | 1 | 1 |
| Tokens (aprox.) | 600-1000 | 1500-2500 | 1200-2000 | 1200-2000 |
| Pré-condições operacionais | nenhuma | terminal aberto | trace monitorado + kill switch | gates aprovados + eval rodando |

---

## A pergunta que o exemplo cobra do leitor

Depois de rodar os quatro, escolha **na sua organização atual** o nível máximo em que você sustenta operar com este tipo de tarefa hoje, **e justifique pelas pré-condições da última linha da tabela acima**, não pela vontade.

A resposta vai surpreender quem nunca passou por este exercício. A maioria das organizações que dizem operar "agentes autônomos" está operando, na prática, no nível 3 mal instrumentado — sem trace monitorado, sem kill switch testado, sem dono nominal. F3 é o instrumento que torna essa diferença visível.
