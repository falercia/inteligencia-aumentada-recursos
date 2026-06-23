#!/usr/bin/env python3
"""
Produção da edição DIGITAL do Livro 1 — Inteligência Aumentada · Os Invariantes da IA.

ORDEM corrigida (jun/2026): numeração contígua C01–C28 (+C14B, +C14C),
apêndices A–Q, paratextos editoriais novos. Reaproveita as capas já
renderizadas em _build/ (capa-frontal.pdf, L1-quarta-capa.pdf).

Gera PDF em chunks (escapa do timeout de 45s) + HTML navegável autocontido,
ambos da MESMA ORDEM (paridade de conteúdo garantida).

Uso:
    python3 gerar-l1.py prepare      # consolida MD por chunk + completo + CSS
    python3 gerar-l1.py chunk N      # gera PDF do chunk N
    python3 gerar-l1.py merge        # capa + chunks + quarta-capa -> PDF final
    python3 gerar-l1.py html         # HTML navegável autocontido
"""
import subprocess, os, re, sys, base64
from pathlib import Path

BASE = Path(__file__).resolve().parent
BUILD = BASE / "_build"
BUILD.mkdir(exist_ok=True)

TITULO = "Inteligência Aumentada"
SUBTITULO = "Os Invariantes da IA"
AUTOR = "Fabio Garcia"
ANO = "2026"

CAPA_PDF = BUILD / "capa-frontal.pdf"
QUARTA_PDF = BUILD / "L1-quarta-capa.pdf"

