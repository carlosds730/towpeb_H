# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Shop_Site.models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0012_auto_20150812_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('price', models.FloatField(validators=[Shop_Site.models.validate], verbose_name='Precio', default=0, help_text='Precio del producto')),
                ('amount', models.IntegerField(validators=[Shop_Site.models.validate], verbose_name='Cantidad de existencias', default=0, help_text='Cantidad de existencias del producto')),
                ('especial_offer', models.BooleanField(default=False, verbose_name='Oferta Especial', help_text='Define si este precio es una oferta especial')),
                ('product', models.ForeignKey(to='Shop_Site.Products', help_text='Producto a la venta', related_name='sale_info', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Producto en venta',
                'verbose_name_plural': 'Productos en venta',
            },
        ),
        migrations.RemoveField(
            model_name='sale_product',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='sale_product',
            name='product',
        ),
        migrations.AddField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(help_text='Producto a la venta', default=1, related_name='attributes', verbose_name='Producto', to='Shop_Site.Products'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attribute',
            name='color',
            field=models.CharField(null=True, verbose_name='Color', blank=True, help_text='Color del producto', max_length=50),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='size',
            field=models.CharField(help_text='Talla del producto', max_length=50, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], null=True, verbose_name='Talla', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(verbose_name='Productos', blank=True, help_text='Los productos que pertenecen a una compra', to='Shop_Site.Products'),
        ),
        migrations.DeleteModel(
            name='Sale_Product',
        ),
    ]
