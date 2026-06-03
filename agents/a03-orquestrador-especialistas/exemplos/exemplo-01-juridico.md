# Exemplo 1 — Consulta jurídica trabalhista (caso canônico)

## Comando

```bash
python agent.py --task "Sou empregado de uma empresa de varejo e meu contrato tem cláusula de não-concorrência por 36 meses no Brasil inteiro, sem nenhuma contraprestação financeira. Isso é válido?"
```

## O que o orquestrador deve fazer

1. **Classificar**: a consulta é claramente do domínio `juridico_trabalhista` (cláusula CLT de não-concorrência).
2. **Despachar**: chamar `especialista_juridico_trabalhista` com a consulta integral.
3. **Receber**: o especialista devolve triagem dos cinco elementos TST (temporal=36m EXCESSIVO, geográfico=Brasil inteiro EXCESSIVO, contraprestação=AUSENTE, etc.), classe de risco provavelmente CRÍTICO, recomendação de revisão por advogado responsável.
4. **Consolidar**: parecer final estruturado conforme o formato declarado no system prompt.

## Saída esperada (esqueleto)

```
DOMÍNIO IDENTIFICADO: jurídico-trabalhista

CLASSIFICAÇÃO DO ESPECIALISTA:
Cláusula com múltiplos elementos potencialmente abusivos:
- Temporal: 36 meses excede o limite jurisprudencial usual (~24 meses) → CRÍTICO
- Geográfico: Brasil inteiro extrapola "mercado relevante" → CRÍTICO
- Contraprestação financeira: AUSENTE → CRÍTICO
Classe de risco geral: CRÍTICO.

RECOMENDAÇÃO PARA O CLIENTE:
A cláusula apresenta múltiplos elementos que tendem a ser considerados
abusivos pela jurisprudência atual do TST. Recomenda-se NÃO assinar (se
ainda em negociação) ou, se já assinada, procurar advogado trabalhista
imediatamente para avaliação de medida judicial.

PRÓXIMO PASSO INTERNO:
Encaminhar o caso para advogado trabalhista responsável da banca,
priorizando como atendimento URGENTE devido ao perfil de risco.
```

## O que observar no terminal

- O orquestrador deve identificar o domínio em 1 iteração e despachar UMA vez.
- O contador de fan-out fica em `1/3`.
- O especialista responde em ~3 segundos (Haiku).
- O parecer final do orquestrador é PT-BR em linguagem de cliente, sem repetir o jargão "TST" cru.

## Modo seco para estudar a mecânica

```bash
python agent.py --dry-run --task "..."
```

Em dry-run, o despacho é simulado e o orquestrador também não chama API real. Use para ler o trace e entender o fluxo sem gastar token.
