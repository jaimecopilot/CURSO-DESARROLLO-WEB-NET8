#!/usr/bin/env python3
"""Convertir Markdown canónico de M01 a PDF con diagramas vectoriales y comprobar integridad."""
from __future__ import annotations

from collections import Counter
from html import escape
from pathlib import Path
from textwrap import wrap
import json
import hashlib
from io import BytesIO
import re
import subprocess
import sys
import unicodedata

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from weasyprint import HTML, CSS
from pypdf import PdfReader, PdfWriter
import fitz

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"M01_MVC"
OUTPUT=ROOT/"VERIFICACION_INTERNA"/"M01_PDFS_VALIDACION.md"
HTML_FORMATTER=HtmlFormatter(cssclass="highlight")

def dotquote(x: str) -> str:
    return '"' + x.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n") + '"'

def parse_node(part: str):
    part=part.strip().rstrip(";")
    m=re.match(r"^([A-Za-z_][A-Za-z_0-9]*)",part)
    if not m: raise ValueError(f"Nodo Mermaid no reconocido: {part}")
    identity=m.group(1)
    label=re.search(r'\["(.*?)"\]',part)
    if label: return identity,label.group(1),"box"
    label=re.search(r'\{(.*?)\}',part)
    if label: return identity,label.group(1).strip('"'),"diamond"
    return identity,identity,"box"

def flowchart_svg(src: str) -> str:
    nodes={}
    edges=[]
    for line in src.splitlines():
        line=line.strip()
        if not line or line.startswith("%%") or line.startswith("flowchart"): continue
        if "-->" not in line: continue
        left,right=line.split("-->",1)
        label=""
        right=right.strip()
        if right.startswith("|"):
            end=right.find("|",1)
            if end>0:
                label=right[1:end]
                right=right[end+1:].strip()
        a,aa,shapea=parse_node(left)
        b,bb,shapeb=parse_node(right)
        for identity,name,shape in [(a,aa,shapea),(b,bb,shapeb)]:
            if identity not in nodes or name!=identity:
                nodes[identity]=(name,shape)
        edges.append((a,b,label))
    if not edges: raise ValueError("Diagrama de flujo Mermaid sin relaciones")
    dot=['digraph G {','graph [rankdir=TB,bgcolor="transparent",pad=0.25,ranksep=0.42,nodesep=0.28,concentrate=false];',
         'node [fontname="DejaVu Sans",fontsize=12,style="rounded,filled",color="#527387",fillcolor="#F2F7F9",fontcolor="#17334B",penwidth=1.1];',
         'edge [fontname="DejaVu Sans",fontsize=10,color="#527387",arrowsize=0.70];']
    for key,(label,shape) in nodes.items():
        text="\n".join(wrap(label,width=34,break_long_words=False,break_on_hyphens=False))
        dot.append(f'{key} [label={dotquote(text)},shape={shape}];')
    for a,b,label in edges:
        arrow=f'{a} -> {b}'
        if label: arrow+=f' [label={dotquote(label)}]'
        dot.append(arrow+";")
    dot.append("}")
    p=subprocess.run(["dot","-Tsvg"],input="\n".join(dot),encoding="utf-8",
                     capture_output=True,check=False)
    if p.returncode: raise RuntimeError("Graphviz no pudo representar Mermaid:\n"+p.stderr)
    svg=p.stdout[p.stdout.find("<svg"):]
    if not svg.startswith("<svg"): raise RuntimeError("SVG inválido devuelto por Graphviz")
    return svg

