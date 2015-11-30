# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0061_auto_20151126_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='sort_order',
            field=models.IntegerField(default=1, verbose_name='Número de orden',
                                      help_text='Este número da el oreden del producto a la hora de mostrarse, se ordena decreciente'),
        ),
    ]
