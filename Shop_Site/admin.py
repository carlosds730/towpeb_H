from django.contrib import admin
from Shop_Site import models
from sorl.thumbnail.admin import AdminImageMixin
from django.contrib.admin.models import LogEntry


# Register your models here.


class PicturesInline(AdminImageMixin, admin.StackedInline):
    model = models.Pictures
    extra = 3


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'user', 'action_time')


class ProductsAdmin(AdminImageMixin, admin.ModelAdmin):
    model = models.Products
    inlines = [PicturesInline]
    list_display = ['name', 'cod_ref', 'short_description', 'label']
    search_fields = ['name', 'cod_ref', 'label']
    list_filter = ['name', 'label']


class CategoryAdmin(AdminImageMixin, admin.ModelAdmin):
    models = models.Category
    list_display = ['name', 'parent']
    search_fields = ['name']
    list_filter = ['name']


class ClientAdmin(admin.ModelAdmin):
    models = models.Clients
    list_display = ['name', 'email']
    search_fields = ['name', 'address', 'email']
    list_filter = ['name', 'email']
    readonly_fields = ['password']


class PurchaseAdmin(admin.ModelAdmin):
    models = models.Purchase
    list_display = ['__str__', 'delivery_address']
    search_fields = ['delivery_address']
    list_filter = ['delivery_address']
    filter_horizontal = ['products']


class Sale_ProductAdmin(admin.ModelAdmin):
    models = models.Sale_Product
    list_display = ['__str__', 'price', 'amount', 'size', 'color']
    search_fields = ['__str__', 'price', 'amount', 'size', 'color']
    list_filter = ['price', 'amount', 'attribute__size', 'attribute__color']


class AttributeAdmin(admin.ModelAdmin):
    models = models.Attribute
    list_display = ['size', 'color']
    search_fileds = ['size', 'color']
    list_filter = ['size', 'color']


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Clients, ClientAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Sale_Product, Sale_ProductAdmin)
admin.site.register(models.Attribute, AttributeAdmin)
