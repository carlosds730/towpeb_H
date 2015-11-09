__author__ = 'Carlos'
# -*- coding: utf8 -*-

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()


# pageinfo = "platypus example"


def myFirstPage(canvas, doc):
    print(Title)
    canvas.saveState()
    canvas.setFont('Helvetica', 26)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, Title[-1])
    canvas.setFont('Helvetica', 11)
    canvas.drawString(inch, 0.75 * inch, "Página %d" % doc.page)
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def getHeaders(listHeaders):
    toRet = []
    for head in listHeaders:
        P = Paragraph('''<para align=center><b>%s</b></para>''' % head, styles["BodyText"])
        toRet.append([P])
    return [toRet]


Title = []


def CreatePDF(purchase, client):
    Title.append('Ticket %s' % purchase.transaction_id)
    doc = SimpleDocTemplate("%s.pdf" % purchase.transaction_id)
    Story = [Spacer(1, 1 * inch)]
    style = styles["BodyText"]
    P = Paragraph('''<para><b>Descripción del pedido</b></para>''', styles["BodyText"])

    Story.append(P)
    space = Spacer(1, 0.25 * inch)
    Story.append(space)
    Story.append(createTable(purchase))

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


def createTable(purchase):
    data = getHeaders(["Productos", "Cantidad", "Precio Unitario", "Precio Total"])
    data.extend([['00', '01', '02', '03'],
                 ['10', '11', '12', '13'],
                 ['20', '21', '22', '23'],
                 ['30', '31', '32', '33'],
                 ['', '', '', 43]])

    t = Table(data)
    t.setStyle(TableStyle([('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                           ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -2), 0.25, colors.black),
                           ('BOX', (-1, -1), (-1, -1), 0.25, colors.black),
                           ('SPAN', (0, -1), (-2, -1))
                           ]))

    return t
