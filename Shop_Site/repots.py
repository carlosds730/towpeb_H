__author__ = 'Carlos'

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT = defaultPageSize[1];
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()

Title = "Hello world"
pageinfo = "platypus example"


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 26)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, Title)
    canvas.setFont('Helvetica', 11)
    canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()


def getHeaders(listHeaders):
    toRet = []
    for head in listHeaders:
        P = Paragraph('''<para align=center><b>%s</b></para>''' % head, styles["BodyText"])
        toRet.append([P])
    return [toRet]


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
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ('SPAN', (0, -1), (-2, -1))
                       ]))


def go():
    doc = SimpleDocTemplate("phello.pdf")
    Story = [Spacer(1, 1 * inch)]
    style = styles["BodyText"]
    Story.append(t)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


go()
