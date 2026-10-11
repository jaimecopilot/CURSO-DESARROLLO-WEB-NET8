#!/usr/bin/env python3
"""Auditoría sin modificar Markdown ni PDF: conteos por punto y diferencias."""
import re, json, unicodedata, sys
from collections import Counter
from pathlib import Path
from rapidfuzz.distance import Levenshtein
import fitz
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
M01=ROOT/"M01_MVC"
docs=[("TEORIA","TEORIA"),("PRACTICAS","PRACTICAS")]
rx_md=r"(?m)^#\s+(?:P)?1\.([1-5])\.\s+.*$"

def count_words(txt):
    return len(txt.split())

def char_count(txt):
    return len(txt)

def normalized_words(txt):
    txt=unicodedata.normalize("NFKC",txt).casefold()
    return re.findall(r"\w+",txt,flags=re.UNICODE)

def ordered_differences(expected, actual):
    # Cada palabra es un símbolo indivisible; diferencia de edición en orden.
    words=sorted(set(expected)|set(actual))
    encoded={word:chr(i+0x1000) for i,word in enumerate(words)}
    source="".join(encoded[word] for word in expected)
    result="".join(encoded[word] for word in actual)
    ops=Levenshtein.editops(source,result)
    absent=[]
    additions=[]
    replacements=[]
    for op in ops:
        if op.tag=="delete": absent.append({"posicion_fuente":op.src_pos,"palabra":expected[op.src_pos]})
        elif op.tag=="insert": additions.append({"posicion_pdf":op.dest_pos,"palabra":actual[op.dest_pos]})
        elif op.tag=="replace": replacements.append({"posicion_fuente":op.src_pos,"esperado":expected[op.src_pos],"obtenido":actual[op.dest_pos]})
    return {"omisiones_en_orden":len(absent),"adiciones_en_orden":len(additions),
            "alteraciones_en_orden":len(replacements),
            "ejemplos_omisiones":absent[:20],"ejemplos_adiciones":additions[:20],
            "ejemplos_alteraciones":replacements[:20]}

def divide_md(content):
    matches=list(re.finditer(rx_md,content))
    if len(matches)!=5 or [m.group(1) for m in matches] != list("12345"):
        raise AssertionError("No se localizaron cinco capítulos Markdown canónicos")
    return {
        m.group(1):content[m.start(): matches[i+1].start() if i+1<len(matches) else len(content)]
        for i,m in enumerate(matches)
    }

def visible_markdown(md_text):
    # Mermaid es un gráfico, no texto literal en el documento final.
    non_diagram=re.sub(r"(?ms)^~~~mermaid\s*\n.*?^~~~\s*$", "", md_text)
    parser=MarkdownIt("commonmark",{"html":True}).enable("table")
    html=parser.render(non_diagram)
    soup=BeautifulSoup(html,"html.parser")
    return soup.get_text(" ",strip=True)

def pdf_chapter_pages(pdf, prefix):
    found={}
    found_text=[]
    expected=[str(i) for i in range(1,6)]
    for pn,page in enumerate(pdf):
        d=page.get_text("dict")
        for block in d["blocks"]:
            for line in block.get("lines",[]):
                spans=line.get("spans",[])
                if not spans: continue
                line_text="".join(s["text"] for s in spans).strip()
                match=re.match(rf"^{prefix}1\.([1-5])\.\s+\S",line_text)
                if match and max(s["size"] for s in spans) >= 16:
                    key=match.group(1)
                    found_text.append({"chapter":key,"page":pn+1,"heading":line_text,"size":round(max(s["size"] for s in spans),1)})
                    found.setdefault(key,pn)
    if list(found.keys())!=expected:
        raise AssertionError(f"Cabeceras por punto no detectadas o duplicadas: {found_text}")
    return found,found_text

def pdf_body_text(page):
    # Ignorar pie y cabecera creados por la plantilla PDF.
    p=page
    rect=fitz.Rect(0,46,p.rect.width,p.rect.height-48)
    return p.get_text("text",clip=rect,sort=True)

