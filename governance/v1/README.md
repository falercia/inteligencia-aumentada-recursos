# Caderno de Governança de IA · v1.0

> Caderno operacional executável do Apêndice O da obra **Inteligência Aumentada · Os Invariantes da IA**.
> O padrão dura, o número muda. O método mora no livro, o caderno mora aqui.

---

## O que vive nesta pasta

O caderno é o artefato prometido pelo Framework Seis e foi pensado como instrumento vivo, assinado pela diretoria, revisado em cadência trimestral, atualizado a cada incidente material. Esta pasta entrega o caderno em dois formatos complementares.

| Arquivo | Para que serve |
|---|---|
| [`00-modelo-caderno-completo.md`](./00-modelo-caderno-completo.md) | O caderno inteiro em peça única, com 6 páginas, pronto para imprimir, assinar e arquivar |
| [`01-identificacao-escopo-principios.md`](./01-identificacao-escopo-principios.md) | Seção 1 fatiada, para edição independente pelo patrocinador executivo |
| [`02-raci-comite.md`](./02-raci-comite.md) | Seção 2 fatiada, para edição independente pelo CTO em conjunto com o jurídico |
| [`03-aup.md`](./03-aup.md) | Seção 3 fatiada, para edição independente por RH em conjunto com o jurídico |
| [`04-controles-canonicos.md`](./04-controles-canonicos.md) | Seção 4 fatiada, para edição independente pelo CTO em conjunto com segurança |
| [`05-plano-incidente.md`](./05-plano-incidente.md) | Seção 5 fatiada, para edição independente por segurança em conjunto com o jurídico |
| [`06-assinaturas-revisao.md`](./06-assinaturas-revisao.md) | Seção 6 fatiada, para colher assinaturas e marcar a próxima revisão |
| [`ANEXOS.md`](./ANEXOS.md) | Lista dos seis anexos referenciados, com modelos clonáveis |
| [`CHANGELOG.md`](./CHANGELOG.md) | Changelog editorial do caderno, datado a cada revisão pública |

A divisão em seções fatiadas resolve o problema clássico de fazer seis áreas editarem o mesmo arquivo Word ao mesmo tempo, com conflito de versão a cada commit. Cada área edita o seu pedaço em ramo próprio, e o caderno único é regenerado a partir das seções no momento de imprimir e assinar.

---

## Como clonar e adaptar em uma janela de meio-período

Quatro horas distribuídas entre as áreas responsáveis bastam para a primeira passagem do caderno em uma organização de porte médio. O caderno não nasce perfeito, ele nasce assinado e em revisão programada.

1. **Copie a pasta inteira para o repositório interno da sua organização.** A licença é CC-BY 4.0 para o conteúdo, com atribuição a Fabio Garcia e à obra Inteligência Aumentada.

2. **Distribua a edição entre as áreas.** Patrocinador executivo edita a seção 1, CTO edita as seções 2 e 4, jurídico revisa a 3, segurança edita a 5, RH treina a AUP em onboarding após a assinatura.

3. **Preencha placeholders nomeados, jamais deixe `[a definir]` em nenhum campo.** Caderno com placeholder em produção é álibi quando o incidente vier, não defesa.

4. **Anexe evidência por controle na seção 4.** Maturidade três sem artefato anexado vira maturidade um disfarçada na primeira auditoria séria.

5. **Marque a próxima revisão no calendário da diretoria no mesmo ato da assinatura.** Sem data no calendário, revisão escorrega para o trimestre seguinte e o caderno entra em coma silencioso.

6. **Adicione o seu adendo setorial em pasta irmã** quando operar em setor criticamente regulado (instituição financeira sob CMN, saúde sob ANS, setor público sob LGPD setorial). O adendo não substitui o caderno, ele se anexa como camada adicional.

---

## Quando este modelo se aplica

O caderno foi calibrado para organização brasileira entre cinquenta e cinco mil colaboradores, com uso de IA em produção em pelo menos um caso de uso material, e sem operação em setor criticamente regulado em que o regulador exija instrumento próprio.

A discussão completa sobre adoção integral versus adendo setorial está na ficha do Apêndice O no livro, e em forma resumida na seção 1.4 do `00-modelo-caderno-completo.md`.

---

## Pacto com o livro

O livro entrega o **método** que sobrevive à próxima geração de modelo e à próxima onda regulatória, na forma da ficha conceitual do Apêndice O com a anatomia em seis blocos, os nove princípios condutores, os sete padrões de adaptação, os dez anti-padrões transversais e os sete indicadores de caderno vivo.

Este repositório entrega o **número** datado, que muda a cada revisão pública, na forma do caderno operacional executável com placeholders nomeados, modelos dos seis anexos e changelog datado.

Quem só lê o livro sai com método e precisa montar o caderno do zero. Quem usa só este repositório sem ler o livro opera no escuro, porque não vai entender por que cada bloco está naquela posição, e vai cortar exatamente o bloco que sustenta a estrutura. Quem opera com os dois, sai com método e ativo pronto.

---

## Cadência de revisão

Este caderno segue a cadência geral declarada do repositório acompanhante, com revisão pública nos primeiros doze meses pós-lançamento da obra. Edições intermediárias são feitas em três situações, conforme a seção 6.3 do caderno: SEV-1 com aprendizado relevante, mudança regulatória material, substituição de fornecedor ou modelo de fronteira em uso pela organização-referência.

O `CHANGELOG.md` registra data, item alterado e motivo de cada revisão.

---

## Como contribuir

Contribuições especialistas são bem-vindas e seguem o `CONTRATO.md` do repositório raiz. Três categorias têm prioridade para o caderno.

1. **Adendos setoriais.** Você é DPO, compliance officer, jurídico setorial ou CTO de organização em setor regulado, e tem versão calibrada do caderno para o seu setor (financeiro, saúde, jurídico, educação, setor público). Abra issue com o template `governance-sector-addendum`.

2. **Calibração de RACI por porte.** Você é CTO ou Head de Tecnologia em organização entre cinquenta e cinco mil colaboradores, e a sua matriz RACI específica do negócio cobre classes de decisão que o modelo base não cobre. Abra issue com o template `raci-calibration`.

3. **Anti-padrões observados em prática.** Você viu, em organização sua ou em consultoria, padrão de governança fictícia que merece ser nomeado na próxima revisão da ficha do livro. Abra issue com o template `governance-anti-pattern`.

Todas as contribuições qualificadas são incorporadas na revisão pública seguinte, com atribuição em `CONTRIBUTORS.md` do repositório raiz quando o contribuidor autoriza.

---

*Caderno de Governança v1.0 · Inteligência Aumentada · Recursos · Fabio Garcia · 2026.*
