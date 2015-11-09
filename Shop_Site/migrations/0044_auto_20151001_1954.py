# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0043_auto_20150925_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='last_name',
            field=models.CharField(max_length=200, help_text='Apellidos del cliente', blank=True,
                                   verbose_name='Apellidos'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='name',
            field=models.CharField(max_length=200, help_text='Nombre del cliente', blank=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 10, 1, 23, 54, 40, 571920, tzinfo=utc), null=True,
                                   help_text='Fecha en que se realiza la compra', blank=True, verbose_name='Fecha'),
        ),
    ]
