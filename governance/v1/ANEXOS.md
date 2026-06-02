# Anexos do Caderno de Governança v1.0

> Modelos clonáveis dos seis anexos referenciados na seção 6.2 do caderno.
> Cada anexo é instrumento controlado pela organização, versionado fora deste repositório.

---

## Anexo 1 — Lista de ferramentas de IA aprovadas

**Responsável operacional.** Comitê de IA, em rotação trimestral entre membros.
**Frequência de atualização.** Contínua, com revisão fechada a cada reunião mensal.
**Canal de versionamento.** Intranet corporativa, em página com histórico de versões.

### Modelo clonável

| Categoria | Ferramenta | Versão | Aprovação (data) | Próxima revisão | Owner | Classificação de dado permitida | Restrições |
|---|---|---|---|---|---|---|---|
| Assistente geral | [exemplo: Claude.ai Enterprise] | [versão] | [DD/MM/AAAA] | [DD/MM/AAAA] | [nome] | Público, Interno | Sem dado pessoal sensível |
| Codificação | [exemplo: GitHub Copilot Business] | | | | | | |
| Geração de imagem | [exemplo: ferramenta X] | | | | | | |
| Tradução | | | | | | | |
| Análise de dados | | | | | | | |
| Pesquisa | | | | | | | |

### Regras de alteração

1. Inclusão de nova ferramenta exige avaliação técnica e jurídica em até quinze dias úteis
2. Exclusão de ferramenta exige plano de migração com janela mínima de trinta dias
3. Toda alteração registra data, motivo e responsável

---

## Anexo 2 — AUP completa com casos práticos e FAQ

**Responsável operacional.** RH, com revisão pelo Comitê de IA.
**Frequência de atualização.** Anual ou pós-incidente material com aprendizado de uso indevido.
**Canal de versionamento.** Intranet corporativa, com aprovação registrada por colaborador.

### Estrutura recomendada

1. Princípios da política (resumo da seção 3.1 do caderno)
2. O que é permitido (cópia da seção 3.2 ampliada com 10-15 exemplos práticos da organização)
3. O que é proibido (cópia da seção 3.3 ampliada com 10-15 exemplos práticos)
4. Sanções (tabela da seção 3.4 ampliada com casos concretos anonimizados)
5. Canal de dúvida (seção 3.5)
6. Treinamento (seção 3.6 ampliada com plano de aprendizagem)
7. **FAQ** com 30 a 50 perguntas frequentes, organizadas por papel (executivo, gerente, colaborador técnico, colaborador administrativo, prestador externo)

A FAQ é o instrumento que mais drift sofre com o tempo, porque ferramentas novas geram dúvidas novas. Revisão trimestral da FAQ é prática recomendada, ainda que a AUP base seja revisada anualmente.

---

## Anexo 3 — Registro de RACI por caso de uso de IA em produção

**Responsável operacional.** CTO, em delegação para AI Engineers responsáveis.
**Frequência de atualização.** A cada promoção de caso de uso para produção, e a cada mudança de Accountable.
**Canal de versionamento.** Planilha controlada com histórico, ou repositório Git.

### Modelo clonável por caso de uso

```yaml
caso_de_uso: "Triagem de tickets de suporte com classificação de severidade"
identificador: "CU-SUP-001"
data_de_entrada_em_producao: "DD/MM/AAAA"
proxima_revisao: "DD/MM/AAAA"
escopo:
  o_que_cobre: "Classificação de tickets recebidos via formulário web em SEV-1 a SEV-4"
  o_que_nao_cobre: "Resposta ao cliente, escalonamento, fechamento"
modelo_usado: "[família, versão]"
prompt_versionado_em: "[URL do prompt no repositório interno]"
golden_set_versionado_em: "[URL]"
raci:
  responsible: "[nome] - AI Engineer"
  accountable: "[nome] - CTO"
  consulted:
    - "[nome] - Owner de produto"
    - "[nome] - Operações de suporte"
  informed:
    - "Comitê de IA (via ata mensal)"
nivel_de_autonomia_F3: "[nível 0 a 5]"
gates_de_promocao_para_proximo_nivel: "[lista]"
metricas_de_qualidade:
  - "Aderência humana em 100% dos casos do golden set"
  - "Taxa de SEV-1 correto > 95% em produção"
  - "Taxa de falso SEV-1 < 5%"
assinaturas:
  responsible: "[assinatura, data]"
  accountable: "[assinatura, data]"
```

