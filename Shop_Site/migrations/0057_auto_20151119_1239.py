# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0056_auto_20151119_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontimg',
            name='url',
            field=models.URLField(blank=True,
                                  help_text='URL al que debe ir la foto cuando den click sobre ella (puede estar en blanco)',
                                  verbose_name='URL', null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(blank=True, help_text='Descripción del producto', null=True,
                                   verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 19, 17, 39, 6, 343228, tzinfo=utc), blank=True,
                                   help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha'),
        ),
    ]
