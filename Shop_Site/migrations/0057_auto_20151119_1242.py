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
            field=models.URLField(null=True,
                                  help_text='URL al que debe ir la foto cuando den click sobre ella (puede estar en blanco)',
                                  verbose_name='URL', blank=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(null=True, help_text='Descripción del producto', verbose_name='Descripción',
                                   blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, help_text='Fecha en que se realiza la compra', verbose_name='Fecha',
                                   blank=True, default=datetime.datetime(2015, 11, 19, 17, 42, 10, 297836, tzinfo=utc)),
        ),
    ]
