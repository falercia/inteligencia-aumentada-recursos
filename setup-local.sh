#!/bin/bash
# ============================================================================
# setup-local.sh
# ----------------------------------------------------------------------------
# Cria a estrutura completa do repositório inteligencia-aumentada-recursos.
# Execute DENTRO do diretório do repositório clonado:
#
#   cd inteligencia-aumentada-recursos
#   bash /caminho/para/setup-local.sh
#
# ============================================================================

set -e  # encerra ao primeiro erro

echo "═══════════════════════════════════════════════════════════════"
echo "  Inteligência Aumentada · Recursos — setup local v1.0.0"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ----------------------------------------------------------------------------
# 1. PASTAS DE TOPO
# ----------------------------------------------------------------------------

echo "▸ Criando pastas de topo..."

mkdir -p .github/ISSUE_TEMPLATE
mkdir -p prompts
mkdir -p evals
mkdir -p datasets
mkdir -p agents
mkdir -p mcp
mkdir -p notebooks

# ----------------------------------------------------------------------------
# 2. LICENSES
# ----------------------------------------------------------------------------

echo "▸ Gerando LICENSE-MIT e LICENSE-CC-BY..."

cat > LICENSE-MIT << 'EOF'
MIT License

Copyright (c) 2026 Fabio Garcia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Aplicável aos scripts Python, notebooks, exemplos de agente, servidores MCP
e quaisquer outros arquivos de código deste repositório.
EOF

cat > LICENSE-CC-BY << 'EOF'
Creative Commons Attribution 4.0 International License (CC BY 4.0)

Copyright (c) 2026 Fabio Garcia

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose,
  even commercially.

Under the following terms:
- Attribution — You must give appropriate credit to Fabio Garcia and to the
  work "Inteligência Aumentada · Os Invariantes da IA", provide a link to
  the license, and indicate if changes were made.

No additional restrictions — You may not apply legal terms or technological
measures that legally restrict others from doing anything the license permits.

Full text: https://creativecommons.org/licenses/by/4.0/legalcode

Aplicável aos prompts em XML, golden sets, anti-padrões, métricas e toda
documentação editorial deste repositório.
EOF

# ----------------------------------------------------------------------------
# 3. CHANGELOG E CONTRIBUTORS
# ----------------------------------------------------------------------------

echo "▸ Gerando CHANGELOG.md e CONTRIBUTORS.md..."

cat > CHANGELOG.md << 'EOF'
# Changelog

Todas as mudanças relevantes deste repositório são documentadas aqui, com
data, motivo e impacto observado em golden set ou em produção.

## [v1.0.0] — 2026-06-XX

### Adicionado
- 30 prompts profissionais em qualidade plena, com:
  - XML completo (persona, constituição, contexto, tarefa, formato, prefill, self-critique)
  - Golden set de 20 casos por prompt (fáceis, médios, limítrofes)
  - Anti-padrões observados
  - Métrica de qualidade quantitativa
- Estrutura inicial de pastas para evals, datasets, agents, mcp, notebooks
- README principal com pacto livro-repositório explícito
- Templates de issue para contribuição da comunidade

### Distribuição por domínio
- 4 prompts em Jurídico (LEG)
- 3 prompts em Saúde (MED)
- 4 prompts em Financeiro (FIN)
- 4 prompts em SaaS (SAAS)
- 3 prompts em Suporte (SUP)
- 3 prompts em RH
- 3 prompts em Marketing (MKT)
- 3 prompts em Educação (EDU)
- 3 prompts em Transversais (TR)

EOF

cat > CONTRIBUTORS.md << 'EOF'
# Contribuidores

Pessoas que ajudaram a calibrar, corrigir ou expandir este repositório.

## Autor e editor responsável

- **Fabio Garcia** — autor da obra Inteligência Aumentada, editor responsável
  pela curadoria, calibração e revisão mensal do conteúdo.

## Calibração de domínio especialista

(Preenchido conforme contribuições qualificadas chegarem.)

## Correção factual

(Preenchido conforme contribuições qualificadas chegarem.)

---

Para contribuir, leia [CONTRATO.md](./CONTRATO.md) e siga os templates de
issue em [.github/ISSUE_TEMPLATE/](./.github/ISSUE_TEMPLATE/).
EOF

