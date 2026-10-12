#!/usr/bin/env python3
"""Comprobar fidelidad visible por capítulo y trazabilidad al Markdown M02.

El documento PDF incluye el MD original como adjunto idéntico, pero
esa comprobación binaria no sustituye el análisis del texto VISIBLE.
"""
from collections import Counter
from pathlib import Path
import json,re,unicodedata
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
import fitz
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"M02_FORMULARIOS_RAZOR"
RX=r"(?m)^#\s+(?:P)?2\.([1-5])\.\s+.+$"
OUT=ROOT/"VERIFICACION_INTERNA"/"M02_FIDELIDAD.md"

def words(s):
    return re.findall(r"\w+",unicodedata.normalize("NFKC",s).casefold(),flags=re.UNICODE)

def md_parts(s):
    x=list(re.finditer(RX,s))
    if len(x)!=5 or [m.group(1) for m in x]!=list("12345"):
        raise AssertionError("Los cinco capítulos no son únicos y consecutivos.")
    return [(i+1,s[m.start():x[i+1].start() if i<4 else len(s)]) for i,m in enumerate(x)]

def visible_md(section):
    source=re.sub(r"(?ms)^~~~mermaid\s*\n.*?^~~~\s*$","",section)
    source=re.sub(r"(?m)^(-\s+[^\n]*?:\s*)(https?://[^\s<>]+)",
        lambda m:m.group(1)+"["+m.group(2)+"]("+m.group(2)+")",source)
    parser=MarkdownIt("commonmark",{"html":True}).enable("table").enable("strikethrough")
    return BeautifulSoup(parser.render(source),"html.parser").get_text(" ",strip=True)

def chapter_starts(pdf, kind):
    prefix="P" if kind=="PRACTICAS" else ""
    found={}
    rx=re.compile(rf"^{prefix}2\.([1-5])\.\s")
    for p,page in enumerate(pdf):
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines",[]):
                spans=line.get("spans",[])
                if not spans:continue
                t="".join(s["text"] for s in spans).strip()
                m=rx.match(t)
                if m and max(s["size"] for s in spans)>=16:
                    n=int(m.group(1))
                    if n in found:
                        raise AssertionError(f"{kind}: cabecera 2.{n} repetida (pág. {p+1}).")
                    found[n]=p
    if list(found)!=list(range(1,6)):
        raise AssertionError(f"{kind}: títulos reales de capítulos no encontrados: {found}")
    if len(set(found.values()))!=5:
        raise AssertionError(f"{kind}: capítulos superpuestos: {found}")
    return found

def inspect(kind):
    mdfile=BASE/kind/f"M02_{kind}.md"
    pdffile=BASE/kind/f"M02_{kind}.pdf"
    md=mdfile.read_text(encoding="utf-8")
    binary=mdfile.read_bytes()
    reader=PdfReader(str(pdffile))
    embedded=reader.attachments.get(mdfile.name)
    if isinstance(embedded,list):
        assert len(embedded)==1
        embedded=embedded[0]
    assert embedded==binary,f"{kind}: MD adjunto no coincide byte por byte"
    pdf=fitz.open(pdffile)
    starts=chapter_starts(pdf,kind)
    parts=md_parts(md)
    rows=[]
    for n,section in parts:
        first=starts[n]
        after=starts[n+1] if n<5 else len(pdf)
        pdftext="\n".join(pdf[p].get_text("text",clip=fitz.Rect(
            0,53,pdf[p].rect.width,pdf[p].rect.height-48),sort=True)
             for p in range(first,after))
        expected=words(visible_md(section))
        actual=words(pdftext)
        missing=Counter(expected)-Counter(actual)
        extra=Counter(actual)-Counter(expected)
        missing_count=sum(missing.values())
        coverage=1-missing_count/max(1,len(expected))
        print(kind,n,f"páginas {first+1}-{after}",f"cobertura {coverage:.3%}",
              "faltan",missing_count,missing.most_common(9),flush=True)
        rows.append(dict(punto=f"{'P' if kind=='PRACTICAS' else ''}2.{n}",
            desde=first+1,hasta=after,palabras_visibles_md=len(expected),
            palabras_extraidas_pdf=len(actual),cobertura=round(coverage,6),
            tokens_no_encontrados=missing_count,ejemplos_missing=missing.most_common(20),
            ejemplos_extra=extra.most_common(10)))
        if coverage<0.98:
            raise AssertionError(f"{kind} capítulo 2.{n}: falta texto visible en PDF (>2%).")
    return {"tipo":kind,"paginas":len(pdf),"fuente_original_incrustada_identica":True,
            "capitulos":rows}

def main():
    results=[inspect("TEORIA"),inspect("PRACTICAS")]
    lines=["# Fidelidad de M02: Markdown canónico frente a texto visible PDF","",
        "Informe interno. El PDF se generó del MD y contiene su fuente adjunta idéntica byte a byte.",
        "Se compararon por capítulo las palabras visibles representadas desde Markdown y extraídas del cuerpo PDF,",
        "excluyendo las cabeceras y pies repetidos y los bloques Mermaid transformados en diagrama.",
        "", "| Documento | Capítulo | Páginas | Cobertura tokens MD → PDF | Tokens no encontrados |",
        "|---|---|---|---:|---:|"]
    for doc in results:
        for row in doc["capitulos"]:
            lines.append(f"| {doc['tipo']} | {row['punto']} | {row['desde']}-{row['hasta']} | {row['cobertura']:.2%} | {row['tokens_no_encontrados']} |")
    lines+=["","Los contadores de tokens son un diagnóstico de extracción textual: no prueban idéntica maquetación,",
        "igualdad visual de los diagramas ni ausencia de errores de lectura humana.",
        "","## Datos","",json.dumps(results,ensure_ascii=False,indent=2)]
    OUT.write_text("\n".join(lines),encoding="utf-8")

if __name__=="__main__":
    main()
