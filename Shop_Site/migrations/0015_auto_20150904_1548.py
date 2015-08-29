# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0014_auto_20150904_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_available',
            field=models.BooleanField(verbose_name='Disponible', default=True, help_text='Define si un producto se puede sacar en la tienda'),
        ),
        migrations.AddField(
            model_name='products',
            name='mark',
            field=models.CharField(verbose_name='Marca', default='Zara', max_length=200, help_text='Marca del producto'),
            preserve_default=False,
        ),
    ]