def sequence_svg(src: str) -> str:
    participants=[]
    actions=[]
    for line in src.splitlines():
        line=line.strip()
        m=re.match(r"participant\s+([A-Za-z_]\w*)\s+as\s+(.+)",line)
        if m:
            participants.append((m.group(1),m.group(2)))
            continue
        m=re.match(r"([A-Za-z_]\w*)\s*(?:-->>|->>|-->|->)\s*([A-Za-z_]\w*)\s*:\s*(.+)",line)
        if m:
            actions.append(("arrow",m.group(1),m.group(2),m.group(3)))
            continue
        m=re.match(r"Note over ([A-Za-z_]\w*):\s*(.+)",line,re.I)
        if m: actions.append(("note",m.group(1),m.group(1),m.group(2)))
    if not participants or not actions: raise ValueError("Secuencia Mermaid sin participantes o mensajes")
    ix={name:i for i,(name,_) in enumerate(participants)}
    margin=75
    step=190
    width=margin*2+max(1,len(participants)-1)*step
    h=118+len(actions)*82
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}" height="{h}">',
         '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#547486" stroke-width="1.1"/></marker></defs>',
         '<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>']
    for i,(_,title) in enumerate(participants):
        x=margin+i*step
        out.append(f'<rect x="{x-70}" y="12" width="140" height="46" rx="7" fill="#ECF4F7" stroke="#547486"/>')
        label=escape(title)
        if len(label)>22:
            first,second=(label[:22],label[22:])
            out.append(f'<text x="{x}" y="31" text-anchor="middle" font-family="DejaVu Sans" font-size="10" fill="#133248">{first}</text>')
            out.append(f'<text x="{x}" y="46" text-anchor="middle" font-family="DejaVu Sans" font-size="10" fill="#133248">{second}</text>')
        else:
            out.append(f'<text x="{x}" y="40" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#133248">{label}</text>')
        out.append(f'<line x1="{x}" y1="58" x2="{x}" y2="{h-14}" stroke="#B8C9D2" stroke-width="1.4" stroke-dasharray="5 5"/>')
    for n,(kind,a,b,label) in enumerate(actions):
        y=115+n*82
        if a not in ix: continue
        x1=margin+ix[a]*step
        wrapped=wrap(label, width=32,break_long_words=False,break_on_hyphens=False)[:3] or [""]
        if kind=="note":
            x=max(8,x1-83)
            out.append(f'<rect x="{x}" y="{y-35}" width="175" height="58" rx="4" fill="#fff6db" stroke="#B1954F"/>')
            for k,v in enumerate(wrapped): out.append(f'<text x="{x+8}" y="{y-17+15*k}" font-family="DejaVu Sans" font-size="10">{escape(v)}</text>')
        elif b in ix:
            x2=margin+ix[b]*step
            out.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#547486" stroke-width="1.8" marker-end="url(#arrow)"/>')
            x=(x1+x2)/2
            for k,v in enumerate(wrapped):
                out.append(f'<text x="{x}" y="{y-33+14*k}" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#17334B">{escape(v)}</text>')
    out.append("</svg>")
    return "".join(out)

DIAGRAM_COUNT=0

def strip_fenced_code(source: str) -> str:
    """El código completo de los README puede contener etiquetas de autor propias.

    No son metadatos de portada: se reconocen solo las declaraciones
    fuera de los bloques de código del manual.
    """
    return re.sub(r"^~~~[^\n]*\n.*?^~~~[ \t]*$", "", source, flags=re.M | re.S)


def metadata_from_markdown(source: str, field: str) -> str:
    """Devuelve una única declaración canónica de portada para curso, tipo o autor."""
    source = strip_fenced_code(source)
    hits=re.findall(r"(?m)^\*\*"+re.escape(field)+r":\s*([^\r\n*]+)\*\*\s*$", source)
    if len(hits)!=1:
        raise ValueError(f"Se requiere exactamente un metadato **{field}: ...** en el Markdown")
    return hits[0].strip()

def author_from_markdown(source: str) -> str:
    """Obtener el texto del autor solo del documento Markdown."""
    labels=re.findall(r"(?m)^\*\*(AUTOR:[ \t]*[^\r\n*]+)\*\*[ \t]*$",strip_fenced_code(source))
    if len(labels)!=1:
        raise ValueError("El Markdown debe contener exactamente una línea **AUTOR: ...**")
    return labels[0].strip()