# ----------------------------------------------------------------------------
# 4. CONTRATO
# ----------------------------------------------------------------------------

echo "▸ Gerando CONTRATO.md..."

cat > CONTRATO.md << 'EOF'
# Contrato de Manutenção e Contribuição

## Política editorial

Este repositório é mantido pelo autor da obra Inteligência Aumentada, com
cadência de release **mensal** nos primeiros doze meses pós-lançamento, e
**trimestral** a partir do décimo terceiro mês. Releases emergenciais fora
dessa cadência podem acontecer em casos de correção regulatória, factual
crítica ou de segurança.

## Tipos de contribuição aceitos

### 1. Calibração de golden set por especialista

Você é profissional sênior no domínio (advogado, médico, analista financeiro,
RH, professor, etc.) e identifica caso limítrofe não coberto pelos 20 casos
atuais, ou divergência entre saída esperada e prática profissional do seu
campo. Abra issue com o template `golden-set-calibration.md`.

### 2. Correção factual ou de referência

Você identifica referência jurisprudencial inexata, artigo de lei mal citado,
paper com identificador errado, número de benchmark desatualizado. Abra issue
com o template `factual-correction.md` e cite a fonte primária correta.

### 3. Sugestão de novo prompt

Você identifica caso de uso recorrente que não está coberto pelos 30 prompts
atuais. Abra issue com o template `new-prompt-suggestion.md` e descreva a dor,
o domínio e por que a biblioteca atual não resolve.

## O que NÃO é aceito

- Pull requests com mudanças editoriais não solicitadas
- Adição de prompts proprietários de empresas ou conteúdo confidencial
- Inclusão de dados pessoais reais, mesmo anonimizados
- Conteúdo sem base em fonte primária verificável

## Política de incorporação

Contribuições qualificadas são incorporadas na revisão mensal seguinte. O
editor responsável é Fabio Garcia, autor da obra. Atribuição em
`CONTRIBUTORS.md` é feita mediante autorização do contribuidor.

## Licença das contribuições

Ao contribuir, você concorda que sua contribuição será publicada sob as
licenças deste repositório (MIT para código, CC-BY 4.0 para conteúdo
editorial). Você mantém o crédito autoral da sua contribuição.
EOF

# ----------------------------------------------------------------------------
# 5. TEMPLATES DE ISSUE
# ----------------------------------------------------------------------------

echo "▸ Gerando templates de issue em .github/ISSUE_TEMPLATE/..."

cat > .github/ISSUE_TEMPLATE/golden-set-calibration.md << 'EOF'
---
name: Calibração de Golden Set
about: Sugerir caso novo ou correção em golden set existente por especialista do domínio
title: "[GOLDEN] P-XXX-NN: <descrição curta>"
labels: golden-set, contribuicao-especialista
---

## Prompt afetado

P-XXX-NN — <nome do prompt>

## Tipo de contribuição

- [ ] Novo caso para golden set
- [ ] Correção de saída esperada em caso existente
- [ ] Sugestão de antipadrão observado em produção

## Sua qualificação profissional