# ---------- ORDEM CANÔNICA (edição digital) ----------
ORDEM = [
    # PARATEXTO INICIAL (reader-facing; capa-e-titulos/orelhas/quarta sao jaqueta -> fora)
    ("00-paratexto/L1-00b-ficha-catalografica.md", "Ficha Catalográfica"),
    ("00-paratexto/L1-00c-dedicatoria.md", "Dedicatória"),
    ("00-paratexto/L1-00c2-promessa.md", "Por que este livro"),
    ("00-paratexto/L1-00d-agradecimentos.md", "Agradecimentos"),
    ("00-paratexto/L1-00e-sobre-os-casos.md", "Sobre os Casos"),
    ("00-paratexto/L1-01-prefacio.md", "Prefácio"),
    ("00-paratexto/L1-02-como-ler.md", "Como Ler"),
    ("00-paratexto/L1-03-introducao.md", "Introdução"),
    ("00-paratexto/L1-04-sumario.md", "Sumário"),
    ("00-paratexto/L1-05-mapa-de-leitura-por-nivel.md", "Mapa de Leitura"),
    ("00-paratexto/L1-06-repositorio-acompanhante.md", "Repositório Acompanhante"),
    # MANIFESTO
    ("01-manifesto/L1-C00M-manifesto-invariantes.md", "Manifesto"),
    ("01-manifesto/L1-C00P-porque-padrao-dura.md", "Por que o Padrão Dura"),
    # CAPÍTULOS (contíguos)
    ("02-capitulos/L1-C01-o-que-e-ia.md", "Cap 01"),
    ("02-capitulos/L1-C02-como-modelos-funcionam.md", "Cap 02"),
    ("02-capitulos/L1-C03-tokens.md", "Cap 03"),
    ("02-capitulos/L1-C04-janela-de-contexto.md", "Cap 04"),
    ("02-capitulos/L1-C05-embeddings.md", "Cap 05"),
    ("02-capitulos/L1-C06-rag.md", "Cap 06"),
    ("02-capitulos/L1-C07-memoria.md", "Cap 07"),
    ("02-capitulos/L1-C08-fine-tuning.md", "Cap 08"),
    ("02-capitulos/L1-C09-engenharia-prompt.md", "Cap 09"),
    ("02-capitulos/L1-C10-chain-of-thought.md", "Cap 10"),
    ("02-capitulos/L1-C11-context-engineering.md", "Cap 11"),
    ("02-capitulos/L1-C12-agentes.md", "Cap 12"),
    ("02-capitulos/L1-C13-mcp.md", "Cap 13"),
    ("02-capitulos/L1-C14-ai-engineering.md", "Cap 14"),
    ("02-capitulos/L1-C14B-reasoning-models.md", "Cap 14B"),
    ("02-capitulos/L1-C14C-spec-driven-development.md", "Cap 14C"),
    ("02-capitulos/L1-C15-comparacao-modelos.md", "Cap 15"),
    ("02-capitulos/L1-C16-open-source.md", "Cap 16"),
    ("02-capitulos/L1-C17-github-repos.md", "Cap 17"),
    ("02-capitulos/L1-C18-economia-tokens.md", "Cap 18"),
    ("02-capitulos/L1-C19-seguranca.md", "Cap 19"),
    ("02-capitulos/L1-C20-futuro.md", "Cap 20"),
    ("02-capitulos/L1-C21-evals.md", "Cap 21"),
    ("02-capitulos/L1-C22-llmops.md", "Cap 22"),
    ("02-capitulos/L1-C23-alignment.md", "Cap 23"),
    ("02-capitulos/L1-C24-governanca.md", "Cap 24"),
    ("02-capitulos/L1-C25-trade-offs.md", "Cap 25"),
    ("02-capitulos/L1-C26-roadmap-pessoal.md", "Cap 26"),
    ("02-capitulos/L1-C27-ia-para-pme-brasileira.md", "Cap 27"),
    ("02-capitulos/L1-C28-interpretabilidade-mecanicista.md", "Cap 28"),
    # FRAMEWORKS
    ("03-frameworks/L1-F1-decid-ia.md", "F1"),
    ("03-frameworks/L1-F2-encaixe-5.md", "F2"),
    ("03-frameworks/L1-F3-agente-prop.md", "F3"),
    ("03-frameworks/L1-F4-prompt-ext.md", "F4"),
    ("03-frameworks/L1-F5-cobertura-integracoes.md", "F5"),
    ("03-frameworks/L1-F6-gov-indelegavel.md", "F6"),
    ("03-frameworks/L1-F7-composto-3t.md", "F7"),
    ("03-frameworks/L1-F8-eval-piramide.md", "F8"),
    ("03-frameworks/L1-F9-rota-dupla.md", "F9"),
    # APÊNDICES A–Q
    ("04-apendices/L1-APX-A-glossario.md", "APX A"),
    ("04-apendices/L1-APX-B-mapa-mental.md", "APX B"),
    ("04-apendices/L1-APX-C-roadmaps.md", "APX C"),
    ("04-apendices/L1-APX-D-ferramentas.md", "APX D"),
    ("04-apendices/L1-APX-E-leituras.md", "APX E"),
    ("04-apendices/L1-APX-F-newsletters.md", "APX F"),
    ("04-apendices/L1-APX-G-papers.md", "APX G"),
    ("04-apendices/L1-APX-H-bibliografia.md", "APX H"),
    ("04-apendices/L1-APX-I-indice-remissivo.md", "APX I"),
    ("04-apendices/L1-APX-J-trilha-do-numero.md", "APX J"),
    ("04-apendices/L1-APX-K-gabaritos.md", "APX K"),
    ("04-apendices/L1-APX-L-biblioteca-prompts.md", "APX L"),
    ("04-apendices/L1-APX-M-manifesto-bolso.md", "APX M"),
    ("04-apendices/L1-APX-N-metodologico-numeros.md", "APX N"),
    ("04-apendices/L1-APX-O-caderno-governanca-v1.md", "APX O"),
    ("04-apendices/L1-APX-P-boxes-tecnicos.md", "APX P"),
    ("04-apendices/L1-APX-Q-manual-do-professor.md", "APX Q"),
    # PARATEXTO FINAL
    ("00-paratexto/L1-10-sobre-o-autor.md", "Sobre o Autor"),
]

