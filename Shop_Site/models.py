# -*- coding: utf8 -*-
import random
from urllib.parse import urljoin
from decimal import *

import django.utils.timezone as tz
from django.db import models
from django.core.exceptions import ValidationError
from sorl.thumbnail import ImageField

from towpeb_H.settings import WEB_SITE_URL as web_site_url






# TODO: Terminar de poner la tallas q faltan, estas fueron la unicas que se me ocurrieron
sizes = [('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')]


# Create your models here.

def validate(number):
    if number >= 0:
        return number
    raise ValidationError('%s No es un precio valido' % number)


class Products(models.Model):
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    name = models.CharField(verbose_name='Nombre', max_length=200, help_text='Nombre del producto')

    cod_ref = models.CharField(verbose_name='Código de referencia', max_length=100,
                               help_text='Código único que define a un producto')

    category = models.ForeignKey('Category', verbose_name='Categoría a la que pertenece', blank=True, null=True,
                                 help_text='La categoría a la que pertenece el producto')

    mark = models.CharField(verbose_name='Marca', max_length=200, help_text='Marca del producto', blank=True, null=True)

    description = models.TextField(verbose_name='Descripción', max_length=300,
                                   help_text='Descripción del producto', null=True, blank=True)

    short_description = models.TextField(verbose_name='Descripción breve', max_length=100,
                                         help_text='Breve descripción del producto', null=True, blank=True)

    image = ImageField(verbose_name='Imagen Principal', upload_to='Pictures',
                       help_text='Foto del principal producto', null=True, blank=True)

    color = models.CharField(verbose_name='Color', max_length=50, help_text='Color del producto')

    price = models.DecimalField(verbose_name='Precio actual', default=0, max_digits=10, decimal_places=2,
                                help_text='Precio real del producto', validators=[validate])

    old_price = models.DecimalField(verbose_name='Precio antiguo de oferta', default=None, max_digits=10,
                                    decimal_places=2, null=True, blank=True,
                                    help_text='Precio anterior del producto si esta en oferta, sino dejar en blanco',
                                    validators=[validate])

    percent = models.IntegerField(verbose_name='Porciento', default=None, null=True, blank=True,
                                  help_text='Porciento de la oferta, sino dejar en blanco')

    label = models.CharField(verbose_name='Etiquetas', max_length=200, blank=True, null=True,
                             help_text='Palabras claves que describan al producto que lo ayuden a ser encontrado '
                                       'fácilmente por los buscadores')

    is_available = models.BooleanField(verbose_name='Disponible', default=True,
                                       help_text='Define si un producto se puede sacar en la tienda')

    def __str__(self):
        return self.name

    def min_price(self):
        return self.price

    def sold_out(self):
        count = 0
        for attr in self.attributes.all():
            count += attr.amount
        return count

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('product', args=[str(self.pk)])

    def get_full_url(self):
        return urljoin(web_site_url, self.get_absolute_url())


class Attribute(models.Model):
    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    product = models.ForeignKey('Products', related_name='attributes', verbose_name='Producto',
                                help_text='Producto a la venta')

    size = models.CharField(verbose_name='Talla', choices=sizes, max_length=50, help_text='Talla del producto')

    amount = models.IntegerField(verbose_name='Cantidad de existencias', default=0, validators=[validate],
                                 help_text='Cantidad de existencias del producto')

    def __str__(self):
        return self.size


class Category(models.Model):
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    name = models.CharField(verbose_name='Nombre', max_length=50, help_text='Nombre de la categoría')

    description = models.TextField(verbose_name='Descripción', max_length=500, help_text='Descripción de la categoría',
                                   blank=True, null=True)

    parent = models.ForeignKey('Category', verbose_name='Padre', blank=True, null=True, help_text='Categoría padre')

    image = ImageField(verbose_name='Imagen', upload_to='Pictures', help_text='Foto de la categoría', null=True,
                       blank=True)

    def __str__(self):
        return str(self.name)

    def min_price(self):
        _min = 10000000
        for x in self.products_set.all():
            if x.price < _min:
                _min = x.price
        return _min if _min != 10000000 else 0

    def get_random_product(self):
        cant_product = self.products_set.all().count()
        if cant_product > 0:
            choice = random.randint(1, cant_product)
            return self.products_set.all()[choice - 1]
        else:
            return None


class Clients(models.Model):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    name = models.CharField(verbose_name='Nombre', max_length=200, help_text='Nombre del cliente')

    last_name = models.CharField(verbose_name='Apellidos', max_length=200, help_text='Apellidos del cliente')

    email = models.EmailField(verbose_name="Email", help_text="Correo del cliente")

    password = models.CharField(verbose_name='Password', max_length=400,
                                help_text='Password del cliente, NO SE PUEDE EDITAR')

    def __str__(self):
        return str(self.name)

        # def save(self, *args, **kwargs):
        # if self.password:
        # self.password = hash(self.password)
        # super(Clients, self).save(*args, **kwargs)

    def full_name(self):
        return str(self.name + " " + self.last_name)


