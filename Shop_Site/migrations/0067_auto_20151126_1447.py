# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0066_auto_20151126_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Este campo no se edita', max_length=200, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(help_text='Este campo no se edita', max_length=200, verbose_name='Slug'),
        ),
    ]
