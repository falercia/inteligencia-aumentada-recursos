# Seção 2 — RACI e Comitê de IA

> Edição independente. Responsável: CTO em conjunto com jurídico.
> Quando preenchida, vai para a página 2 do `00-modelo-caderno-completo.md`.

---

## 2.1 Matriz RACI por classe de decisão

A matriz abaixo cobre as classes de decisão recorrentes em operação de IA. **Cada classe tem um único Accountable, sem exceção.** Esta é a regra fundamental do Princípio Oito, Responsabilidade Indelegável.

| Classe de decisão | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Adoção de novo caso de uso de IA | Líder do produto ou área | CTO | Jurídico, DPO, Segurança, Financeiro | Comitê de IA |
| Aprovação de fornecedor ou modelo de terceiros | Time de Engenharia | CTO | Jurídico, Segurança, Sourcing | Comitê de IA |
| Promoção de agente entre níveis de autonomia | AI Engineer responsável | CTO | Owner do produto, Operações, Segurança | Comitê de IA |
| Definição de RACI de caso específico | AI Engineer responsável | CTO | Owner do produto, RH se aplicável | Comitê de IA |
| Resposta a incidente de severidade alta | On-call responsável | CTO | DPO, Jurídico, Comunicação | Diretoria |
| Atualização do AUP de uso de IA | RH | CEO ou conselho | Jurídico, DPO, CTO | Toda organização |
| Revisão deste caderno | Comitê de IA | CEO | Diretoria | Toda organização |

### 2.1.1 Como customizar a matriz ao negócio

As sete classes acima são piso, jamais teto. Customize ao seu contexto seguindo três regras:

1. **Adicione classes específicas do negócio.** Empresa que opera com agente autônomo em produção precisa adicionar classe própria para "promoção de tier de autonomia", com gates de observabilidade explícitos. Empresa em setor regulado precisa adicionar classe para "submissão de uso de IA a órgão regulador".

2. **Substitua o Accountable apenas quando o cargo correspondente não existe na organização.** Empresa sem CTO formal pode atribuir o Accountable a "Head de Tecnologia", "Diretor de Engenharia" ou cargo equivalente, sempre nominado.

3. **Nunca distribua Accountable entre duas pessoas.** O Princípio Oito é categórico. Duas pessoas Accountables significa ninguém Accountable na hora do incidente. Quando a decisão exigir aprovação cruzada, mantenha um Accountable e adicione o segundo como Consulted obrigatório com poder de veto registrado em ata.

---

## 2.2 RACIs específicos por caso de uso em produção

A matriz acima cobre classes genéricas. Cada caso de uso de IA em produção exige RACI específico assinado, em anexo controlado, conforme o controle 7 da seção 4.

O modelo de RACI específico está em `ANEXOS.md`, em formato clonável.

---

## 2.3 Comitê de IA

O Comitê de IA é o órgão executivo permanente de governança. **Não é fórum de debate filosófico.**

### 2.3.1 Composição mínima

- CTO ou Head de Tecnologia
- DPO ou encarregado de dados
- Representante do Jurídico
- Representante de Segurança da Informação
- Representante de Operações

A organização pode estender a composição com representante de produto, financeiro ou compliance, sem reduzir o piso mínimo.

### 2.3.2 Cadência

Reunião mensal de uma hora, com pauta fixa:

- Revisão de incidentes do mês
- Novos casos de uso submetidos
- Revisão de RACI específicos
- Status do Apêndice J no contexto da organização (modelos, preços, regulação)
- Status do AUP, treinamentos e violações

### 2.3.3 Mandato

O comitê decide unilateralmente sobre:

- Adoção de novo modelo
- Promoção de agente entre níveis de autonomia
- Aprovação de exceções ao AUP
- Encaminhamento de incidente severo à diretoria

Decisões que excedam o mandato escalam à diretoria com parecer técnico do comitê.

### 2.3.4 Quórum mínimo

Três dos cinco membros, com obrigatoriedade da presença do CTO ou substituto formal. Reunião sem quórum gera ata de não-deliberação e remarca para a semana seguinte.

### 2.3.5 Ata

Toda reunião gera ata em até três dias úteis, com:

- Decisões deliberadas
- Votação quando aplicável
- Próximos passos com responsável e prazo
- Itens encaminhados à diretoria

Ata arquivada por cinco anos em repositório controlado. Anti-padrão: ata fora do prazo é equivalente a reunião não realizada para fins de auditoria.

---

*Seção 2 do Caderno de Governança v1.0. Edição independente pelo CTO em conjunto com jurídico. Integra-se ao `00-modelo-caderno-completo.md` no momento da consolidação.*