class Purchase(models.Model):
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    products = models.ManyToManyField('Sale_Product', related_name='purchase', blank=True, verbose_name='Productos',
                                      help_text='Los productos que pertenecen a una compra')

    delivery_address = models.CharField(verbose_name='Dirección de entrega', max_length=400, blank=True, null=True,
                                        help_text='Dirección de entrega de la compra')

    client = models.ForeignKey('Clients', verbose_name='Cliente', blank=True, null=True,
                               help_text='Cliente que realiza la compra')

    on_hold = models.BooleanField(verbose_name='En espera', default=True,
                                  help_text='Define si la compra no se ha realizado')

    # when the hasn't been payed date represents the date the of the first purchase made in this cart.
    # when the Purchase has been settled for payment date represents the date when this happened.
    date = models.DateField(verbose_name='Fecha', default=tz.now(), blank=True, null=True,
                            help_text='Fecha en que se realiza la compra')

    amount = models.IntegerField(verbose_name='Cantidad', default=1,
                                 help_text='Cantidad de productos que se quieren comprar')

    transaction_id = models.CharField(verbose_name='Id de la Transacción', default='', max_length=700,
                                      help_text='Numero de la transacción')

    def __str__(self):
        return str(self.pk)

    def is_valid(self):
        for p in self.products.all():
            if not p.valid():
                return False
        return True

    def total_price(self):
        total = 0
        for p in self.products.all():
            total += p.product.price * p.amount
        return str(total) + ' €'

    def total_price_two(self):
        total = 0
        for p in self.products.all():
            total += p.product.price * p.amount
        return str(total) + ' €', str(total)

    def total_price_with_taxes(self):
        total = shipping_Cost()[0]
        for p in self.products.all():
            total += p.product.price * p.amount
        print(total)
        print(str(total * 100).split('0')[0])
        return str(total) + ' €', str(total), str(total * 100).split('.')[0]

    def discount(self):
        if self.on_hold:
            self.on_hold = False
            for sale_product in self.products.all():
                if sale_product.valid():
                    sale_product.attribute.amount -= sale_product.amount
                else:
                    raise Exception()
            for sale_product in self.products.all():
                sale_product.attribute.save()
                sale_product.save()


class Sale_Product(models.Model):
    class Meta:
        verbose_name = 'Producto vendido'
        verbose_name_plural = 'Productos vendidos'

    product = models.ForeignKey('Products', verbose_name='Producto', blank=True, null=True)

    attribute = models.ForeignKey('Attribute', verbose_name='Atributo', blank=True, null=True)

    amount = models.IntegerField(verbose_name='Cantidad', default=0, null=True, blank=True)

    def __str__(self):
        return str(self.product) + ' ' + str(self.attribute)

    def price(self):
        return str(self.product.price * self.amount) + ' €'

    def valid(self):
        return self.amount <= self.attribute.amount

    def to_show_old_cart(self):
        total = self.product.price * self.amount
        return 'Talla: ' + str(
            self.attribute.size + ' - ' 'Color: ' + self.product.color + ' - ' + 'Precio Total: ' + str(total) + '€')

    def to_show_email(self):
        return self.product.name + ' Talla:' + str(self.attribute)


class Pictures(models.Model):
    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

    image = ImageField(verbose_name='Imagen', upload_to='Pictures',
                       help_text='Foto del producto', null=True, blank=True)

    product = models.ForeignKey('Products', verbose_name='Producto', null=True, blank=True, related_name='pictures')

    def __str__(self):
        return str(self.image.name)


class Address(models.Model):
    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

    client = models.OneToOneField('Clients', verbose_name='Clientes', related_name='address', blank=True,
                                  null=True)

    address = models.CharField(verbose_name='Dirección', blank=True, null=True, max_length=400)

    company = models.CharField(verbose_name='Compañía', blank=True, null=True, max_length=100)

    apt_suite = models.CharField(verbose_name='Apartamento/Suite', blank=True, null=True, max_length=50)

    city = models.CharField(verbose_name='Ciudad', blank=True, null=True, max_length=100)

    province = models.CharField(verbose_name='Provincia', blank=True, null=True, max_length=100)

    country = models.CharField(verbose_name='País', blank=True, null=True, max_length=100)

    postal_code = models.CharField(verbose_name='Código Postal', blank=True, null=True, max_length=50)

    phone = models.CharField(verbose_name='Télefono', blank=True, null=True, max_length=50)

    # def __str__(self):
    #     return self.last_name + ', ' + self.first_name + ' ' + self.province + ', ' + self.country


class Newsletter_Clients(models.Model):
    class Meta:
        verbose_name = 'Cliente de noticias'
        verbose_name_plural = 'Clientes de noticias'

    email = models.EmailField(verbose_name='Email', unique=True, help_text='Email al que mandar las noticias')

    def __str__(self):
        return str(self.email)


def shipping_Cost():
    return 4, "4.00"
