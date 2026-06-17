# Instruções de push — v1.1.0

> Sessão de 2026-06-02. Pacote pronto em `_repositorio-acompanhante/` no local.

---

## O que sobe nesta release

| Arquivo de origem | Destino no repo |
|---|---|
| `evals/eval_runner.py` | `evals/eval_runner.py` |
| `evals/compile_golden_sets.py` | `evals/compile_golden_sets.py` |
| `evals/requirements.txt` | `evals/requirements.txt` |
| `evals/README.md` (sobrescreve) | `evals/README.md` |
| `datasets/README.md` (sobrescreve) | `datasets/README.md` |
| `README.md` raiz (atualizado) | `README.md` |
| `CHANGELOG-v1.1.0.md` (conteúdo) | adicionar ao topo de `CHANGELOG.md` |

---

## Comandos exatos

Assumindo que o repositório clonado fica em `~/Documents/Personal/Livros/inteligencia-aumentada-recursos/` (mesmo padrão da v1.0.1).

```bash
cd ~/Documents/Personal/Livros/inteligencia-aumentada-recursos

# 1. Copiar arquivos novos e atualizados
SRC="/Users/fabiogarcia/Documents/Personal/Livros/Ebook IA/_repositorio-acompanhante"

# evals/
mkdir -p evals
cp "$SRC/evals/eval_runner.py"          evals/
cp "$SRC/evals/compile_golden_sets.py"  evals/
cp "$SRC/evals/requirements.txt"        evals/
cp "$SRC/evals/README.md"               evals/

# datasets/
mkdir -p datasets
cp "$SRC/datasets/README.md"            datasets/

# README raiz (sobrescreve)
cp "$SRC/README.md"                     README.md

# CHANGELOG (acrescenta v1.1.0 ao topo do CHANGELOG existente)
# Edição manual recomendada: abrir CHANGELOG.md, colar o conteúdo de
# CHANGELOG-v1.1.0.md acima das entradas existentes, salvar.
#
# Alternativa via script:
{
  cat "$SRC/CHANGELOG-v1.1.0.md"
  echo ""
  echo "---"
  echo ""
  cat CHANGELOG.md
} > CHANGELOG.md.new && mv CHANGELOG.md.new CHANGELOG.md

# 2. Verificar diff antes de comitar
git status
git diff --stat

# 3. Commit + tag + push
git add evals/ datasets/ README.md CHANGELOG.md
git commit -m "v1.1.0 — Motor de avaliação executável (eval_runner.py + compile_golden_sets.py)"
git tag -a v1.1.0 -m "v1.1.0: eval_runner.py rodável, gate de CI, compilador de golden sets"
git push origin main
git push origin v1.1.0
```

---

## Validação local antes do push (recomendado)

```bash
cd ~/Documents/Personal/Livros/inteligencia-aumentada-recursos

# Confirma que eval_runner.py roda em dry-run (não chama API)
python evals/eval_runner.py --prompt P-LEG-01 --dry-run

# Se a saída mostrar "✗ FALHOU" com erro de golden.yaml não encontrado,
# isso é esperado nesta release: os YAMLs estão sob revisão pelo autor
# e serão publicados em v1.1.1 (patch) nos próximos dias.

# Confirma estrutura do compilador
python evals/compile_golden_sets.py --validate
```

---

## Compilação dos JSONLs (separadamente, antes ou depois do push)

Os 30 JSONLs em `/datasets` serão gerados a partir dos `prompts/{ID}/golden.yaml` do repositório. Eles podem ser:

- **Gerados localmente e commitados** antes do `git push v1.1.0` se quiser que a release já contenha os JSONLs
- **Gerados após push e publicados como v1.1.1** patch nos próximos dias, com calibração datada

Recomendação: rodar localmente, conferir o conteúdo, commitar como `v1.1.1` patch para separar claramente "infraestrutura" (v1.1.0) de "calibração de dados" (v1.1.1). Invariante Cinco aplicado.

```bash
# Quando os YAMLs estiverem prontos
python evals/compile_golden_sets.py
git add datasets/*.jsonl
git commit -m "v1.1.1 — 30 golden sets compilados em JSONL com calibração datada"
git tag -a v1.1.1 -m "Calibração inicial dos 30 golden sets compilados em JSONL"
git push origin main && git push origin v1.1.1
```

---

## Anti-padrão que esta release evita

Publicar JSONLs sintéticos gerados automaticamente, sem calibração humana datada, viola o Invariante Cinco (Honestidade Temporal) e o pacto editorial do APX-L. Por isso a release de **infraestrutura** (motor + script de compilação) sai independente da release de **dados** (JSONLs calibrados).

A documentação no README e no CHANGELOG é explícita sobre essa separação. O leitor que clonar o repo na manhã do dia 1 de julho encontra um motor rodável; o leitor que clonar na manhã do dia 10 encontra também os 30 JSONLs públicos com data de calibração visível.

---

## Após o push, atualizar

- `_PROJETO/RETOMAR-AQUI.md` no projeto Ebook IA: registrar v1.1.0 como publicada
- Memória `project_ebook_ia_status`: marcar compromisso público de julho como cumprido (infra) + pendente (calibração)

---

*Pacote v1.1.0 preparado em 2026-06-02. Janela natural de publicação: primeira semana de julho de 2026 conforme cadência declarada no README.*
