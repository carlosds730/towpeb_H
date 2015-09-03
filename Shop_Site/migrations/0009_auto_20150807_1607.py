# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0008_auto_20150807_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(verbose_name='Productos', blank=True, help_text='Los productos que pertenecen a una compra', to='Shop_Site.Sale_Product'),
        ),
    ]
