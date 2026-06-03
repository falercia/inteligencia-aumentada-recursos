# Exemplo 2 — Consulta multidomínio (despacho duplo)

## Comando

```bash
python agent.py --task "Tive um acidente em horário de trabalho na semana passada — torci o tornozelo numa escada com manutenção atrasada. Meu chefe se recusa a abrir CAT e diz que devo pagar a consulta médica. Posso forçar?" --verbose
```

## O que o orquestrador deve fazer

1. **Reconhecer dois domínios na consulta**:
   - Clínico: torção de tornozelo, semana passada — exige triagem de urgência.
   - Jurídico-trabalhista: recusa de abertura de CAT (Comunicação de Acidente de Trabalho) — exige triagem da legalidade da recusa.

2. **Despachar duas vezes**, cada despacho com a parte relevante da consulta:
   - `especialista_clinico_triagem`: "Torci o tornozelo na semana passada num acidente de trabalho. Preciso de orientação clínica."
   - `especialista_juridico_trabalhista`: "Meu empregador se recusa a abrir CAT após acidente em horário de trabalho. É legal? Quais meus direitos?"

3. **Consolidar** em parecer único, com dois blocos (um por domínio).

## Saída esperada (esqueleto)

```
DOMÍNIO IDENTIFICADO: múltiplo (clínico + jurídico-trabalhista)

CLASSIFICAÇÃO DO ESPECIALISTA — CLÍNICO:
Torção de tornozelo com mais de 5 dias sem avaliação. Triagem: AMARELO
(pode evoluir com dor crônica se não houver avaliação ortopédica). Próximo
passo: consultar ortopedista nos próximos dois dias úteis.

RECOMENDAÇÃO PARA O CLIENTE — CLÍNICO:
Procure atendimento ortopédico em até 48 horas. Use gelo e compressa nos
intervalos. Evite carga até a avaliação.

PRÓXIMO PASSO INTERNO — CLÍNICO:
Não há ação interna; cliente foi orientado a buscar atendimento direto.

CLASSIFICAÇÃO DO ESPECIALISTA — JURÍDICO-TRABALHISTA:
Recusa de abertura de CAT por empregador após acidente de trabalho
configura descumprimento de obrigação legal (Lei 8.213/91). Classe de
risco: ALTO. O empregado pode (a) comunicar diretamente ao INSS, (b)
registrar a recusa em sindicato ou MPT, (c) procurar advogado.

RECOMENDAÇÃO PARA O CLIENTE — JURÍDICO:
A recusa de seu empregador em abrir CAT é potencialmente ilegal. Você
pode emitir a CAT diretamente no INSS (Meu INSS) ou via sindicato. Não
deixe passar — a CAT é direito seu e protege benefícios previdenciários.

PRÓXIMO PASSO INTERNO — JURÍDICO:
Encaminhar para advogado trabalhista da banca em até 24h. Caso classe ALTO.
```

## O que observar no terminal

- O contador de fan-out termina em `2/3`.
- O `--verbose` mostra duas chamadas distintas, cada uma com sua tool e input.
- O orquestrador identifica os dois domínios sem precisar de pergunta de esclarecimento.

## Variação útil

Teste com `--max-fan-out 1` e observe o gate bloqueando o segundo despacho. O orquestrador deve então reconhecer o limite e devolver parecer parcial, sinalizando que o segundo domínio não foi atendido — comportamento defensável em produção sob pressão de custo.