def audit_one(kind):
    stem="M01_"+kind
    md_path=M01/kind/(stem+".md")
    pdf_path=M01/kind/(stem+".pdf")
    source=md_path.read_text(encoding="utf-8")
    parts=divide_md(source)
    pdf=fitz.open(pdf_path)
    prefix="P" if kind=="PRACTICAS" else ""
    starts,headings=pdf_chapter_pages(pdf,prefix)
    rows=[]
    for i,n in enumerate("12345"):
        start=starts[n];end=starts[str(i+2)] if i<4 else len(pdf)
        pdftext="\n".join(pdf_body_text(pdf[pg]) for pg in range(start,end))
        raw=parts[n]
        display=visible_markdown(raw)
        mdtokens=normalized_words(display)
        pdftokens=normalized_words(pdftext)
        md_counter=Counter(mdtokens);pdf_counter=Counter(pdftokens)
        missing=md_counter-pdf_counter
        added=pdf_counter-md_counter
        # Comparación adicional que respeta el orden del contenido fuente.
        alignment=ordered_differences(mdtokens,pdftokens)
        shared=sum((md_counter&pdf_counter).values())
        row={
            "punto":"1."+n,
            "paginas_desde":start+1, "paginas_hasta":end,
            "num_paginas":end-start,
            "md_literal_palabras":count_words(raw),
            "md_literal_caracteres":char_count(raw),
            "md_visible_palabras":count_words(display),
            "md_visible_caracteres":char_count(display),
            "pdf_extraido_palabras":count_words(pdftext),
            "pdf_extraido_caracteres":char_count(pdftext),
            "diferencia_literal_palabras":count_words(pdftext)-count_words(raw),
            "diferencia_literal_caracteres":len(pdftext)-len(raw),
            "tokens_normalizados_fuente":len(mdtokens),
            "tokens_normalizados_pdf":len(pdftokens),
            "tokens_compartidos":shared,
            "faltantes_normalizados":sum(missing.values()),
            "adiciones_normalizadas":sum(added.values()),
            "faltantes_frecuentes":missing.most_common(12),
            "adiciones_frecuentes":added.most_common(12),
            "alineacion_secuencial":alignment
        }
        rows.append(row)
    return {
        "documento":kind,
        "total_md_literal_palabras":count_words(source),
        "total_md_literal_caracteres":len(source),
        "total_pdf_paginas":len(pdf),
        "cabeceras_detectadas":headings,
        "por_punto":rows,
        "aviso":"Los conteos PDF y MD literal no tienen por qué coincidir: sintaxis Markdown, figuras, encabezados y composición alteran el texto extraíble. Los tokens son diagnóstico, no una prueba concluyente de fidelidad."
    }

def main():
    for kind in ["TEORIA","PRACTICAS"]:
        r=audit_one(kind)
        print("========== "+kind+" ==========")
        print(f"MD: {r['total_md_literal_palabras']} palabras, {r['total_md_literal_caracteres']} caracteres; PDF: {r['total_pdf_paginas']} páginas")
        print("Punto | paginas | MD literal palabras/caracteres | MD visible palabras/caracteres | PDF extraído palabras/caracteres | faltan/sobran tokens")
        for x in r["por_punto"]:
            print(f"{x['punto']} | {x['paginas_desde']}-{x['paginas_hasta']} | "
                  f"{x['md_literal_palabras']}/{x['md_literal_caracteres']} | "
                  f"{x['md_visible_palabras']}/{x['md_visible_caracteres']} | "
                  f"{x['pdf_extraido_palabras']}/{x['pdf_extraido_caracteres']} | "
                  f"{x['faltantes_normalizados']}/{x['adiciones_normalizadas']} | "
                  f"omisiones/alteraciones en orden: {x['alineacion_secuencial']['omisiones_en_orden']}/{x['alineacion_secuencial']['alteraciones_en_orden']}")
        print("JSON_AUDITORIA_INICIO")
        print(json.dumps(r,ensure_ascii=False,indent=2))
        print("JSON_AUDITORIA_FIN")
if __name__=="__main__":
    main()
