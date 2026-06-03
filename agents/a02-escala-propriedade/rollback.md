# Procedimento de Rollback — A02

> Aplicável a partir do **Nível 2 (Co-piloto)**. No Nível 1 (Assistente), o agente não executa ações com escrita, então rollback é não aplicável. Procedimento testado mensalmente em produção; aqui descrito para que o leitor adapte ao próprio contexto.

---

## O que precisa ser revertido

Esta biblioteca de agentes opera com duas categorias de efeito:

1. **`simulate_send_email`** → grava arquivo `.eml` em `./outbox/`. Reversão: e-mail de retratação enviado ao mesmo destinatário, com texto institucional declarando o engano e o procedimento corretivo. Em produção, **não basta apagar o arquivo `.eml` local** — se a tool foi conectada a um servidor SMTP real, o envio já saiu.
2. **`update_subscription`** → grava em `./state/subscriptions.json` e produz um backup do estado anterior em `./state/backup-*.json`. Reversão: restaurar o backup mais recente.

---

## Procedimento de rollback de `update_subscription`

```bash
# 1. Localizar o backup mais recente do cliente afetado
ls -lt state/backup-Acme_Industrial-*.json | head -1

# 2. Ler o estado anterior
cat state/backup-Acme_Industrial-20260801-103245.json
# { "name": "Acme Industrial", "previous_status": "ativa" }

# 3. Restaurar via update_subscription com o estado anterior
python -c "from tools_simuladas import execute_update_subscription; \
  print(execute_update_subscription({'customer_name': 'Acme Industrial', \
  'new_status': 'ativa'}))"

# 4. Validar
cat state/subscriptions.json
```

---

## Procedimento de rollback de `simulate_send_email` em produção real

Em ambiente real (com SMTP plugado), o rollback não é "apagar o e-mail enviado" — o e-mail já foi entregue. O rollback é:

1. **Identificar o destinatário e timestamp** do e-mail equivocado pelo trace JSONL.
2. **Enviar e-mail de retratação** dentro de 24h, com texto institucional pré-aprovado.
3. **Registrar incidente** no canal de operações (mesmo que SEV-3, para histórico).
4. **Avaliar se a tool causou rebaixamento automático** do agente (ver `gates.py record-incident`).

---

## Teste mensal documentado

O teste de rollback é exercício deliberado, não confiança em procedimento:

```bash
# 1. Criar estado simulado
python -c "from tools_simuladas import execute_update_subscription; \
  print(execute_update_subscription({'customer_name': 'Acme Industrial', \
  'new_status': 'cancelada-fim-ciclo'}))"

# 2. Executar rollback como acima

# 3. Validar que o estado voltou ao anterior

# 4. Registrar o teste nos gates de promoção
python gates.py record-rollback-test
```

Quem não testa mensalmente perde, na hora do incidente, exatamente o que o teste protegia. A regra de F3 é literal: *rollback documentado e não exercitado é teatro*.

---

## Dono nominal do rollback

Em ambiente educacional: o leitor que está executando.

Em produção real, o dono nominal precisa ter:

- Nome e cargo registrados em `gates.py` (campo `owner_approved`)
- Acesso de escrita à fonte de verdade (no nosso caso, `./state/`)
- Treinamento documentado no procedimento de rollback
- Backup pessoal de plantão para janelas de ausência
