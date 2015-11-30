# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone

import Shop_Site.models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0069_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale_product',
            name='price_sale',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Precio', max_length=50),
        ),
        migrations.AlterField(
            model_name='products',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, null=True,
                                      validators=[Shop_Site.models.validate], max_digits=10,
                                      help_text='Precio anterior del producto (usar solo si el producto está en oferta, sino dejar en blando)',
                                      verbose_name='Precio antiguo'),
        ),
        migrations.AlterField(
            model_name='products',
            name='percent',
            field=models.IntegerField(blank=True, default=None, verbose_name='Porciento de descuento', null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(default=0, verbose_name='Precio actual', validators=[Shop_Site.models.validate],
                                      max_digits=10, decimal_places=2, help_text='Precio actual del producto'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Fecha', null=True,
                                   help_text='Fecha en que se realiza la compra'),
        ),
    ]
