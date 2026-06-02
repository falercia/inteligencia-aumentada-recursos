# P-RH-02 · Análise de feedback 360

**Domínio:** Recursos Humanos
**Caso de uso:** Síntese de feedback 360 graus em temas, com preservação de anonimato e equilíbrio de tom
**Modelo recomendado:** Sonnet equivalente

---

## Estrutura

```
P-RH-02-feedback-360/
├── README.md          ← este arquivo
├── prompt.xml         ← XML completo (persona, constituição,
│                       contexto, tarefa, formato, prefill,
│                       self_critique, input)
├── golden-set.yaml    ← 20 casos categorizados
├── anti-padroes.md    ← antipadrões + métrica
├── changelog.md       ← histórico de versões
└── exemplos-saida/    ← outputs reais anonimizados
```

## Como usar

1. Copie esta pasta inteira para o seu repositório.
2. Adapte a constituição em `prompt.xml` ao seu contexto.
3. Construa seu golden set próprio com pelo menos 20 casos do
   seu tráfego real, usando `golden-set.yaml` como template.
4. Rode `eval_runner.py` (release v1.1.0+) antes de cada release.

## Conexão com a obra

A ficha conceitual completa, com analogia, anti-padrões
detalhados e exemplos de aplicação, está no **APX-L · Biblioteca
de Prompts Profissionais** do livro Inteligência Aumentada · Os
Invariantes da IA.

## Licença

- `prompt.xml`, `golden-set.yaml`, `anti-padroes.md`,
  `changelog.md`: CC-BY 4.0
- Atribuição obrigatória a Fabio Garcia / Inteligência Aumentada.
