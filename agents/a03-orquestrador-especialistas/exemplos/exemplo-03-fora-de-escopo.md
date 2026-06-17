# Exemplo 3 — Fora de escopo (recusa explícita, sem despacho)

## Comando

```bash
python agent.py --task "Qual a melhor maneira de investir R$ 50 mil em renda fixa hoje? Quais bancos têm os melhores CDBs?"
```

## O que o orquestrador deve fazer

1. **Reconhecer que o domínio é financeiro/investimentos** — não casa com nenhum dos três especialistas registrados (jurídico-trabalhista, clínico, suporte técnico SaaS).
2. **NÃO despachar** para nenhum especialista.
3. **NÃO responder** como se fosse especialista (o orquestrador não tem competência de domínio).
4. **Devolver mensagem de fora de escopo**, sugerindo o canal correto.

## Saída esperada

```
DOMÍNIO IDENTIFICADO: fora de escopo

CLASSIFICAÇÃO DO ESPECIALISTA:
Não aplicável — nenhum especialista foi consultado.

RECOMENDAÇÃO PARA O CLIENTE:
Esta consulta envolve recomendação de investimento financeiro, que está
fora dos domínios atendidos por esta central (jurídico-trabalhista,
clínico, suporte técnico). Encaminhe a consulta ao seu assessor de
investimentos credenciado pela CVM ou à área de investimentos do seu banco.

PRÓXIMO PASSO INTERNO:
Marcar o ticket como "fora de escopo — financeiro" e fechar.
```

## O que observar no terminal

- Contador de fan-out: `0/3` (nenhum despacho feito).
- A iteração é única — o orquestrador identifica fora de escopo na primeira passada e encerra.
- Custo: aproximadamente 1 chamada do orquestrador, sem especialistas.

## Por que este exemplo importa

Recusar atender fora de escopo é uma das competências mais subestimadas em sistemas multiagente. O agente que tenta cobrir tudo vira generalista medíocre e perde confiança do usuário. O agente disciplinado reconhece a fronteira do que pode entregar com qualidade e encaminha o resto explicitamente — este é o Invariante 1 da obra (Plausibilidade não é verdade) aplicado à arquitetura.

## Variação útil para teste adversarial

Teste com pergunta que parece estar no escopo mas não está:

```bash
python agent.py --task "Posso processar meu banco por ter me cobrado tarifa errada?"
```

Esperado: fora de escopo (jurídico-civil/consumidor não é jurídico-trabalhista). O orquestrador NÃO deve despachar para `especialista_juridico_trabalhista` só porque tem "processar" e "jurídico" na query — isso seria classificação preguiçosa.
