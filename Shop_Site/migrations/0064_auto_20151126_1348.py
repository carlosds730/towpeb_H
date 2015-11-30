# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0063_auto_20151126_1318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['-sort_order'], 'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(default='', max_length=200, verbose_name='Slug'),
            preserve_default=False,
        ),
    ]