# Chunks por índice (fim exclusivo) — cada um deve render em <40s.
# APX-L (idx 63) é gigante -> chunk próprio.
CHUNKS = [
    ("00-paratexto",        0, 13),  # 0-12  ficha..C00P
    ("01-fundamentos",     13, 21),  # 13-20 C01-C08
    ("02-prompt-agentes",  21, 29),  # 21-28 C09-C14C
    ("03-modelos-prat",    29, 37),  # 29-36 C15-C22
    ("04-gov-interp",      37, 43),  # 37-42 C23-C28
    ("05-frameworks",      43, 52),  # 43-51 F1-F9
    ("06-apx-A-I",         52, 61),  # 52-60 APX A-I
    ("07-apx-J-K",         61, 63),  # 61-62 APX J,K
    ("08-apx-L",           63, 64),  # 63    APX L (gigante)
    ("09-apx-M-Q-autor",   64, 70),  # 64-69 APX M-Q + Sobre o Autor
]

CSS_PDF = """
@page { size: 16cm 24cm; margin: 2cm 1.8cm;
  @bottom-center { content: counter(page); font-family: sans-serif; font-size: 9pt; color: #6b7280; }
  @top-left { content: string(chapter); font-family: sans-serif; font-size: 8pt; color: #9ca3af; font-style: italic; } }
@page :first { margin: 0; @bottom-center { content: none; } @top-left { content: none; } }
body { font-family: "Liberation Serif","DejaVu Serif",Georgia,serif; font-size: 11pt; line-height: 1.55; color: #0d1b2a; text-align: justify; hyphens: auto; }
.title-page { page-break-after: always; text-align: center; padding-top: 5cm; }
.title-page .tp-title { font-size: 38pt; font-weight: 700; color: #0d1b2a; letter-spacing: -1pt; }
.title-page .tp-sub { font-size: 15pt; color: #b45309; font-style: italic; margin-top: 10pt; }
.title-page .tp-series { font-size: 11pt; color: #6b7280; margin-top: 28pt; }
.title-page .tp-thesis { font-size: 13pt; color: #E97451; font-weight: 700; margin-top: 40pt; }
.title-page .tp-author { font-size: 16pt; color: #0d1b2a; margin-top: 60pt; font-weight: 600; }
.title-page .tp-year { font-size: 10pt; color: #6b7280; margin-top: 6pt; }
h1,h2,h3,h4 { font-family: "Liberation Serif","DejaVu Serif",Georgia,serif; font-weight: 700; color: #0d1b2a; string-set: chapter content(); page-break-after: avoid; }
h1 { font-size: 24pt; border-bottom: 2pt solid #E97451; padding-bottom: 8pt; page-break-before: always; letter-spacing: -0.5pt; }
h2 { font-size: 17pt; color: #1b263b; margin-top: 22pt; border-left: 3pt solid #E97451; padding-left: 10pt; }
h3 { font-size: 13pt; margin-top: 16pt; }
p { margin: 0 0 9pt 0; orphans: 3; widows: 3; }
blockquote { margin: 14pt 0; padding: 10pt 14pt; border-left: 3pt solid #E97451; background: #fefce8; font-style: italic; page-break-inside: avoid; }
ul,ol { margin: 8pt 0 12pt 0; padding-left: 22pt; } li { margin-bottom: 4pt; }
table { width: 100%; border-collapse: collapse; margin: 14pt 0; font-size: 9.5pt; }
thead { display: table-header-group; } tr { page-break-inside: avoid; }
th { background: #0d1b2a; color: #fef3c7; padding: 6pt 8pt; text-align: left; font-family: sans-serif; font-weight: 700; font-size: 8.5pt; }
td { padding: 5pt 8pt; border-bottom: 0.5pt solid #d1d5db; vertical-align: top; }
tr:nth-child(even) td { background: #fafafa; }
code { font-family: "DejaVu Sans Mono",monospace; font-size: 9.5pt; background: #f3f4f6; padding: 1pt 4pt; }
pre { background: #0d1b2a; color: #fef3c7; padding: 12pt; font-size: 8.5pt; line-height: 1.45; white-space: pre-wrap; word-wrap: break-word; margin: 12pt 0; }
pre code { background: transparent; color: #fef3c7; padding: 0; }
img { max-width: 100%; height: auto; display: block; margin: 14pt auto; page-break-inside: avoid; }
a { color: #D97706; text-decoration: none; }
.page-break { page-break-after: always; }
strong { color: #0d1b2a; font-weight: 700; }
hr { border: none; border-top: 1pt solid #E97451; margin: 18pt auto; width: 60%; opacity: 0.6; }
"""

