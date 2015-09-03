# -*- coding: utf8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from sorl.thumbnail import ImageField

from Shop_Site.extra_functions import hash







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

    description = models.TextField(verbose_name='Descripción', max_length=300,
                                   help_text='Descripción del producto', null=True, blank=True)

    short_description = models.TextField(verbose_name='Descripción breve', max_length=100,
                                         help_text='Breve descripción del producto', null=True, blank=True)

    image = ImageField(verbose_name='Imagen Principal', upload_to='Pictures',
                       help_text='Foto del principal producto', null=True, blank=True)

    label = models.CharField(verbose_name='Etiquetas', max_length=200, blank=True, null=True,
                             help_text='Palabras claves que describan al producto que lo ayuden a ser encontrado facilmente por los buscadores')

    def __repr__(self):
        return self._type + ':' + str(self.price)

    def __str__(self):
        return self.name + ': ' + str(self.cod_ref)

# TODO: Terminar de poner la tallas q faltan, estas fueron la unicas que se me ocurrieron
sizes = [('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')]


class Attribute(models.Model):
    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    color = models.CharField(verbose_name='Color', max_length=50, help_text='Color del producto', blank=True, null=True)

    size = models.CharField(verbose_name='Talla', choices=sizes, max_length=50, help_text='Talla del producto',
                            blank=True, null=True)

    def __str__(self):
        return str(self.size + ': ' + self.color)


class Sale_Product(models.Model):
    class Meta:
        verbose_name = 'Producto en venta'
        verbose_name_plural = 'Productos en venta'

    product = models.ForeignKey('Products', verbose_name='Producto', help_text='Producto a la venta')

    attribute = models.ForeignKey('Attribute', verbose_name='Atributos', help_text='Atributos del productos')

    # TODO: Analizar, en el caso de un producto rebajado, ahora como se hace es creando dos productos en venta y
    # la pagina se da cuenta y lo pone como rebaja pero el trabajador tiene q saber q se pone asi, la otra manera podria ser
    # poner una lista de precios al producto en venta, y cdo sea rebaja le anhade el precio la pag lo muestra como rebaja
    # y cdo se acabe le quita el precio y el producto vuelve al anterior. La primera manera tiene la ventaja de que al crear los
    # dos, cdo se acabe la rebaja pone la cantidad en cero y ya no sale rebaja, y la proxima vez q quiera hacer rebaja solo
    # en cambiarle la cantidad.
    price = models.FloatField(verbose_name='Precio', default=0, help_text='Precio del producto',
                              validators=[validate])

    amount = models.IntegerField(verbose_name='Cantidad de existencias', default=0, validators=[validate],
                                 help_text='Cantidad de existencias del producto')

    especial_offer = models.BooleanField(verbose_name='Oferta Especial', default=False,
                                         help_text='Define si este precio es una oferta especial')

    def __str__(self):
        return str(self.product.name)

    def size(self):
        return str(self.attribute.size)

    def color(self):
        return str(self.attribute.color)


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


class Clients(models.Model):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    name = models.CharField(verbose_name='Nombre', max_length=200, help_text='Nombre del cliente')

    address = models.CharField(verbose_name='Dirección', max_length=400, help_text='Dirección del cliente', blank=True,
                               null=True)

    email = models.EmailField(verbose_name="Email")

    password = models.CharField(verbose_name='Password', max_length=400,
                                help_text='Password del cliente, NO SE PUEDE EDITAR')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super(Clients, self).save(*args, **kwargs)
        if self.password:
            self.password = hash(self.password)


class Purchase(models.Model):
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    products = models.ManyToManyField('Sale_Product', blank=True, verbose_name='Productos',
                                      help_text='Los productos que pertenecen a una compra')

    delivery_address = models.CharField(verbose_name='Dirección de entrega', max_length=400,
                                        help_text='Dirección de entrega de la compra')

    client = models.ForeignKey('Clients', verbose_name='Cliente', blank=True, null=True,
                               help_text='Cliente que realiza la compra')

    on_hold = models.BooleanField(verbose_name='En espera', default=True,
                                  help_text='Define si la compra no se ha realizado')

    amount = models.IntegerField(verbose_name='Cantidad', default=1,
                                 help_text='Cantidad de productos que se quieren comprar')

    def __str__(self):
        return str(self.pk)


class Pictures(models.Model):
    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

    image = ImageField(verbose_name='Imagen', upload_to='Pictures',
                       help_text='Foto del producto', null=True, blank=True)

    product = models.ForeignKey('Products', verbose_name='Producto', null=True, blank=True, related_name='pictures')

    def __str__(self):
        return str(self.image.name)
