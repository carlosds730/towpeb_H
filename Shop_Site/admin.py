from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from django.contrib.admin.models import LogEntry

from Shop_Site import models


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


class ProductsAdmin(AdminImageMixin, admin.ModelAdmin):
    model = models.Products
    inlines = [AttributeAdminInline, PicturesInline]
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
    inlines = [AddressAdminInline]
    list_display = ['name', 'email']
    search_fields = ['name', 'address', 'email']
    list_filter = ['name', 'email', 'is_ghost']
    readonly_fields = ['password']


class PurchaseAdmin(admin.ModelAdmin):
    models = models.Purchase
    list_display = ['__str__', 'delivery_address']
    search_fields = ['delivery_address']
    list_filter = ['delivery_address']
    filter_horizontal = ['products']
    readonly_fields = ['transaction_id']


class NewsletterClientsAdmin(admin.ModelAdmin):
    model = models.Newsletter_Clients
    list_display = ['email']
    search_fields = ['email']
    list_filter = ['email']


class LookBookImgAdmin(AdminImageMixin, admin.ModelAdmin):
    models = models.LookBookImg
    list_display = ['image', 'sort_order']

admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Clients, ClientAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Newsletter_Clients, NewsletterClientsAdmin)
admin.site.register(models.LookBookImg, LookBookImgAdmin)
