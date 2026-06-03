# Exemplo 3 — Promover agente do nível 3 (Supervisionado) para nível 4 (Autônomo regulado)

## Comando

```bash
python agent.py \
  --question "Meu agente de classificação de tickets de suporte está há 90 dias estável no nível 3 do F3 (Supervisionado), com taxa de acerto de 91% no golden set, sem incidentes SEV-1, com rollback testado em simulado mensal. Devo promover para nível 4 (Autônomo Regulado)?" \
  --thesis-a "Promover para nível 4 é o movimento certo agora (gates atendidos)." \
  --thesis-b "Manter em nível 3 mais um trimestre é o movimento certo (margem de segurança)." \
  --rounds 1 \
  --verbose
```

## Por que este exemplo importa

A maior parte das decisões de promoção de autonomia em IA acontece sem debate explícito — o time vai descobrindo, na prática, em qual nível está confortável. O debate forçado revela considerações que **ficariam silenciosas** numa decisão por consenso passivo:

- **Proponente da promoção** argumenta que 90 dias + 91% + zero SEV-1 + rollback testado são os critérios canônicos do F3 e ficam satisfeitos. Não promover é sub-utilização.
- **Oponente da promoção** argumenta que 91% no golden set não vira 91% em produção (distribution shift), que o simulado mensal de rollback não substitui o exercício real, e que o custo de manter no nível 3 é baixo enquanto o custo de promover prematuramente é alto (incidente caro + reputação).

## Decisão esperada (em direção geral)

Este caso é, propositalmente, **muito próximo do limiar**. O juiz tende a decidir empate técnico com nota maior ao oponente em "honestidade sobre limites" e ao proponente em "conexão com consequência prática".

A recomendação prática típica:
- **Promover para nível 4, MAS com instrumentação adicional nos primeiros 30 dias**: amostragem humana de 5% do tráfego em vez dos 1% típicos, alerta automático no primeiro sinal de drift, kill switch redundante (não apenas o canônico).
- Após 30 dias estáveis no nível 4 com a instrumentação extra, relaxar para o padrão do F3 nível 4.

## Pontos cegos que o juiz deve identificar

- Nenhum dos dois agentes mencionou **eval adversarial** específico para o tipo de ticket em produção (jailbreak via input do cliente, prompt injection via assunto, ataque de classificação adversarial). Promover sem essa cobertura é risco oculto.
- Nenhum dos dois discutiu **observabilidade humana ativa vs. amostragem**. No nível 4, a confiança vem da observabilidade automatizada; mas no primeiro mês de promoção, observação humana ativa de 30 min/dia paga muito.
- Nenhum dos dois citou a **Camada Dupla do próprio nível F3**: o critério (90d + 91% + rollback) é padrão durável; os números específicos podem precisar ajuste em domínios sensíveis.

## Para que serve este debate

A pergunta "devo promover meu agente?" raramente recebe atenção arquitetural à altura da decisão. O debate A04 força essa atenção, com proponente e oponente operando no mesmo nível de rigor, e juiz arbitrando contra critério explícito. É o exato instrumento que protege contra "promoção por inércia" (subir nível porque o time achou que ia subir) e contra "manutenção por medo" (não subir nunca porque ninguém quer assumir a decisão).
