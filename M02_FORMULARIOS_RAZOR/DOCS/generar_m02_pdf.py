#!/usr/bin/env python3
"""M02: PDF desde Markdown canónico; reutiliza el estilo de M01, sin sus textos."""
from collections import Counter
from pathlib import Path
from html import escape
from io import BytesIO
import hashlib,json,re,sys,unicodedata
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"M02_FORMULARIOS_RAZOR"
sys.path.insert(0,str(ROOT/"M01_MVC"/"DOCS"))
import generar_m01_pdf as estilo
from markdown_it import MarkdownIt
from weasyprint import HTML
from pypdf import PdfReader,PdfWriter
import fitz
CSS=(estilo.CSS_TEMPLATE
     .replace("font-size: 9.8pt; line-height: 1.46","font-size: 11.2pt; line-height: 1.60")
     .replace("font-size: 8.2pt; line-height: 1.35","font-size: 9.0pt; line-height: 1.50"))
CSS+=estilo.HTML_FORMATTER.get_style_defs(".highlight")
CSS += "\np { margin: 7.5pt 0 10pt; }\nh2 { margin-top: 19pt; }\n"
CHAPTER=re.compile(r"^(?:P)?2\.([1-5])\.\s")
OUT=ROOT/"VERIFICACION_INTERNA"/"M02_PDFS_VALIDACION.md"

def html_from_md(source,kind):
    course=estilo.metadata_from_markdown(source,"CURSO")
    label=estilo.metadata_from_markdown(source,"TIPO")
    author=estilo.author_from_markdown(source)
    assert author=="AUTOR: JAIME GALLO"
    assert label==("TEORÍA" if kind=="TEORIA" else "PRÁCTICAS")
    # Mantener visibles las URLs de la fuente, además de enlazarlas.
    src=re.sub(r"(?m)^(-\s+[^\n]*?:\s*)(https?://[^\s<>]+)",
        lambda m:m.group(1)+"["+m.group(2)+"]("+m.group(2)+")",source)
    md=MarkdownIt("commonmark",{"html":True}).enable("table").enable("strikethrough")
    md.renderer.rules["fence"]=estilo.fence_render
    rendered=md.render(src)
    chapters=[]
    first=[True]
    def h1(m):
        txt=m.group(1)
        plain=re.sub("<[^>]*>","",txt)
        match=CHAPTER.match(plain)
        if match:
            chapters.append(match.group(1))
            return f'<h1 class="chapter" id="punto-{match.group(1)}">{txt}</h1>'
        if first[0]:
            first[0]=False
            return f'<h1 class="doc-title">{txt}</h1>'
        return "<h1>"+txt+"</h1>"
    rendered=re.sub(r"<h1>(.*?)</h1>",h1,rendered,flags=re.S)
    assert chapters==list("12345"),f"{kind}: orden de capítulos {chapters}"
    cover=(r'(<h1 class="doc-title">.*?</h1>\s*<h2>.*?</h2>\s*'
       r'<p><strong>CURSO:\s*'+re.escape(escape(course))+r'</strong></p>\s*'
       r'<p><strong>TIPO:\s*'+re.escape(escape(label))+r'</strong></p>\s*'
       r'<p><strong>'+re.escape(escape(author))+r'</strong></p>)')
    rendered,n=re.subn(cover,r'<section class="cover">\1</section>',rendered,count=1,flags=re.S)
    assert n==1,f"{kind}: faltan metadatos de portada"
    rendered=rendered.replace("<h2>Índice del módulo</h2>",
        '<h2 class="toc-heading">Índice del módulo</h2>',1)
    def cssq(s):return s.replace("\\","\\\\").replace('"','\\"').replace("\n"," ")
    css=(CSS.replace("__MD_COURSE__",cssq(course))
            .replace("__MD_TYPE__",cssq(label))
            .replace("__MD_AUTHOR__",cssq(author)))
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
       +'<style>'+css+'</style></head><body>'+rendered+'</body></html>')

def verify(target,md,kind,raw):
    reader=PdfReader(str(target))
    name=target.stem+".md"
    embedded=reader.attachments.get(name)
    if isinstance(embedded,list):
        assert len(embedded)==1
        embedded=embedded[0]
    assert embedded==raw,f"{kind}: fuente Markdown adjunta no idéntica"
    assert reader.metadata.author=="AUTOR: JAIME GALLO"
    pages=len(reader.pages)
    print(f"{kind}: {pages} páginas, {len(md.split())} palabras Markdown.",flush=True)
    if not 72<=pages<=100:
        print(f"AVISO: {kind} necesita revisar extensión: {pages} páginas.",flush=True)
    doc=fitz.open(target)
    chapters={}
    for i,page in enumerate(doc):
        t=page.get_text("text")
        if not t.strip():raise AssertionError(f"{kind}: página vacía {i+1}")
        if i>0 and "JAIME GALLO" not in t:raise AssertionError(f"{kind}: autor ausente en {i+1}")
        for word in page.get_text("words"):
            x0,y0,x1,y1=word[:4]
            if x0<2 or x1>page.rect.width-2 or y0<2 or y1>page.rect.height-2:
                raise AssertionError(f"{kind}: texto desbordado página {i+1}: {word[:4]}")
        for n in range(1,6):
            label=("P" if kind=="PRACTICAS" else "")+f"2.{n}."
            if label in t and n not in chapters:chapters[n]=i+1
    assert len(chapters)==5,f"{kind}: faltan capítulos {chapters}"
    return {"tipo":kind,"paginas":pages,"palabras_md":len(md.split()),
       "caracteres_md":len(md),"bytes_pdf":target.stat().st_size,
       "sha256_md":hashlib.sha256(raw).hexdigest(),
       "fuente_md_incrustada_identica":True,"capitulos_inicio":chapters}

def create(kind):
    source=BASE/kind/f"M02_{kind}.md"
    target=BASE/kind/f"M02_{kind}.pdf"
    raw=source.read_bytes()
    md=raw.decode("utf-8")
    html=html_from_md(md,kind)
    HTML(string=html,base_url=str(BASE)).write_pdf(str(target))
    writer=PdfWriter()
    writer.append(BytesIO(target.read_bytes()))
    writer.add_metadata({"/Author":"AUTOR: JAIME GALLO",
       "/Title":f"M02 {kind}: formularios y Razor Pages"})
    writer.add_attachment(filename=source.name,data=raw)
    buf=BytesIO()
    writer.write(buf)
    target.write_bytes(buf.getvalue())
    return verify(target,md,kind,raw)

def main():
    results=[create("TEORIA"),create("PRACTICAS")]
    if any(not 72<=r["paginas"]<=100 for r in results):
        raise AssertionError("Los dos PDF deben aproximarse a 80 páginas antes de publicarse.")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    lines=["# M02 — Informe técnico documental","",
       "Las fuentes de contenido son únicamente los dos Markdown canónicos.",
       "Cada PDF incluye su Markdown completo, adjunto idéntico byte por byte.",
       "","| Documento | Palabras MD | Páginas PDF |","|---|---:|---:|"]
    for row in results:
        lines.append(f"| {row['tipo']} | {row['palabras_md']} | {row['paginas']} |")
    lines+=["","## Detalle de comprobaciones","",
       "Se verificaron portada, autor, cinco capítulos, paginación, integridad binaria de Markdown adjunto y límites de texto extraíble.",
       "La inspección visual humana página a página no se sustituye por estas comprobaciones.",
       "",json.dumps(results,ensure_ascii=False,indent=2)]
    OUT.write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(results,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
