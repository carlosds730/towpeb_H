# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0064_auto_20151126_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Este campo no se edita', max_length=200, default='', verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(max_length=200, help_text='Este campo no se edita', verbose_name='Slug'),
        ),
    ]
