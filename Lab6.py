import os
import json
import fitz
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm


def get_font():
    f_p = 'DejaVuSans.ttf'
    if not os.path.exists(f_p):
        u = "https://raw.githubusercontent.com/prawnpdf/prawn/master/data/fonts/DejaVuSans.ttf"
        try:
            r = requests.get(u, timeout=10)
            with open(f_p, 'wb') as f:
                f.write(r.content)
        except:
            return 'Helvetica'
    pdfmetrics.registerFont(TTFont('DejaVuSans', f_p))
    return 'DejaVuSans'


def get_full_code(p):
    if not os.path.exists(p): return ["# Файл коду не знайдено"]
    if p.endswith('.ipynb'):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                d = json.load(f)
            lines = []
            for c in d.get('cells', []):
                if c.get('cell_type') == 'code':
                    src = c.get('source', [])
                    if src:
                        lines.extend(src)
                        lines.append("\n\n# --- \n\n")
            return lines if lines else ["# Notebook порожній"]
        except:
            return ["# Помилка читання .ipynb"]
    with open(p, 'r', encoding='utf-8') as f:
        return f.readlines()


def make_code_pdf(fn, lines, f_n):
    doc = SimpleDocTemplate(fn, pagesize=A4, leftMargin=1.5 * cm, rightMargin=1 * cm, topMargin=1.5 * cm,
                            bottomMargin=1.5 * cm)
    st = ParagraphStyle(name='C', fontName=f_n, fontSize=8, leading=10)
    els = []
    txt = "".join(lines).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for l in txt.split('\n'):
        c = l.replace(" ", "&nbsp;")
        els.append(Paragraph(c if c else "&nbsp;", st))
    doc.build(els)


def make_title(fn, f_n):
    doc = SimpleDocTemplate(fn, pagesize=A4, leftMargin=0, rightMargin=0)
    st_t = ParagraphStyle(name='T', fontName=f_n, fontSize=24, alignment=TA_CENTER, leading=30)
    st_n = ParagraphStyle(name='N', fontName=f_n, fontSize=14, alignment=TA_CENTER, leading=20)
    els = [
        Spacer(1, 9 * cm),
        Paragraph("Підсумковий звіт", st_t),
        Paragraph("з лабораторних робіт 1-6", st_t),
        Spacer(1, 4 * cm),
        Paragraph("Виконавець: Базилевич Олексій", st_n),
        Paragraph("Група: К-27", st_n),
        Paragraph("Викладач: Андрій Ляшко", st_n),
        Spacer(1, 3 * cm),
        Paragraph("2026", st_n)
    ]
    doc.build(els)


def make_sep(fn, n, v, f_n):
    doc = SimpleDocTemplate(fn, pagesize=A4, leftMargin=0, rightMargin=0)
    st = ParagraphStyle(name='S', fontName=f_n, fontSize=28, alignment=TA_CENTER, leading=35)
    vt = f"варіант № {v}" if v else "без варіантів"
    els = [
        Spacer(1, 11 * cm),
        Paragraph(f"Лабораторна робота № {n}", st),
        Paragraph(vt, st)
    ]
    doc.build(els)


def fit_img(ip, op):
    idoc = fitz.open(ip)
    pb = idoc.convert_to_pdf()
    idoc.close()
    timg = fitz.open("pdf", pb)
    fdoc = fitz.open()
    a4w, a4h = fitz.paper_size("A4")
    for p in timg:
        np = fdoc.new_page(width=a4w, height=a4h)
        r = p.rect
        s = min((a4w - 40) / r.width, (a4h - 40) / r.height)
        tw, th = r.width * s, r.height * s
        tr = fitz.Rect((a4w - tw) / 2, (a4h - th) / 2, (a4w + tw) / 2, (a4h + th) / 2)
        np.show_pdf_page(tr, timg, p.number)
    fdoc.save(op)
    fdoc.close()
    timg.close()


