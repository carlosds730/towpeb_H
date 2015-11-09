__author__ = 'Carlos'
# -*- coding: utf8 -*-

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from Shop_Site.models import shipping_Cost

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()


# pageinfo = "platypus example"


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 26)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, Title[-1])
    print(Title)
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
    P = Paragraph('''<para><b>Detalles del cliente</b></para>''', styles["BodyText"])
    Story.append(P)
    generateInfoClient(purchase, Story)
    space = Spacer(1, 0.25 * inch)
    Story.append(space)

    P = Paragraph('''<para><b>Detalles del envío</b></para>''', styles["BodyText"])
    Story.append(P)
    generateShipment(purchase.client.address, Story)
    space = Spacer(1, 0.25 * inch)
    Story.append(space)

    P = Paragraph('''<para><b>Descripción del pedido</b></para>''', styles["BodyText"])
    Story.append(P)
    space = Spacer(1, 0.1 * inch)
    Story.append(space)
    Story.append(createTable(purchase))

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


def createTable(purchase):
    data = getHeaders(["Producto", "Cantidad", "Precio Unitario", "Precio Total"])
    for sale_product in purchase.products.all():
        data.append(
            [sale_product.to_show_email(), sale_product.amount, sale_product.product.price, sale_product.price()])

    P = Paragraph('''<para align=center><b>%s</b></para>''' % purchase.total_price_with_taxes()[0], styles["BodyText"])
    data.append(['Envío', '', '', shipping_Cost()[1] + ' €'])
    data.append(['', '', '', P])

    t = Table(data)
    t.setStyle(TableStyle([('TEXTCOLOR', (1, 1), (-2, -2), colors.black),
                           ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -2), 0.25, colors.black),
                           ('BOX', (-1, -1), (-1, -1), 0.25, colors.black),
                           ('SPAN', (0, -2), (-2, -2)),
                           ('SPAN', (0, -1), (-2, -1))
                           ]))

    return t


def generateInfoClient(purchase, Story):
    name = Paragraph('''<para><b>Nombre: </b>%s</para>''' % purchase.client.full_name(), styles["BodyText"])
    email = Paragraph('''<para><b>Email: </b>%s</para>''' % purchase.client.email, styles["BodyText"])
    Story.append(name)
    Story.append(email)
    if purchase.client.address.company:
        to_add = Paragraph('''<para><b>Compañía: </b>%s</para>''' % purchase.client.company, styles["BodyText"])
        Story.append(to_add)


def generateShipment(address, Story):
    to_add = Paragraph('''<para><b>Dirección: </b>%s</para>''' % address.address, styles["BodyText"])
    Story.append(to_add)
    if address.apt_suite:
        to_add = Paragraph('''<para><b>Apartamento: </b>%s</para>''' % address.apt_suite, styles["BodyText"])
        Story.append(to_add)
    to_add = Paragraph('''<para><b>Ciudad: </b>%s</para>''' % address.city, styles["BodyText"])
    Story.append(to_add)
    to_add = Paragraph('''<para><b>Provincia: </b>%s</para>''' % address.province, styles["BodyText"])
    Story.append(to_add)
    to_add = Paragraph('''<para><b>Código Postal: </b>%s</para>''' % address.postal_code, styles["BodyText"])
    Story.append(to_add)
    if address.phone:
        to_add = Paragraph('''<para><b>Teléfono: </b>%s</para>''' % address.phone, styles["BodyText"])
        Story.append(to_add)
