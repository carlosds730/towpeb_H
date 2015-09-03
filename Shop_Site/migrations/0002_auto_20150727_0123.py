# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Shop_Site.models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50, help_text='Nombre de la categoría', verbose_name='Nombre')),
                ('description', models.TextField(null=True, blank=True, max_length=500, help_text='Descripción de la categoría', verbose_name='Descripción')),
                ('image', models.ImageField(null=True, blank=True, upload_to='Pictures', help_text='Foto de la categoría', verbose_name='Imagen')),
                ('parent', models.ForeignKey(help_text='Categoría padre', null=True, blank=True, to='Shop_Site.Category', verbose_name='Padre')),
            ],
            options={
                'verbose_name_plural': 'Categorías',
                'verbose_name': 'Categoría',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, help_text='Nombre del cliente', verbose_name='Nombre')),
                ('address', models.CharField(null=True, blank=True, max_length=400, help_text='Dirección del cliente', verbose_name='Dirección')),
                ('email', models.EmailField(null=True, blank=True, max_length=254, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, help_text='Nombre del producto', verbose_name='Nombre')),
                ('price', models.FloatField(default=0, validators=[Shop_Site.models.validate], help_text='Precio del producto', verbose_name='Precio')),
                ('cod_ref', models.CharField(max_length=100, help_text='Me tienes q decir q poner aqui', verbose_name='Código de referencia')),
                ('etiquetas', models.CharField(max_length=200, help_text='Averiguar q es las etiquetas', verbose_name='Etiquetas')),
                ('cantidad', models.IntegerField(default=0, validators=[Shop_Site.models.validate], help_text='Cantidad de existencias del producto', verbose_name='Cantidad de existencias')),
                ('description', models.TextField(null=True, blank=True, max_length=300, help_text='Breve descripción del producto', verbose_name='Descripción')),
                ('short_description', models.TextField(null=True, blank=True, max_length=100, help_text='Una breve descripción del producto', verbose_name='Descripción breve')),
                ('image', models.ImageField(null=True, blank=True, upload_to='Pictures', help_text='Foto del producto', verbose_name='Imagen')),
                ('visible', models.BooleanField(default=True, help_text='Define si un producto va a ser visible en la tienda', verbose_name='Visible en la tienda')),
                ('category', models.ForeignKey(help_text='La categoría a la que pertenece el producto', null=True, blank=True, to='Shop_Site.Category', verbose_name='Categoría a la que pertenece')),
            ],
            options={
                'verbose_name_plural': 'Productos',
                'verbose_name': 'Producto',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('delivery_address', models.CharField(max_length=400, help_text='Dirección de entrega de la compra', verbose_name='Dirección de entrega')),
                ('products', models.ManyToManyField(blank=True, to='Shop_Site.Products', null=True, help_text='Los productos que pertenecen a una compra', verbose_name='Productos')),
            ],
            options={
                'verbose_name': 'Carrito',
                'verbose_name_plural': 'Carritos',
            },
        ),
        migrations.DeleteModel(
            name='TShirt',
        ),
    ]
