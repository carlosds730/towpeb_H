# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Shop_Site.models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0006_auto_20150803_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('color', models.CharField(max_length=50, help_text='Color del producto', verbose_name='Color')),
                ('size', models.CharField(max_length=50, help_text='Talla del producto', choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], verbose_name='Talla')),
            ],
            options={
                'verbose_name_plural': 'Atributos',
                'verbose_name': 'Atributo',
            },
        ),
        migrations.CreateModel(
            name='Sale_Product',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('price', models.FloatField(validators=[Shop_Site.models.validate], default=0, help_text='Precio del producto', verbose_name='Precio')),
                ('amount', models.IntegerField(validators=[Shop_Site.models.validate], default=0, help_text='Cantidad de existencias del producto', verbose_name='Cantidad de existencias')),
                ('attribute', models.ForeignKey(help_text='Atributos del productos', verbose_name='Atributos', to='Shop_Site.Attribute')),
            ],
            options={
                'verbose_name_plural': 'Productos en venta',
                'verbose_name': 'Producto en venta',
            },
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name_plural': 'Productos', 'verbose_name': 'Producto'},
        ),
        migrations.RemoveField(
            model_name='products',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='products',
            name='price',
        ),
        migrations.AddField(
            model_name='purchase',
            name='client',
            field=models.ForeignKey(null=True, help_text='Cliente que realiza la compra', blank=True, to='Shop_Site.Clients', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(help_text='Los productos que pertenecen a una compra', blank=True, to='Shop_Site.Products', verbose_name='Productos'),
        ),
        migrations.AddField(
            model_name='sale_product',
            name='product',
            field=models.ForeignKey(help_text='Producto a la venta', verbose_name='Producto', to='Shop_Site.Products'),
        ),
    ]