CSS_HTML = """
:root { --ink:#0d1b2a; --accent:#E97451; --cream:#fefce8; }
* { box-sizing: border-box; }
body { font-family: Georgia,"Times New Roman",serif; max-width: 860px; margin: 0 auto; padding: 40px 28px 120px; line-height: 1.7; color: var(--ink); background: #fff; }
.title-page { text-align: center; padding: 30px 0 50px; border-bottom: 2px solid #eee; margin-bottom: 30px; }
.title-page .tp-title { font-size: 3em; font-weight: 700; letter-spacing: -1px; }
.title-page .tp-sub { font-size: 1.2em; font-style: italic; color: #b45309; margin-top: 8px; }
.title-page .tp-series { color: #6b7280; margin-top: 18px; }
.title-page .tp-thesis { color: var(--accent); font-weight: 700; margin-top: 24px; font-size: 1.1em; }
.title-page .tp-author { font-size: 1.3em; font-weight: 600; margin-top: 40px; }
.title-page .tp-year { color: #6b7280; }
h1 { font-size: 1.9em; border-bottom: 3px solid var(--accent); padding-bottom: .25em; margin-top: 2.4em; }
h2 { font-size: 1.4em; color: #1b263b; border-left: 4px solid var(--accent); padding-left: 12px; margin-top: 1.6em; }
h3 { font-size: 1.15em; color: #1b263b; }
blockquote { border-left: 4px solid var(--accent); background: var(--cream); padding: .7em 1.1em; margin: 1.3em 0; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.3em 0; font-size: .93em; }
th,td { border: 1px solid #ddd; padding: 8px 11px; text-align: left; vertical-align: top; }
th { background: var(--ink); color: var(--cream); }
tr:nth-child(even) td { background: #fafafa; }
code { background: #f4f4f4; padding: 1px 5px; border-radius: 3px; font-size: .9em; font-family: Consolas,monospace; }
pre { background: var(--ink); color: var(--cream); padding: 16px; border-radius: 6px; overflow-x: auto; font-size: .85em; line-height: 1.5; }
pre code { background: transparent; color: var(--cream); }
img { max-width: 100%; height: auto; display: block; margin: 1.4em auto; }
a { color: #1a5276; text-decoration: none; } hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
#TOC { background: #faf9f6; border: 1px solid #e0ddd0; padding: 1.2em 1.6em; border-radius: 8px; margin: 1.5em 0; }
#TOC a { color: var(--ink); }
"""


def resolver_img(conteudo, origem, modo):
    d = origem.parent
    def sub(m):
        alt, link = m.group(1), m.group(2)
        if link.startswith(("http://", "https://", "data:")):
            return m.group(0)
        ap = (d / link).resolve()
        if not ap.exists():
            return m.group(0)
        if modo == "file":
            return f"![{alt}](file://{ap})"
        raw = ap.read_bytes(); ext = ap.suffix.lower()
        mime = {".svg":"image/svg+xml",".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg"}.get(ext,"application/octet-stream")
        return f"![{alt}](data:{mime};base64,{base64.b64encode(raw).decode('ascii')})"
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", sub, conteudo)


def folha():
    return ('<div class="title-page">'
            f'<div class="tp-title">{TITULO}</div>'
            f'<div class="tp-sub">{SUBTITULO}</div>'
            f'<div class="tp-series">Volume 1 da série <em>Inteligência Aumentada</em></div>'
            f'<div class="tp-thesis">Modelos passam. Método fica.</div>'
            f'<div class="tp-author">{AUTOR}</div>'
            f'<div class="tp-year">{ANO} · Edição digital</div></div>')


