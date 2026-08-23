import json
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#71717A"))
        self.drawString(36, 20, "SMA PHYSICS • DAILY PRACTICE PROBLEM (DPP-43)")
        self.drawRightString(559, 20, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#E4E4E7"))
        self.setLineWidth(0.5)
        self.line(36, 30, 559, 30)
        self.restoreState()

def clean_latex(text):
    if not text:
        return ""
    text = re.sub(r'\$\$(.*?)\$\$', r'<b>\1</b>', text)
    text = re.sub(r'\$(.*?)\$', r'<b>\1</b>', text)
    text = text.replace('\\text{', '').replace('}', '')
    text = text.replace('\\hat{i}', 'i^').replace('\\hat{j}', 'j^').replace('\\hat{k}', 'k^')
    text = text.replace('\\vec{r}', 'r').replace('\\vec{v}', 'v').replace('\\vec{a}', 'a')
    text = text.replace('\\mu', 'μ').replace('\\theta', 'θ').replace('\\omega', 'ω')
    text = text.replace('\\Delta', 'Δ').replace('\\cdot', '·').replace('\\times', '×')
    text = text.replace('\\frac', '').replace('<br>', ' ')
    return text

def build_pdf():
    json_path = os.path.join("dpps", "dpp-43", "dpp-43.json")
    out_pdf = os.path.join("dpps", "dpp-43", "SMA_DPP_43.pdf")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=45
    )

    frame_left = Frame(36, 45, 255, 670, id='col1', leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    frame_right = Frame(303, 45, 255, 670, id='col2', leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame_left, frame_right])])

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('HeadTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#4338CA"), spaceAfter=1)
    sub_style = ParagraphStyle('HeadSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#18181B"), spaceAfter=6)
    q_style = ParagraphStyle('QText', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#09090B"), spaceAfter=3)
    opt_style = ParagraphStyle('OptText', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=8.5, textColor=colors.HexColor("#3F3F46"), spaceAfter=1.5)

    story = []
    story.append(Paragraph("SMA PHYSICS — TARGET JEE MAIN", title_style))
    story.append(Paragraph(f"DPP-43: {data['meta']['title']}", sub_style))
    story.append(Spacer(1, 4))

    for idx, q in enumerate(data['questions'], start=1):
        q_clean = clean_latex(q['statement'])
        story.append(Paragraph(f"<b>Q{idx:02d}.</b> {q_clean}", q_style))
        for opt in q['options']:
            opt_clean = clean_latex(opt['text'])
            story.append(Paragraph(f"<b>({opt['key']})</b> {opt_clean}", opt_style))
        story.append(Spacer(1, 4))

    # Answer Key Table
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>ANSWER KEY (DPP-43)</b>", sub_style))
    ans_data = []
    row1 = [f"Q{i:02d}:{data['questions'][i-1]['correct']}" for i in range(1, 11)]
    row2 = [f"Q{i:02d}:{data['questions'][i-1]['correct']}" for i in range(11, 21)]
    ans_data.append(row1)
    ans_data.append(row2)

    t = Table(ans_data, colWidths=[24]*10)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 5.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#C7D2FE")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {out_pdf}")

if __name__ == '__main__':
    build_pdf()