A taxa de cobertura nominal (número de casos de uso em produção com RACI específico assinado dividido pelo total de casos em produção) é evidência direta para o controle 7.

---

## Anexo 4 — Trilha do Número da organização

**Responsável operacional.** Comitê de IA, com colaboração do Sourcing.
**Frequência de atualização.** Mensal, em sintonia com a revisão pública do Apêndice J da obra.
**Canal de versionamento.** Documento interno com histórico, espelho do Apêndice J ajustado ao contexto da organização.

### Estrutura recomendada

Cada modelo, fornecedor, regulação ou benchmark relevante para a operação da organização tem ficha datada com:

- Identificação (nome, fornecedor, versão)
- Data de última atualização
- Preço negociado, contrato vigente, vencimento
- Posicionamento de risco da organização (alta dependência, baixa dependência, alternativas disponíveis)
- Próximo gate de revisão

A Trilha do Número interna é o instrumento que evita a organização ser surpreendida por mudança de preço, descontinuação de modelo, mudança regulatória ou substituição de fornecedor sem plano B.

---

## Anexo 5 — Catálogo de evals em produção

**Responsável operacional.** Engenharia, com revisão pelo Comitê de IA.
**Frequência de atualização.** A cada release de prompt ou modelo, e a cada incidente que exija nova eval.
**Canal de versionamento.** Repositório Git interno com tags semânticas, espelhado conforme F8.

### Estrutura recomendada por eval

```yaml
identificador: "EVAL-CU-SUP-001-classificacao-severidade"
caso_de_uso_associado: "CU-SUP-001"
nivel_F8:
  - "Base: 20 casos canônicos com saída ouro"
  - "Meio: 50 casos com ambiguidade controlada"
  - "Topo: 10 casos adversariais"
limiar_de_corte: "Pontuação agregada > 85%"
gate_em_CI: "Bloqueia merge se cair abaixo do limiar"
ultimo_resultado:
  data: "DD/MM/AAAA"
  pontuacao: "[valor]"
  observacoes: "[texto]"
proxima_revisao: "DD/MM/AAAA"
golden_set_em: "[URL]"
script_em: "[URL]"
```

A taxa de cobertura (casos de uso em produção com eval em CI dividido pelo total) é evidência direta para o controle 6.

---

## Anexo 6 — Registro de incidentes

**Responsável operacional.** Segurança, com colaboração de Engenharia.
**Frequência de atualização.** A cada incidente.
**Canal de versionamento.** Ferramenta de incidentes corporativa, com exportação trimestral para o caderno.

### Estrutura recomendada por incidente

```yaml
identificador: "INC-AAAAMMDD-NNN"
data_de_deteccao: "DD/MM/AAAA HH:MM"
data_de_conclusao: "DD/MM/AAAA HH:MM"
severidade: "SEV-X"
caso_de_uso_afetado: "CU-XXX-NNN"
descricao_breve: "[uma frase]"
causa_raiz: "[texto]"
clientes_afetados: "[número]"
dado_exposto: "[descrição factual]"
custo_estimado: "[valor]"
tempo_de_deteccao: "[minutos]"
tempo_de_resposta: "[minutos]"
aderencia_ao_playbook: "[total | parcial | nula, com nota]"
acoes_corretivas:
  - acao: "[texto]"
    responsavel: "[nome]"
    prazo: "DD/MM/AAAA"
    status: "[aberta | em andamento | concluída]"
postmortem_em: "[URL]"
licao_aprendida_no_caderno: "[seção e item afetados, se aplicável]"
```

O registro de incidentes é fonte primária da revisão trimestral. Sem registro estruturado, a memória institucional do incidente se perde e a próxima ocorrência repete a mesma falha.

---

*Anexos do Caderno de Governança v1.0. Cada anexo é instrumento controlado pela organização, versionado fora deste repositório. Os modelos clonáveis acima são piso, não teto.*