def main():
    fn = get_font()
    res = fitz.open()
    tmp = []

    t_f = "t_title.pdf"
    make_title(t_f, fn)
    tmp.append(t_f)
    tdoc = fitz.open(t_f)
    res.insert_pdf(tdoc)
    tdoc.close()

    cfg = [
        {"n": 1, "v": "", "p": "Lab1", "c": "Lab1/MainTaskForLab1/LAB1 робочий зошит.pdf", "code": [], "media": True},
        {"n": 2, "v": "99", "p": "Lab2", "c": "Lab2/MainTaskForLab2/LAB2/LSM.pdf", "code": [], "media": True},
        {"n": 3, "v": "4", "p": "Lab3", "c": "Lab3/MainTaskForLab3/Лаб 3.docx.pdf", "code": [], "media": True},
        {"n": 4, "v": "99 (20; 4)", "p": "Lab4", "c": "Lab4/MainTaskForLab4/Lab4.docx.pdf", "code": [], "media": True},
        {"n": 5, "v": "", "p": "Lab5", "c": "Lab5/MainTaskForLab5/LAB5/lab5.pdf", "code": ["Lab5/Lab5_1.ipynb"],
         "media": True, "no_report": True},
        {"n": 6, "v": "", "p": "Lab6", "c": "Lab6/MainTaskForLab6/lab6.pdf", "code": ["lab6.py"], "media": False}
    ]

    toc, pg = [], 3
    for l in cfg:
        sf = f"t_s_{l['n']}.pdf"
        make_sep(sf, l['n'], l['v'], fn)
        tmp.append(sf)
        sdoc = fitz.open(sf)
        res.insert_pdf(sdoc)
        toc.append([1, f"Лабораторна робота № {l['n']}", pg])
        pg += len(sdoc)
        sdoc.close()

        cp = l["c"]
        if os.path.exists(cp):
            toc.append([2, "Умова", pg])
            cdoc = fitz.open(cp)
            res.insert_pdf(cdoc)
            pg += len(cdoc)
            cdoc.close()

        pd = os.path.join(l['p'], "Pdf")
        if l.get("media") and os.path.exists(pd):
            for f in sorted(os.listdir(pd)):
                fp = os.path.join(pd, f)
                to = f"t_m_{l['n']}_{f}.pdf"
                if f.lower().endswith('.pdf'):
                    if l.get("no_report"): continue
                    toc.append([2, f"Звіт: {f}", pg])
                    md = fitz.open(fp)
                    res.insert_pdf(md)
                    pg += len(md)
                    md.close()
                elif f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    toc.append([2, f"Скріншот: {f}", pg])
                    fit_img(fp, to)
                    tmp.append(to)
                    md = fitz.open(to)
                    res.insert_pdf(md)
                    pg += len(md)
                    md.close()

        for part in l['code']:
            cp = part if os.path.exists(part) else os.path.join(l['p'], part)
            if os.path.exists(cp):
                toc.append([2, f"Код: {os.path.basename(cp)}", pg])
                tf = f"t_c_{l['n']}_{os.path.basename(cp).replace('.', '_')}.pdf"
                tmp.append(tf)
                make_code_pdf(tf, get_full_code(cp), fn)
                cd = fitz.open(tf)
                res.insert_pdf(cd)
                pg += len(cd)
                cd.close()

    st_tt = ParagraphStyle(name='TT', fontName=fn, fontSize=18, alignment=TA_CENTER, spaceAfter=20)
    t_els = [Paragraph("Зміст", st_tt)]
    for lvl, t, p in toc:
        ind = 20 if lvl == 2 else 0
        st_l = ParagraphStyle(name=f'L{lvl}', fontName=fn, fontSize=11, leftIndent=ind)
        t_els.append(Paragraph(f"{t} . . . . . . . . . {p}", st_l))

    t_toc = "t_toc.pdf"
    SimpleDocTemplate(t_toc, pagesize=A4).build(t_els)
    tmp.append(t_toc)
    tdoc = fitz.open(t_toc)
    res.insert_pdf(tdoc, start_at=1)
    tdoc.close()

    res.set_toc(toc)
    res.save("Final_Report_Bazylevich_Alex.pdf")
    res.close()

    for f in tmp:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass
    print("Звіт згенеровано успішно: Final_Report_Bazylevich_Alex.pdf")


if __name__ == "__main__":
    main()