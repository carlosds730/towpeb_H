from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin

from Shop_Site import models, repots


# Register your models here.


class AttributeAdminInline(admin.StackedInline):
    model = models.Attribute
    extra = 1


class AddressAdminInline(admin.StackedInline):
    model = models.Address
    extra = 1


class PicturesInline(AdminImageMixin, admin.StackedInline):
    model = models.Pictures
    extra = 1


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'user', 'action_time')


# class AgotadoListFilter(admin.SimpleListFilter):
#     title = _("Agotado")
#     parameter_name = "agotado"
#
#     def lookups(self, request, model_admin):
#         return [
#             ('True', _('Agotado')),
#             ('False', _('No sgotado')),
#         ]
#
#     def queryset(self, request, queryset):
#         if self.value() == 'True':
#             return queryset.filter(on_hold=False)
#         if self.value() == 'False':
#             return queryset.filter(on_hold=True)


class ProductsAdmin(AdminImageMixin, admin.ModelAdmin):
    model = models.Products
    inlines = [AttributeAdminInline, PicturesInline]
    list_display = ['name', 'cod_ref', 'admin_amount', 'product_price', 'discount_percent']
    search_fields = ['name', 'cod_ref', 'label']
    # list_filter = ['name', 'label']
    readonly_fields = ['percent']
    prepopulated_fields = {"slug": ("name",)}
    actions = ['reverse_discount', 'discount']

    def product_price(self, obj):
        return obj.total_price()

    product_price.short_description = 'Precio Actual'
    product_price.admin_order_field = 'price'

    def discount_percent(self, obj):
        if obj.percent and obj.percent != 0:
            return str(obj.percent) + "%"
        else:
            return None

    discount_percent.short_description = 'Descuento'
    discount_percent.admin_order_field = 'percent'

    def admin_amount(self, obj):
        amount = obj.sold_out()
        if amount > 0:
            return '<span>%s</span>' % amount
        return '<span style="color:red">Agotado</span>'

    admin_amount.allow_tags = True
    admin_amount.short_description = 'Existencias'
    # admin_amount.admin_order_field = 'percent'

    def discount(self, request, queryset):
        for product in queryset:
            product.set_discount(10)

    discount.short_description = 'Aplicar descuento de 50'

    def reverse_discount(self, request, queryset):
        for product in queryset:
            product.reverse_discount()

    reverse_discount.short_description = 'Eliminar descuentos'


class CategoryAdmin(AdminImageMixin, admin.ModelAdmin):
    models = models.Category
    list_display = ['name', 'parent']
    search_fields = ['name']
    list_filter = ['name']
    prepopulated_fields = {"slug": ("name",)}


class ClientAdmin(admin.ModelAdmin):
    models = models.Clients
    inlines = [AddressAdminInline]
    list_display = ['name', 'email']
    search_fields = ['name', 'address', 'email']
    list_filter = ['name', 'email', 'is_ghost']
    readonly_fields = ['password']
    actions = ['download_mails']

    def download_mails(self, request, queryset):
        f = open("mails.txt", mode='w')

        for cliente in queryset.all():
            f.writelines(cliente.email + ";")

        f.writelines("\n")

        f.close()

        file = open('mails.txt', mode='r+b')
        name = 'mails.txt'
        response = HttpResponse(file, content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename="%s"' % name
        self.message_user(request, 'Archivo generado con éxito')
        return response

    download_mails.short_description = 'Descargar los mails de los clientes'


class PagadoListFilter(admin.SimpleListFilter):
    title = _("Pagado")
    parameter_name = "pagado"

    def lookups(self, request, model_admin):
        return [
            ('True', _('Pagado')),
            ('False', _('No Pagado')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(on_hold=False)
        if self.value() == 'False':
            return queryset.filter(on_hold=True)


class MontoListFilter(admin.SimpleListFilter):
    title = _("Monto")
    parameter_name = "monto"

    def lookups(self, request, model_admin):
        return [
            ('50', _('Menores que 50 €')),
            ('100', _('Entre 50 € y 100 €')),
            ('200', _('Entre 100 € y 200 €')),
            ('300', _('Mayores que 200 €')),
        ]

    def queryset(self, request, queryset):
        if self.value() == '50':
            return queryset.filter(monto__lte=50)
        if self.value() == '100':
            return queryset.filter(monto__gt=50, monto__lte=100)
        if self.value() == '200':
            return queryset.filter(monto__gt=100).filter(monto__lte=200)
        if self.value() == '300':
            return queryset.filter(monto__gt=200)


class PurchaseAdmin(admin.ModelAdmin):
    models = models.Purchase
    list_display = ['number', 'admin_client', 'address', 'date', 'Pagado', 'Costo']
    search_fields = ['address']
    list_filter = ['date', MontoListFilter, PagadoListFilter, 'client']
    filter_horizontal = ['products']
    readonly_fields = ['transaction_id', 'monto']
    exclude = ['delivery_address', 'amount']
    actions = ['generate_report', 'generate_report_each']

    def generate_report_each(self, request, queryset):
        import os

        files = []

        for purchase in queryset.all():
            if not purchase.on_hold:
                path = repots.CreatePDF(purchase, False)
                files.append((path, os.path.split(path)[1]))

        from zipfile import ZipFile
        with ZipFile('download.zip', 'w') as myzip:
            count = 0
            for fl in files:
                myzip.write(fl[0], arcname=fl[1])
                count += 1
            myzip.close()

        file = open('download.zip', mode='r+b')
        name = 'download.zip'
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="%s"' % name
        self.message_user(request, 'Tickets generados con éxito')
        return response

    generate_report_each.short_description = 'Descargar los tickets de envío para los carritos seleccionados (solo carritos pagados)'

    def generate_report(self, request, queryset):
        name, total = repots.CreateReportPDF(queryset)
        return HttpResponseRedirect('/media/reportes/' + name)

    generate_report.short_description = 'Generar un reporte de los carritos seleccionados'

    def admin_client(self, obj):
        if obj.client:
            return '<a href="../clients/%s/">%s</a>' % (obj.client.id, obj.client.full_name())
        else:
            return '<span>(Nada)</span>'

    admin_client.allow_tags = True
    admin_client.short_description = 'Cliente'
    admin_client.admin_order_field = 'client'


class NewsletterClientsAdmin(admin.ModelAdmin):
    model = models.Newsletter_Clients
    list_display = ['email']
    search_fields = ['email']
    list_filter = ['email']
    actions = ['download_mails']

    def download_mails(self, request, queryset):
        f = open("mails.txt", mode='w')

        for cliente in queryset.all():
            f.writelines(cliente.email + ";")

        f.writelines("\n")

        f.close()

        file = open('mails.txt', mode='r+b')
        name = 'mails.txt'
        response = HttpResponse(file, content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename="%s"' % name
        self.message_user(request, 'Archivo generado con éxito')
        return response

    download_mails.short_description = 'Descargar los mails de los clientes'


class LookBookImgAdmin(AdminImageMixin, admin.ModelAdmin):
    models = models.LookBookImg
    list_display = ['__str__', 'sort_order']


class FrontImgAdmin(AdminImageMixin, admin.ModelAdmin):
    models = models.LookBookImg
    list_display = ['__str__', 'sort_order']


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Clients, ClientAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Newsletter_Clients, NewsletterClientsAdmin)
admin.site.register(models.LookBookImg, LookBookImgAdmin)
admin.site.register(models.FrontImg, FrontImgAdmin)