def consolidar(ini, fim, modo, com_folha):
    out = ["---", "lang: pt-BR", "---", ""]
    if com_folha:
        out.append(folha())
    for i in range(ini, fim):
        rel, nome = ORDEM[i]
        p = BASE / rel
        if not p.exists():
            print(f"  ✗ FALTA: {rel}", file=sys.stderr); continue
        out.append('\n\n<div class="page-break"></div>\n\n')
        out.append(resolver_img(p.read_text(encoding="utf-8"), p, modo))
    return "\n".join(out)


def cmd_prepare():
    (BUILD / "l1-style.css").write_text(CSS_PDF, encoding="utf-8")
    falta = [r for r, _ in ORDEM if not (BASE / r).exists()]
    if falta:
        print(f"✗ {len(falta)} arquivos faltam:"); [print("   ", f) for f in falta]; sys.exit(1)
    print(f"✓ Todos os {len(ORDEM)} arquivos existem")
    for idx, (nome, ini, fim) in enumerate(CHUNKS):
        md = consolidar(ini, fim, "file", com_folha=(idx == 0))
        (BUILD / f"l1-chunk-{idx:02d}.md").write_text(md, encoding="utf-8")
        print(f"  ✓ chunk {idx:02d} ({nome}): {fim-ini} itens, {len(md)//1024} KB")


def cmd_chunk(idx):
    md = BUILD / f"l1-chunk-{idx:02d}.md"
    html = BUILD / f"l1-chunk-{idx:02d}.html"
    pdf = BUILD / f"l1-chunk-{idx:02d}.pdf"
    subprocess.run(["pandoc", str(md), "-f",
        "markdown+raw_html+definition_lists+fenced_code_blocks+pipe_tables",
        "-t", "html5", "--standalone", "-o", str(html), "--metadata=lang:pt-BR"], check=True)
    import weasyprint
    weasyprint.HTML(filename=str(html), base_url=str(BASE)).write_pdf(
        str(pdf), stylesheets=[weasyprint.CSS(filename=str(BUILD/"l1-style.css"))])
    print(f"✓ chunk {idx:02d}: {pdf.stat().st_size//1024} KB")


def cmd_merge():
    from pypdf import PdfWriter
    final = BASE / "Inteligencia-Aumentada-EDICAO-DIGITAL.pdf"
    w = PdfWriter()
    if CAPA_PDF.exists():
        w.append(str(CAPA_PDF)); print("  + capa-frontal")
    for idx in range(len(CHUNKS)):
        c = BUILD / f"l1-chunk-{idx:02d}.pdf"
        if c.exists():
            w.append(str(c)); print(f"  + chunk {idx:02d}")
        else:
            print(f"  ✗ FALTA chunk {idx:02d}")
    if QUARTA_PDF.exists():
        w.append(str(QUARTA_PDF)); print("  + quarta-capa")
    w.write(str(final)); w.close()
    print(f"\n✓ PDF final: {final.name} ({final.stat().st_size/1048576:.2f} MB)")


def cmd_html():
    md = consolidar(0, len(ORDEM), "data", com_folha=True)
    tmp = BUILD / "l1-html-src.md"; tmp.write_text(md, encoding="utf-8")
    out = BASE / "Inteligencia-Aumentada-EDICAO-DIGITAL.html"
    subprocess.run(["pandoc", str(tmp), "-f",
        "markdown+raw_html+definition_lists+fenced_code_blocks+pipe_tables",
        "-t", "html5", "--standalone", "--toc", "--toc-depth=1", "-o", str(out),
        "--metadata=lang:pt-BR"], check=True)
    h = out.read_text(encoding="utf-8")
    h = h.replace("</head>", f"<title>{TITULO} · {SUBTITULO}</title><style>{CSS_HTML}</style></head>")
    out.write_text(h, encoding="utf-8")
    print(f"✓ HTML: {out.name} ({out.stat().st_size/1048576:.2f} MB)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prepare": cmd_prepare()
    elif cmd == "chunk": cmd_chunk(int(sys.argv[2]))
    elif cmd == "merge": cmd_merge()
    elif cmd == "html": cmd_html()
    else: print(__doc__)
