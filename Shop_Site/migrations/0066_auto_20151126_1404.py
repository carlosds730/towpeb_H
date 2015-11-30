# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0065_auto_20151126_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(verbose_name='Slug', help_text='Este campo no se edita', default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(verbose_name='Slug', help_text='Este campo no se edita', default='', max_length=200),
        ),
    ]
