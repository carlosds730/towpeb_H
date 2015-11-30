# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0062_products_sort_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['sort_order'], 'verbose_name_plural': 'Productos', 'verbose_name': 'Producto'},
        ),
    ]
