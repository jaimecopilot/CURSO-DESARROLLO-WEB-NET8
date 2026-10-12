#!/usr/bin/env python3
"""Vistas de TODAS las páginas de ambos PDF para revisión visual editorial."""
from pathlib import Path
import fitz
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"VERIFICACION_INTERNA"/"M02_VISUAL"
OUT.mkdir(parents=True,exist_ok=True)
font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font=ImageFont.truetype(font_path,19)
C=4; R=4; W=370; GAP=17; HEADER=33; TOP=47
def render_sheet(pdf,kind):
    pages=len(pdf)
    sheets=[]
    for start in range(0,pages,C*R):
        sample=pdf[0]; h=round(W*sample.rect.height/sample.rect.width)
        canvas=Image.new("RGB",(C*(W+GAP)+GAP,R*(h+HEADER+GAP)+GAP+TOP), "#dbe3eb")
        pen=ImageDraw.Draw(canvas)
        pen.text((GAP,12),f"M02 {kind} - páginas {start+1} a {min(start+C*R,pages)} / {pages}",fill="#182939",font=font)
        for pos,pn in enumerate(range(start,min(start+C*R,pages))):
            p=pdf[pn]
            scale=W/p.rect.width
            pix=p.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
            thumb=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
            x=GAP+(pos%C)*(W+GAP)
            y=TOP+GAP+(pos//C)*(h+HEADER+GAP)
            canvas.paste(thumb,(x,y))
            pen.rectangle((x-1,y-1,x+W+1,y+h+1),outline="#8795a2",width=1)
            pen.text((x+5,y+h+4),f"Página {pn+1}",fill="#172c42",font=font)
        fn=OUT/f"{kind}_HOJA_{start//(C*R)+1:02d}.png"
        canvas.save(fn,optimize=True)
        sheets.append(fn)
    # Alta resolución para portada, primera página de texto y últimas.
    high_pages=sorted(set([0,1,2,pages//2,pages-2,pages-1]))
    for i in high_pages:
        page=pdf[i]; pix=page.get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False)
        pix.save(str(OUT/f"{kind}_PAGINA_{i+1:03d}.png"))
    return sheets,high_pages
for kind in ("TEORIA","PRACTICAS"):
    source=ROOT/"M02_FORMULARIOS_RAZOR"/kind/f"M02_{kind}.pdf"
    pdf=fitz.open(source)
    sheets,high=render_sheet(pdf,kind)
    print(kind,"PDF",len(pdf),"páginas",len(sheets),"hojas-contacto",len(high),"páginas de alta resolución")
