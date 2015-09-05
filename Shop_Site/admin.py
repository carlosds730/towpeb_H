from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from django.contrib.admin.models import LogEntry

from Shop_Site import models




# Register your models here.

class AttributeAdminInline(admin.StackedInline):
    model = models.Attribute
    extra = 2



class PicturesInline(AdminImageMixin, admin.StackedInline):
    model = models.Pictures
    extra = 3


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'user', 'action_time')


class ProductsAdmin(AdminImageMixin, admin.ModelAdmin):
    model = models.Products
    inlines = [PicturesInline, AttributeAdminInline]
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





admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Clients, ClientAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
