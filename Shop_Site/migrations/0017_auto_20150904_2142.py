# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0016_auto_20150904_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='label',
            field=models.CharField(help_text='Palabras claves que describan al producto que lo ayuden a ser encontrado fácilmente por los buscadores', max_length=200, verbose_name='Etiquetas', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='delivery_address',
            field=models.CharField(help_text='Dirección de entrega de la compra', max_length=400, verbose_name='Dirección de entrega', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(help_text='Los productos que pertenecen a una compra', to='Shop_Site.Products', verbose_name='Productos', blank=True, related_name='purchase'),
        ),
    ]
