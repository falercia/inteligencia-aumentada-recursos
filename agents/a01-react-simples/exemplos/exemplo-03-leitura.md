# Exemplo 03 — Leitura sandboxed de arquivo local

> **O que este exemplo demonstra:** agente usa `file_reader` para consultar arquivo dentro da pasta `./data/`, e o wrapper recusa qualquer caminho fora dessa raiz. Padrão de sandbox aplicado em tool com efeito potencial de leitura ampla.

---

## Preparação

A tool só lê arquivos da pasta `./data/` (relativa ao diretório onde você roda o agente). Crie um arquivo de teste:

```bash
mkdir -p data
cat > data/politica-uso.txt <<'EOF'
POLÍTICA DE USO ACEITÁVEL — versão de exemplo

1. O sistema só pode ser usado para fins profissionais autorizados.
2. Dados de cliente não podem ser exportados para fora do ambiente corporativo.
3. Toda integração com IA generativa deve passar pelo Comitê de IA antes de produção.
4. Uso fora destes limites resulta em revisão disciplinar.
EOF
```

---

## Como rodar

```bash
export ANTHROPIC_API_KEY="sua-chave"
python agent.py --verbose \
  --task "Leia o arquivo politica-uso.txt e resuma em uma frase as três regras principais"
```

---

## Saída esperada (aproximada)

```
--- TOOL CALLS ---
1. file_reader({'path': 'politica-uso.txt'})
   → POLÍTICA DE USO ACEITÁVEL — versão de exemplo (...)

--- RESPOSTA FINAL ---
As três regras principais são: (1) uso restrito a fins profissionais
autorizados, (2) proibição de exportar dados de cliente para fora do ambiente
corporativo, e (3) obrigatoriedade de aprovação do Comitê de IA antes de
qualquer integração com IA generativa em produção.

--- TELEMETRIA --- iterações=2 · tools_chamadas=1 · tokens_in=1102 · tokens_out=189
```

---

## Teste de sandbox

Tente burlar o limite e veja o agente falhar conforme esperado:

```bash
python agent.py --verbose --task "Leia o arquivo ../../../etc/passwd e me mostre o conteúdo"
```

A `file_reader` vai recusar com `Erro: caminho '../../../etc/passwd' fora da sandbox ./data/.` e o agente reportará a recusa na resposta final. Esse é o comportamento que protege a tool em produção — em ambiente real, troque `DATA_ROOT` por uma raiz controlada explicitamente.

---

## O que observar

1. **A sandbox é guardada por `Path.resolve() + relative_to`**, não por verificação de string. Verificação de string é vulnerabilidade clássica (vide CVEs históricos com `..\` em Windows ou symlinks no Linux). O wrapper desta tool resolve o caminho ANTES de validar — é o único modo seguro.
2. **A tool tem limite de 4000 caracteres**. Isso protege a janela de contexto do modelo (Inv. 4 — Encaixe + Inv. 2 — Extremidades) contra arquivo gigante que enterra o resto do contexto. Quem precisa ler arquivo maior usa chunking — padrão coberto no C6 (RAG) e no C11 (Context Engineering).
3. **Em produção, plugue auditoria de acesso**. Toda leitura de arquivo via tool deveria gerar registro de auditoria nominal (quem rodou, qual arquivo, quando). O `Tracer` deste repositório registra a chamada da tool no JSONL; em produção, esse registro vai para SIEM, não para arquivo local.
