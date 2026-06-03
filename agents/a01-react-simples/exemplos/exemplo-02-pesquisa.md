# Exemplo 02 — Pesquisa com encaminhamento a fonte primária

> **O que este exemplo demonstra:** agente usa `fake_web_search` para responder pergunta factual, e o `system_prompt.md` força o agente a declarar que a fonte é simulada e sugerir verificação na fonte primária. Padrão honesto de uso de tool de pesquisa em ambiente educacional.

---

## Como rodar

```bash
# Modo real
export ANTHROPIC_API_KEY="sua-chave"
python agent.py --verbose \
  --task "Pesquise como funciona a LGPD e me explique em três frases"
```

---

## Saída esperada (modo real, aproximada)

```
[A01] tracing em ./traces/trace-20260801-104102-12345.jsonl
[A01] tarefa: Pesquise como funciona a LGPD e me explique em três frases

--- TOOL CALLS ---
1. fake_web_search({'query': 'LGPD'})
   → 1. ANPD — Lei Geral de Proteção de Dados
        A LGPD (Lei 13.709/2018) regula o tratamento de dados pessoais...

--- RESPOSTA FINAL ---
A LGPD (Lei 13.709/2018) regula o tratamento de dados pessoais no Brasil,
estabelecendo direitos do titular e deveres do controlador e operador. A
fiscalização é feita pela ANPD (Autoridade Nacional de Proteção de Dados),
com sanções que podem chegar a 2% do faturamento. **Atenção: este resultado
veio da tool simulada de pesquisa deste exemplo educacional. Para informação
operacional vigente, consulte gov.br/anpd.**

--- TELEMETRIA --- iterações=2 · tools_chamadas=1 · tokens_in=1247 · tokens_out=312
```

---

## O que observar

1. **O agente cumpre a diretriz do system prompt**: declara que a fonte é simulada e sugere a fonte primária. Isso não vem de "boa vontade do modelo" — vem de instrução explícita no `system_prompt.md`. Sem a instrução, o modelo apresentaria o resultado canned como se fosse verdade verificada.
2. **A tool é determinística**. Rode duas vezes e o resultado da `fake_web_search` será idêntico. Isso é deliberado e educacional: permite que professores reproduzam o exemplo em sala, e que a CI valide a saída sem instabilidade externa.
3. **Em produção, trocar a tool sem trocar o agente**. O schema `WEB_SEARCH_TOOL` é o mesmo formato esperado por buscadores reais (Brave, Tavily, Exa). Basta trocar `execute_web_search` por uma chamada real ao buscador, mantendo a interface, e o agente continua funcionando. É a aplicação da Camada Dupla no nível de stack.

---

## Limites declarados

Esta tool **não pesquisa de verdade**. As consultas sem keyword reconhecida (`selic`, `lgpd`, `claude`) retornam um resultado padrão informando isso. Em produção real, a recomendação é integrar com uma das APIs de busca mencionadas no Apêndice J do livro (seção *Buscadores*).