def fence_render(tokens, idx, options, env):
    global DIAGRAM_COUNT
    tok=tokens[idx]
    lang=(tok.info.strip().split(" ") or [""])[0].lower()
    content=tok.content
    if lang=="mermaid":
        try:
            if content.lstrip().startswith("flowchart"):
                svg=flowchart_svg(content)
                figure_type="flow"
            elif content.lstrip().startswith("sequenceDiagram"):
                svg=sequence_svg(content)
                figure_type="sequence"
            else:
                raise ValueError("Tipo Mermaid aún no soportado")
            DIAGRAM_COUNT+=1
            return '<figure class="diagram diagram-'+figure_type+'">'+svg+'</figure>'
        except Exception as e:
            raise RuntimeError(f"Error al representar diagrama Mermaid {DIAGRAM_COUNT+1}: {e}")
    aliases={"cshtml":"html+razor", "http":"http", "text":"text","xml":"xml","bash":"bash","csharp":"csharp"}
    name=aliases.get(lang,lang)
    try: lexer=get_lexer_by_name(name)
    except Exception: lexer=TextLexer()
    highlighted=highlight(content,lexer,HTML_FORMATTER)
    return f'<div class="code-block">{highlighted}</div>'

CSS_TEMPLATE=r"""
@page {
  size: A4;
  margin: 23mm 16mm 19mm 16mm;
  @top-left {
    content: "__MD_COURSE__" "\A" string(current_chapter, first);
    white-space: pre-wrap;
    width: 117mm;
    text-align: left;
    font: 7.1pt "DejaVu Sans";
    color: #42586a;
  }
  @top-right {
    content: "__MD_TYPE__" "\A" "__MD_AUTHOR__";
    white-space: pre-wrap;
    width: 51mm;
    text-align: right;
    font: 7.8pt "DejaVu Sans";
    color: #42586a;
  }
  @bottom-right { content: "Página " counter(page); font: 8pt "DejaVu Sans"; color: #64748B; }
}
/* En portada no aparece cabecera ni numeración. */
@page:first {
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-right { content: none; }
}
html { font-family: "DejaVu Sans", sans-serif; }
body { font-size: 9.8pt; line-height: 1.46; color: #1e293b; }
.cover { height: 235mm; box-sizing: border-box; padding-top: 60mm; break-after: page; }
.cover h1.doc-title { font-size: 27pt; line-height: 1.25; margin-bottom: 10mm; }
.cover h2 { font-size: 16pt; margin: 0; color: #52687a; }
.cover p { margin-top: 8mm; font-size: 12pt; letter-spacing: .15pt; }
.cover p:first-of-type { margin-top: 25mm; }
.cover strong { color: #12324b; }
h1,h2,h3,h4 { font-weight: 700; line-height: 1.2; break-after: avoid; color: #12324b; }
h1 { font-size: 20pt; margin: 0 0 10pt; }
h1.doc-title { font-size: 22pt; padding: 12pt 0 16pt; border-bottom: 2pt solid #2c647b; }
h1.chapter { font-size: 19pt; margin: 0 0 18pt; break-before: page; border-bottom: 1pt solid #93acb7; padding-bottom: 7pt; string-set: current_chapter content(text); }
h3.toc-heading { string-set: current_chapter content(text); }
h2 { font-size: 13.5pt; margin-top: 17pt; }
h3 { font-size: 11.5pt; margin-top: 14pt; }
h4 { font-size: 10pt; margin-top: 11pt; }
p { margin: 6pt 0 8pt; orphans: 2; widows: 2; }
strong { color: #102b44; }
a { color: #115d8d; text-decoration: underline; }
ul,ol { padding-left: 16pt; margin: 7pt 0 10pt; }
li { margin: 3pt 0; }
hr { margin: 13pt 0; border: 0; border-top: 1px solid #dae4e8; }
blockquote { border-left: 2.5pt solid #9eb6c5; padding: 4pt 11pt; background: #f7fafb; }
table { width: 100%; border-collapse: collapse; font-size: 8pt; margin: 10pt 0 12pt; table-layout: auto; }
thead { display: table-header-group; }
th { background: #edf3f6; color: #13374c; border: 0.5pt solid #bbcbd4; padding: 5pt 6pt; text-align: left; }
td { border: 0.5pt solid #c8d4da; padding: 5pt 6pt; vertical-align: top; overflow-wrap: anywhere; }
tr { break-inside: avoid; }
p code, li code, td code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.4pt; background: #eef4f7; padding: .3pt 2pt; overflow-wrap: anywhere; }
.code-block { margin: 9pt 0; break-inside: auto; border-left: 2pt solid #85aaba; background: #f5f8fa; padding: 8pt 9pt; }
.highlight { background: transparent; }
.highlight pre,pre { font-family: "DejaVu Sans Mono", monospace; font-size: 8.2pt; line-height: 1.35; white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; margin: 0; }
.code-block .highlight pre { white-space: pre-wrap; overflow-wrap: anywhere; }
.diagram { display: block; text-align: center; margin: 10pt 0 13pt; break-inside: avoid; }
.diagram svg { display: block; width: auto; height: auto; margin: 0 auto; }
.diagram-flow svg { max-width: 155mm; max-height: 130mm; }
.diagram-sequence svg { max-width: 168mm; max-height: 94mm; }
.diagram svg { max-width: 100%; }
.toc { margin: 14pt 0 20pt; border: 0.8pt solid #cbdbe2; padding: 13pt 17pt; background: #f6f9fb; }
.toc h2 { margin-top: 0; font-size: 13pt; }
.toc p { font-size: 10pt; margin: 8pt 0; }
.subtitle { font-weight: 500; font-size: 11pt; color: #577083; }
.chapter-meta { color: #5e7c90; }
"""
def document_html(markdown: str, title: str, kind: str) -> str:
    author=author_from_markdown(markdown)
    course=metadata_from_markdown(markdown,"CURSO")
    kind_label=metadata_from_markdown(markdown,"TIPO")
    if kind_label!=("TEORÍA" if kind=="TEORIA" else "PRÁCTICAS"):
        raise ValueError(f"TIPO de documento distinto a su carpeta: {kind_label}")
    # El auditor de fidelidad compara el rótulo visible, no los tokens de la URL
    # almacenada como hipervínculo y conservada en el MD canónico adjunto.
    # Las referencias bibliográficas se mantienen literales y se convierten
    # a hipervínculos PDF; no se modifican ni resumen las fuentes Markdown.
    markdown_html = re.sub(r"(?m)^(-\s+[^\n]*?:\s*)(https?://[^\s<>]+)", lambda m: m.group(1) + "[Consultar fuente](" + m.group(2) + ")", markdown)
    md=MarkdownIt("commonmark",{"html":True}).enable("table").enable("strikethrough")

    md.renderer.rules["fence"]=fence_render
    body=md.render(markdown_html)
    toc=[]
    first=[True]
    def heading(m):
        val=m.group(1)
        ident=re.search(r"(?:P?1)\.([1-5])\.",re.sub("<[^>]*>","",val))
        if ident:
            anchor=f"punto-{ident.group(1)}"
            toc.append((anchor, re.sub("<[^>]*>","",val)))
            return f'<h1 id="{anchor}" class="chapter">{val}</h1>'
        if first[0]:
            first[0]=False
            return f'<h1 class="doc-title">{val}</h1>'
        return f"<h1>{val}</h1>"
    body=re.sub(r"<h1>(.*?)</h1>",heading,body,flags=re.S)
    if len(toc)!=5: raise ValueError(f"Índice de {title}: se esperaban 5 capítulos, hallados {toc}")
    # Maquetar solo metadatos ya presentes en el MD como portada.
    cover_re=(r'(<h1 class="doc-title">.*?</h1>\s*<h2>.*?</h2>\s*'
              r'<p><strong>CURSO:\s*'+re.escape(escape(course))+r'</strong></p>\s*'
              r'<p><strong>TIPO:\s*'+re.escape(escape(kind_label))+r'</strong></p>\s*'
              r'<p><strong>'+re.escape(escape(author))+r'</strong></p>)')
    body,cover_count=re.subn(cover_re,r'<section class="cover">\1</section>',
                            body,count=1,flags=re.S)
    if cover_count!=1:
        raise ValueError("No se reconoció la portada canónica con autor")
    # El índice procede exclusivamente del Markdown; su título sirve de cabecera
    # hasta la primera página del capítulo 1.1.
    body=body.replace("<h3>Índice del módulo</h3>",
                      '<h3 class="toc-heading">Índice del módulo</h3>',1)
    def css_quote(value: str) -> str:
        return value.replace("\\","\\\\").replace('"','\\"').replace("\n"," ")
    css=(CSS_TEMPLATE
         .replace("__MD_COURSE__",css_quote(course))
         .replace("__MD_TYPE__",css_quote(kind_label))
         .replace("__MD_AUTHOR__",css_quote(author)))
    css+=HTML_FORMATTER.get_style_defs(".highlight")
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{escape(title)}</title>
    <style>{css}</style></head><body>{body}</body></html>"""

def normalize(text: str):
    return " ".join(unicodedata.normalize("NFKC",text).lower().split())

def generate(kind: str):
    global DIAGRAM_COUNT
    DIAGRAM_COUNT=0
    file=BASE/kind/f"M01_{kind}.md"
    output=BASE/kind/f"M01_{kind}.pdf"
    markdown=file.read_text(encoding="utf-8")
    title="M01 — Teoría de ASP.NET Core MVC" if kind=="TEORIA" else "M01 — Prácticas de ASP.NET Core MVC"
    html=document_html(markdown,title,kind)
    HTML(string=html,base_url=str(BASE)).write_pdf(str(output))
    # El PDF contiene también la fuente canónica MD, byte por byte.
    # Esta copia incrustada NO sustituye la comprobación del texto visual.
    raw_bytes=file.read_bytes()
    digest=hashlib.sha256(raw_bytes).hexdigest()
    writer=PdfWriter()
    writer.append(BytesIO(output.read_bytes()))
    writer.add_metadata({"/Title": title, "/Author": author_from_markdown(markdown), "/Subject": "Curso de Desarrollo Web ASP.NET Core MVC .NET 8"})
    writer.add_attachment(filename=file.name,data=raw_bytes)
    buffer=BytesIO()
    writer.write(buffer)
    output.write_bytes(buffer.getvalue())
    check_pdf(output,markdown,DIAGRAM_COUNT,source_bytes=raw_bytes,filename=file.name)
    pdf=PdfReader(str(output))
    return {"tipo":kind,"markdown":file.relative_to(ROOT).as_posix(),"pdf":output.relative_to(ROOT).as_posix(),
            "palabras_markdown":len(markdown.split()),"caracteres_markdown":len(markdown),
            "paginas_pdf":len(pdf.pages),"diagramas_renderizados":DIAGRAM_COUNT,
            "bytes_pdf":output.stat().st_size,"md_sha256":digest,"fuente_incrustada_igual":True}

def check_pdf(file: Path, md: str, diagram_count: int, source_bytes: bytes, filename: str):
    reader=PdfReader(str(file))
    embedded=reader.attachments.get(filename)
    if embedded is None:
        raise AssertionError(f"{file.name}: no está incrustada la fuente MD")
    if isinstance(embedded,list):
        if len(embedded)!=1: raise AssertionError(f"{file.name}: varias versiones MD incrustadas")
        embedded=embedded[0]
    if embedded != source_bytes:
        raise AssertionError(f"{file.name}: el MD incrustado difiere byte por byte de la fuente")
    if hashlib.sha256(embedded).digest()!=hashlib.sha256(source_bytes).digest():
        raise AssertionError(f"{file.name}: huella MD no válida")
    if reader.metadata is None or reader.metadata.author != author_from_markdown(md):
        raise AssertionError(f"{file.name}: falta autor correcto en metadatos PDF")
    if not reader.metadata.title:
        raise AssertionError(f"{file.name}: falta título en metadatos PDF")
    if not 7<=len(reader.pages)<=300: raise AssertionError(f"{file.name}: número de páginas incompatible con portada, índice y cinco capítulos: {len(reader.pages)}")
    pdftext="\n".join(p.extract_text() or "" for p in reader.pages)
    low=normalize(pdftext)
    prefix="P" if "PRACTICAS" in file.as_posix() else ""
    for n in range(1,6):
        chapter=f"{prefix}1.{n}."
        if chapter.lower() not in low: raise AssertionError(f"{file.name}: capítulo {chapter} ausente")
        if prefix and f"reto 1.{n}" not in low: raise AssertionError(f"{file.name}: el reto 1.{n} no aparece")
    for term in ["Cuaderno","Lápiz","Carpeta","Producto","Razor","Model","1.5"]:
        if normalize(term) not in low: raise AssertionError(f"{file.name}: falta contenido {term}")
    words=re.findall(r"\w+",pdftext.lower(),re.UNICODE)
    source_without_urls=re.sub(r"https?://\S+","",md)
    source_without_mermaid=re.sub(r"^~~~mermaid.*?^~~~\s*$","",source_without_urls,flags=re.M|re.S)
    md_words=re.findall(r"\w+",source_without_mermaid.lower(),re.UNICODE)
    fraction=min(1.0,len(words)/max(1,len(md_words)))
    if fraction<0.58: raise AssertionError(f"{file.name}: PDF demasiado corto frente al Markdown ({fraction:.2%})")
    if diagram_count != len(re.findall(r"^~~~mermaid\b",md,re.M)):
        raise AssertionError(f"{file.name}: no se convirtieron todos los diagramas a SVG")
    doc=fitz.open(str(file))
    author=author_from_markdown(md)
    course=metadata_from_markdown(md,"CURSO")
    kind_label=metadata_from_markdown(md,"TIPO")
    chapter_titles=[re.sub(r"^(?:P)?1\.[1-5]\.\s*", "", m.group(0))
       for m in re.finditer(r"(?m)^# (?:P)?1\.[1-5]\.\s+[^\r\n]+",md)]
    if len(chapter_titles)!=5:
        raise AssertionError(f"{file.name}: se esperan cinco títulos de capítulo en Markdown")
    current_chapter="Índice del módulo"
    # El cuerpo empieza después del margen superior de 23 mm definido en @page.
    # Una transcripción puede comenzar justo al principio del cuerpo y contener
    # literalmente "AUTOR: ..."; por eso la cabecera se identifica por quedar
    # completamente dentro del margen, no por un umbral y0 que invada el cuerpo.
    header_bottom=23 * 72 / 25.4
    for i,p in enumerate(doc):
        all_boxes=p.search_for(author)
        boxes=all_boxes if i==0 else [box for box in all_boxes if box.y1 < header_bottom]
        if len(boxes)!=1:
            raise AssertionError(f"{file.name}, página {i+1}: autor en portada/cabecera aparece {len(boxes)} veces; total visible {len(all_boxes)}")
        if i==0:
            if boxes[0].y0 < 90:
                raise AssertionError(f"{file.name}: autor en cabecera en lugar de portada")
            if "Índice del módulo" in p.get_text("text"):
                raise AssertionError(f"{file.name}: índice mezclado con la portada")
        else:
            if boxes[0].y1 >= header_bottom:
                raise AssertionError(f"{file.name}, página {i+1}: falta el autor en la cabecera superior")
            header=p.get_text("text",clip=fitz.Rect(0,0,p.rect.width,84))
            normalized_header=normalize(header)
            if normalize(course) not in normalized_header:
                raise AssertionError(f"{file.name}: página {i+1}: falta título canónico del curso en cabecera")
            if normalize(kind_label) not in normalized_header:
                raise AssertionError(f"{file.name}: página {i+1}: falta tipo documental en cabecera")
            if "Índice del módulo" not in p.get_text("text"):
                # El capítulo actual se determina por el título H1, que siempre
                # comienza en página nueva. El de la cabecera debe corresponder
                # con uno de los cinco títulos del Markdown (o con el índice).
                expected_any=[normalize("Índice del módulo")]
                expected_any += [normalize(re.sub(r"^#\s*", "",m.group(0))) for m in re.finditer(
                    r"(?m)^# (?:P)?1\.[1-5]\.\s+[^\r\n]+", md)]
                header_txt=normalize(header)
                if not any(v in header_txt for v in expected_any):
                    raise AssertionError(f"{file.name}: página {i+1}: sin título de capítulo canónico. Cabecera extraída: {header!r}")
        if not p.get_text().strip(): raise AssertionError(f"{file.name}: página {i+1} completamente vacía")
        w=p.rect.width
        for x0,y0,x1,y1,*rest in p.get_text("words"):
            if x0<1 or x1>w-1:
                raise AssertionError(f"{file.name}: texto fuera de margen horizontal en página {i+1}")
    print(f"PDF VALIDADO: {file.name}, {len(reader.pages)} páginas, {diagram_count} diagramas, AUTOR en portada y cabeceras posteriores validado, fuente Markdown incrustada IDENTICA byte por byte; ratio palabras {fraction:.1%}")

def main():
    from validar_m01 import run
    run()
    results=[generate("TEORIA"),generate("PRACTICAS")]
    text=["# M01 — Verificación automática de PDF y Markdown","",
          "**Carácter:** control técnico interno. No aparece en los PDF docentes.","",
          "Las dos ediciones se generan directamente de los Markdown canónicos, sin resumir capítulos ni ejemplos.",
          "Se comprueba la existencia de los cinco capítulos, retos, contenido fundamental, diagramas vectoriales y páginas PDF sin texto vacío ni recortes horizontales detectables.",
          "", "| Archivo | Palabras MD | Caracteres MD | Páginas PDF | Diagramas SVG |",
          "|---|---:|---:|---:|---:|"]
    for item in results:
        text.append(f"| {item['tipo']} | {item['palabras_markdown']} | {item['caracteres_markdown']} | {item['paginas_pdf']} | {item['diagramas_renderizados']} |")
    text += ["","## Autor procedente del Markdown","",
             "Los dos PDF presentan **AUTOR: JAIME GALLO** en portada y en la cabecera de cada página siguiente.",
             "El texto repetido en la cabecera se toma de la línea canónica del Markdown correspondiente; no se introduce un autor independiente en el generador.",
             "","## Huellas de fuente canónica","","| Documento | SHA-256 del MD que está incrustado en el PDF | Coincidencia byte por byte |","|---|---|---|"]
    for item in results:
        text.append(f"| {item['tipo']} | `{item['md_sha256']}` | {item['fuente_incrustada_igual']} |")
    text += ["","## Alcance y límites","",
             "La validación calcula conteos, inspecciona texto extraído y cajas de texto mediante PyMuPDF, y comprueba que cada diagrama Mermaid tiene salida SVG. "
             "Este resultado **no implica** inspección visual manual de todas las páginas, navegación con lectores de pantalla o una clase piloto.",
             "Las pruebas E2E del código se ejecutan mediante el workflow independiente \`m01-ci.yml\`.",
             ""]
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text("\n".join(text),encoding="utf-8")
    print(json.dumps(results,ensure_ascii=False,indent=2))

if __name__=="__main__":
    try: main()
    except Exception as e:
        print(f"ERROR AL GENERAR PDF M01: {e}",file=sys.stderr)
        raise