(Descreva brevemente sua experiência no domínio. Ex: "Advogada trabalhista
sênior com 15 anos de prática em TST".)

## Descrição do caso

**Input:**
<descrição do input>

**Saída esperada:**
<descrição da saída esperada conforme sua prática profissional>

**Por que importa:**
<explicação de por que esse caso é representativo ou crítico>

## Fonte primária quando aplicável

<jurisprudência, artigo de lei, paper, norma técnica, etc.>

## Autoriza atribuição em CONTRIBUTORS.md?

- [ ] Sim, com meu nome
- [ ] Sim, anônimo
- [ ] Não
EOF

cat > .github/ISSUE_TEMPLATE/factual-correction.md << 'EOF'
---
name: Correção Factual
about: Apontar erro de fato, referência ou número em qualquer prompt
title: "[FATO] P-XXX-NN: <descrição curta>"
labels: correcao-factual
---

## Localização do erro

**Prompt:** P-XXX-NN — <nome>
**Arquivo:** prompt.xml | golden-set.yaml | anti-padroes.md | README.md
**Trecho exato:**

```
<cole o trecho com o erro>
```

## Erro identificado

<descreva o erro>

## Correção sugerida

<descreva a correção>

## Fonte primária

<URL, citação de norma, paper, regulamentação, etc.>

## Urgência

- [ ] Crítica (impacto regulatório ou risco de erro material em uso)
- [ ] Alta (afeta confiabilidade do prompt)
- [ ] Média (melhoria editorial)
- [ ] Baixa (refinamento)
EOF

cat > .github/ISSUE_TEMPLATE/new-prompt-suggestion.md << 'EOF'
---
name: Sugestão de Novo Prompt
about: Propor inclusão de novo prompt na biblioteca
title: "[NOVO] <domínio>: <caso de uso>"
labels: sugestao-novo-prompt
---

## Domínio sugerido

Jurídico | Saúde | Financeiro | SaaS | Suporte | RH | Marketing | Educação | Transversal | Outro

## Caso de uso

<descrição da dor que o prompt resolveria>

## Por que a biblioteca atual não resolve

<argumente que nenhum dos 30 prompts atuais cobre esse caso, e por quê>

## Exemplo de input típico

<dê um exemplo concreto de input>

## Exemplo de saída esperada

<dê um exemplo concreto de saída>

## Frequência observada

<com que frequência esse caso aparece em sua experiência ou no mercado>

## Você está disposto a colaborar na construção?

- [ ] Sim, posso ajudar a redigir o prompt e calibrar o golden
- [ ] Sim, posso ajudar apenas com a calibração
- [ ] Não, estou apenas sugerindo
EOF

# ----------------------------------------------------------------------------
# 6. README DAS PASTAS DE TOPO
# ----------------------------------------------------------------------------

echo "▸ Gerando README.md das pastas (prompts, evals, datasets, agents, mcp, notebooks)..."

cat > prompts/README.md << 'EOF'
# Biblioteca de Prompts Profissionais — v1.0.0

Trinta prompts profissionais em qualidade plena, organizados por domínio.

## Padrão de adoção

1. **Clone o repositório.**
2. **Identifique o prompt mais próximo do seu domínio.**
3. **Copie o diretório inteiro** para seu repositório interno.
4. **Adapte a constituição** ao seu contexto.
5. **Construa seu golden set próprio** com pelo menos 20 casos do seu tráfego real.
6. **Rode `eval.py`** (a partir da release v1.1.0) antes de cada release.

## Estrutura de cada pasta

```
P-XXX-NN-slug/
├── README.md          ← ficha conceitual e instruções de uso
├── prompt.xml         ← XML completo
├── golden-set.yaml    ← 20 casos com input + saída esperada
├── anti-padroes.md    ← antipadrões observados
├── changelog.md       ← histórico do prompt
└── exemplos-saida/    ← outputs reais anonimizados
```

## Índice por domínio

### Jurídico (LEG)
- `P-LEG-01-clausula-nao-concorrencia-clt` — Revisão de cláusula de não-concorrência CLT
- `P-LEG-02-nda-lgpd-compliant` — Análise de NDA brasileiro LGPD-compliant
- `P-LEG-03-red-flags-contrato-ma` — Red flags em contrato M&A
- `P-LEG-04-parecer-compliance-lgpd` — Parecer sobre compliance LGPD

### Saúde (MED)
- `P-MED-01-triagem-sintomas` — Triagem de sintomas com recusa por escopo
- `P-MED-02-sumula-prontuario` — Súmula de prontuário
- `P-MED-03-interacao-medicamentosa` — Alerta de interação medicamentosa

### Financeiro (FIN)
- `P-FIN-01-anomalia-extrato` — Detecção de anomalia em extrato
- `P-FIN-02-risco-credito-pf` — Classificação de risco de crédito PF
- `P-FIN-03-sumula-itr` — Súmula de relatório trimestral ITR
- `P-FIN-04-analise-carteira` — Análise de carteira recomendada

### SaaS e Produto (SAAS)
- `P-SAAS-01-feature-request` — Classificação de feature request por persona
- `P-SAAS-02-sumula-nps` — Súmula de NPS qualitativo
- `P-SAAS-03-release-notes` — Geração de release notes
- `P-SAAS-04-churn-signal` — Análise de churn signal

### Suporte (SUP)
- `P-SUP-01-severidade-ticket` — Classificação de ticket em severidade
- `P-SUP-02-resposta-empatica` — Resposta empática a reclamação
- `P-SUP-03-escalonamento` — Decisão sobre escalonamento

### RH
- `P-RH-01-triagem-curriculo` — Triagem de currículo com fit
- `P-RH-02-feedback-360` — Análise de feedback 360
- `P-RH-03-descritivo-vaga` — Descritivo de vaga em linguagem inclusiva

### Marketing (MKT)
- `P-MKT-01-copy-ab` — Geração de copy A/B testável
- `P-MKT-02-brand-voice` — Análise de brand voice
- `P-MKT-03-sumula-pesquisa` — Súmula de pesquisa de mercado

### Educação (EDU)
- `P-EDU-01-plano-aula` — Geração de plano de aula
- `P-EDU-02-avaliacao-rubrica` — Avaliação rubrica-baseada
- `P-EDU-03-resposta-socratica` — Resposta socrática a dúvida do aluno

### Transversais (TR)
- `P-TR-01-extracao-json` — Extração estruturada com schema JSON
- `P-TR-02-multi-label` — Classificação multi-label
- `P-TR-03-recusa-fallback` — Recusa estruturada com fallback
EOF

cat > evals/README.md << 'EOF'
# Evals

Scripts e padrões para avaliação de prompts em CI/CD e em produção.

## Estado atual (v1.0.0)

Stub estrutural. O `eval_runner.py` executável chega na **release v1.1.0**
(jul/2026).

## O que estará aqui

- `eval_runner.py` — runner para executar golden sets contra um modelo
- `llm_judge.py` — juiz LLM calibrado para avaliação semântica
- `metrics.py` — métricas padronizadas por tipo de prompt
- `regression_check.py` — comparação automática de releases

## Referência conceitual

Capítulo 39 (Evals) e Framework 8 (Pirâmide da Avaliação) do livro.
EOF

cat > datasets/README.md << 'EOF'
# Datasets

Golden sets compilados em formato JSONL e YAML, exportados dos diretórios
de cada prompt para facilitar carregamento pelo `eval_runner.py`.

## Estado atual (v1.0.0)

Stub estrutural. A compilação automática chega na **release v1.1.0**.

## O que estará aqui

- `golden-sets-v1.jsonl` — todos os 600 casos (30 prompts × 20 casos) em JSONL
- `golden-sets-by-domain/` — segmentação por domínio
- `adversarial/` — conjunto adversarial para testes de jailbreak

## Referência conceitual

Capítulo 39 (Evals) e Capítulo 41 (Alignment) do livro.
EOF

cat > agents/README.md << 'EOF'
# Agents

Exemplos de agentes que compõem prompts da biblioteca em fluxos práticos.

## Estado atual (v1.0.0)

Stub estrutural. Primeiros exemplos chegam na **release v1.3.0** (set/2026).

## O que estará aqui

- `triage-agent/` — agente que orquestra P-SUP-01, P-SUP-02, P-SUP-03 em fluxo
- `due-diligence-agent/` — agente jurídico orquestrando P-LEG-02, P-LEG-03, P-LEG-04
- `customer-success-agent/` — agente CS orquestrando P-SAAS-04 + P-SUP-02

## Referência conceitual

Capítulo 12 (Agentes), Capítulo 40 (LLMOps) e Framework 3 (Escala de Propriedade).
EOF

cat > mcp/README.md << 'EOF'
# MCP

Servidores MCP de referência, minimalistas e auditáveis.

## Estado atual (v1.0.0)

Stub estrutural. Primeiro servidor chega na **release v1.4.0** (out/2026).

## O que estará aqui

- `mcp-golden-set/` — servidor MCP que expõe golden sets como ferramentas
- `mcp-eval/` — servidor MCP que executa eval_runner como ferramenta
- `mcp-template/` — template mínimo para construir servidor MCP novo

## Referência conceitual

Capítulo 13 (MCP) e Framework 5 (Matriz de Cobertura de Integrações).
EOF

cat > notebooks/README.md << 'EOF'
# Notebooks

Notebooks Python reproduzíveis para conceitos fundacionais.

## Estado atual (v1.0.0)

Stub estrutural. Primeiros notebooks chegam na **release v1.2.0** (ago/2026).

## O que estará aqui

- `01-tokenizacao.ipynb` — tokenização aplicada, com tiktoken
- `02-context-window.ipynb` — efeito lost-in-the-middle visualizado
- `03-embeddings.ipynb` — espaço vetorial e similaridade aplicada
- `04-prompt-caching.ipynb` — economia de tokens com caching
- `05-eval-judge-calibration.ipynb` — calibração de LLM-as-judge

## Referência conceitual

Capítulos 2, 3, 4, 5, 11, 39 do livro.
EOF

# ----------------------------------------------------------------------------
# 7. CRIAR 30 PASTAS DE PROMPTS COM ESTRUTURA MÍNIMA
# ----------------------------------------------------------------------------

echo "▸ Criando 30 pastas de prompts..."

# Lista de slugs dos 30 prompts
PROMPT_DIRS=(
  "P-LEG-01-clausula-nao-concorrencia-clt"
  "P-LEG-02-nda-lgpd-compliant"
  "P-LEG-03-red-flags-contrato-ma"
  "P-LEG-04-parecer-compliance-lgpd"
  "P-MED-01-triagem-sintomas"
  "P-MED-02-sumula-prontuario"
  "P-MED-03-interacao-medicamentosa"
  "P-FIN-01-anomalia-extrato"
  "P-FIN-02-risco-credito-pf"
  "P-FIN-03-sumula-itr"
  "P-FIN-04-analise-carteira"
  "P-SAAS-01-feature-request"
  "P-SAAS-02-sumula-nps"
  "P-SAAS-03-release-notes"
  "P-SAAS-04-churn-signal"
  "P-SUP-01-severidade-ticket"
  "P-SUP-02-resposta-empatica"
  "P-SUP-03-escalonamento"
  "P-RH-01-triagem-curriculo"
  "P-RH-02-feedback-360"
  "P-RH-03-descritivo-vaga"
  "P-MKT-01-copy-ab"
  "P-MKT-02-brand-voice"
  "P-MKT-03-sumula-pesquisa"
  "P-EDU-01-plano-aula"
  "P-EDU-02-avaliacao-rubrica"
  "P-EDU-03-resposta-socratica"
  "P-TR-01-extracao-json"
  "P-TR-02-multi-label"
  "P-TR-03-recusa-fallback"
)

for dir in "${PROMPT_DIRS[@]}"; do
  mkdir -p "prompts/$dir/exemplos-saida"
  touch "prompts/$dir/prompt.xml"
  touch "prompts/$dir/golden-set.yaml"
  touch "prompts/$dir/anti-padroes.md"

  # Stub do changelog
  cat > "prompts/$dir/changelog.md" << EOF
# Changelog — $dir

## v1.0.0 — 2026-06-XX

Versão inicial publicada com biblioteca v1.0.0 do repositório.

- Golden set com 20 casos (fáceis, médios, limítrofes)
- Prefill ancorando início da resposta
- Self-critique calibrado contra a constituição
- Anti-padrões observados documentados
- Métrica de qualidade quantitativa
EOF

  # Stub do README (será substituído pela ficha conceitual real do livro)
  cat > "prompts/$dir/README.md" << EOF
# $dir

> Stub gerado por setup-local.sh.
> A ficha conceitual completa será populada por extract-prompts.py
> a partir do APX-L do livro.
EOF
done

# ----------------------------------------------------------------------------
# 8. .gitignore E ARQUIVOS DE QUALIDADE DE VIDA
# ----------------------------------------------------------------------------

echo "▸ Gerando .gitignore..."

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs e saídas locais
*.log
output/
tmp/
EOF

# ----------------------------------------------------------------------------
# 9. RESUMO FINAL
# ----------------------------------------------------------------------------

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Estrutura criada com sucesso!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Próximos passos:"
echo ""
echo "1. Rodar o script de extração para popular os 30 prompts:"
echo "   python3 \"$(dirname \"$0\")/extract-prompts.py\""
echo ""
echo "2. Copiar o README principal:"
echo "   cp \"$(dirname \"$0\")/README.md\" ."
echo ""
echo "3. Commitar e publicar:"
echo "   git add ."
echo "   git commit -m \"v1.0.0 — biblioteca completa com 30 prompts em qualidade plena\""
echo "   git tag v1.0.0"
echo "   git push origin main"
echo "   git push origin v1.0.0"
echo ""
