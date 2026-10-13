#!/usr/bin/env python3
"""M04: PDF desde Markdown canónico; reutiliza el estilo de M01, sin sus textos."""
from collections import Counter
from pathlib import Path
from html import escape
from io import BytesIO
import hashlib,json,re,sys,unicodedata
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"M04_APIS_SEGURIDAD"
sys.path.insert(0,str(ROOT/"M01_MVC"/"DOCS"))
import generar_m01_pdf as estilo
from markdown_it import MarkdownIt
from weasyprint import HTML
from pypdf import PdfReader,PdfWriter
import fitz
# Misma escala que M01: texto 9.8 pt y código 8.2 pt.
# No aumentar fuentes ni interlineado para inflar la extensión.
CSS=estilo.CSS_TEMPLATE + estilo.HTML_FORMATTER.get_style_defs(".highlight")
CHAPTER=re.compile(r"^(?:P)?4\.([1-4])(?:\.|\s)")
OUT=ROOT/"VERIFICACION_INTERNA"/"M04_PDFS_VALIDACION.md"

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
    rendered=re.sub(r"<h2>((?:P)?4\.[1-4](?:\.|\s).*?)</h2>",r"<h1>\1</h1>",rendered,flags=re.S)
    rendered=re.sub(r"<h1>(.*?)</h1>",h1,rendered,flags=re.S)
    assert chapters==list("1234"),f"{kind}: orden de capítulos {chapters}"
    cover=(r'(<h1 class="doc-title">.*?</h1>\s*<h2>.*?</h2>\s*'
       r'<p><strong>CURSO:\s*'+re.escape(escape(course))+r'</strong></p>\s*'
       r'<p><strong>TIPO:\s*'+re.escape(escape(label))+r'</strong></p>\s*'
       r'<p><strong>'+re.escape(escape(author))+r'</strong></p>)')
    rendered,n=re.subn(cover,r'<section class="cover">\1</section>',rendered,count=1,flags=re.S)
    assert n==1,f"{kind}: faltan metadatos de portada"
    rendered=rendered.replace("<h2>Índice del módulo</h2>",
        '<h2 class="toc-heading">Índice del módulo</h2>',1)
    if kind=="PRACTICAS":
        # El prólogo, índice y orientaciones ocupan UNA página tras la portada.
        # La compresión es editorial en el prólogo, no en ejercicios/código.
        cover_end=rendered.index("</section>")+len("</section>")
        chapter_start=rendered.index('<h1 class="chapter" id="punto-1">')
        assert chapter_start>cover_end
        rendered=(rendered[:cover_end]+'<section class="module-intro">'
                  +rendered[cover_end:chapter_start]+'</section>'
                  +rendered[chapter_start:])
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
    if not 75<=pages<=100:
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
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines",[]):
                spans=line.get("spans",[])
                if not spans:continue
                rendered_line="".join(span["text"] for span in spans).strip()
                match=re.match(r"^(?:P)?4\.([1-4])(?:\.|\s)",rendered_line)
                if match and max(span["size"] for span in spans)>=16:
                    chapters.setdefault(int(match.group(1)),i+1)
    assert list(chapters)==[1,2,3,4],f"{kind}: falta o está desordenado algún capítulo {chapters}"
    # Comparación de contenido VISIBLE. No confundir la fuente MD adjunta
    # con que todo su texto haya quedado realmente maquetado en el PDF.
    md_without_mermaid=re.sub(r"(?ms)^~~~mermaid\s*\n.*?^~~~\s*$","",md)
    md_html=MarkdownIt("commonmark",{"html":True}).enable("table").enable("strikethrough").render(md_without_mermaid)
    expected=Counter(re.findall(r"\w+",BeautifulSoup(md_html,"html.parser").get_text(" ",strip=True).casefold()))
    body_text="\n".join(page.get_text("text",clip=fitz.Rect(0,72,page.rect.width,page.rect.height-45),sort=True) for page in doc)
    actual=Counter(re.findall(r"\w+",body_text.casefold()))
    missing=expected-actual
    ratio=1-sum(missing.values())/max(1,sum(expected.values()))
    if ratio < 0.999:
        raise AssertionError(f"{kind}: pérdida de palabras visibles MD->PDF: {ratio:.4%}; {missing.most_common(15)}")
    print(f"{kind}: cobertura de palabras visibles {ratio:.3%}; capítulos {chapters}",flush=True)
    return {"tipo":kind,"paginas":pages,"palabras_md":len(md.split()),
       "cobertura_palabras_visibles":round(ratio,6),
       "palabras_faltantes_en_extraccion":missing.most_common(12),
       "caracteres_md":len(md),"bytes_pdf":target.stat().st_size,
       "sha256_md":hashlib.sha256(raw).hexdigest(),
       "fuente_md_incrustada_identica":True,"capitulos_inicio":chapters}

def create(kind):
    source=BASE/kind/f"M04_{kind}.md"
    target=BASE/kind/f"M04_{kind}.pdf"
    raw=source.read_bytes()
    md=raw.decode("utf-8")
    html=html_from_md(md,kind)
    HTML(string=html,base_url=str(BASE)).write_pdf(str(target))
    writer=PdfWriter()
    writer.append(BytesIO(target.read_bytes()))
    writer.add_metadata({"/Author":"AUTOR: JAIME GALLO",
       "/Title":f"M04 {kind}: Integración de APIs y seguridad básica"})
    writer.add_attachment(filename=source.name,data=raw)
    buf=BytesIO()
    writer.write(buf)
    target.write_bytes(buf.getvalue())
    return verify(target,md,kind,raw)

def main():
    results=[create("TEORIA"),create("PRACTICAS")]
    if any(not 75<=r["paginas"]<=100 for r in results):
        print("AVISO EDITORIAL: PDF de ensayo fuera de 75-100 páginas; NO publicar.",flush=True)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    lines=["# M04 — Informe técnico documental","",
       "Las fuentes de contenido son únicamente los dos Markdown canónicos.",
       "Cada PDF incluye su Markdown completo, adjunto idéntico byte por byte.",
       "","| Documento | Palabras MD | Páginas PDF |","|---|---:|---:|"]
    for row in results:
        lines.append(f"| {row['tipo']} | {row['palabras_md']} | {row['paginas']} |")
    lines+=["","## Detalle de comprobaciones","",
       "Se verificaron portada, autor, cuatro capítulos, paginación, integridad binaria de Markdown adjunto y límites de texto extraíble.",
       "La inspección visual humana página a página no se sustituye por estas comprobaciones.",
       "",json.dumps(results,ensure_ascii=False,indent=2)]
    OUT.write_text("\n".join(lines),encoding="utf-8")
    (OUT.parent/"M04_PDF_EXTENSION_OK.txt").write_text("OK" if all(75<=row["paginas"]<=100 for row in results) else "PENDIENTE",encoding="utf-8")
    print(json.dumps(results,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
