# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0011_auto_20150811_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='amount',
            field=models.IntegerField(verbose_name='Cantidad', help_text='Cantidad de productos que se quieren comprar', default=1),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='product',
            field=models.ForeignKey(verbose_name='Producto', to='Shop_Site.Products', blank=True, null=True, related_name='pictures'),
        ),
    ]
