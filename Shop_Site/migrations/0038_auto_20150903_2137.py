# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc

import Shop_Site.models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0037_auto_20150903_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='new_price',
        ),
        migrations.AddField(
            model_name='attribute',
            name='old_price',
            field=models.DecimalField(max_digits=10, decimal_places=2,
                                      help_text='Precio anterior del producto si esta en oferta, sino dejar en blanco',
                                      blank=True, default=None, validators=[Shop_Site.models.validate],
                                      verbose_name='Precio antiguo de oferta', null=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='percent',
            field=models.IntegerField(blank=True, default=None, verbose_name='Porciento',
                                      help_text='Porciento de la oferta, sino dejar en blanco', null=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=2, help_text='Precio real del producto', default=0,
                                      verbose_name='Precio actual', validators=[Shop_Site.models.validate]),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2015, 9, 4, 1, 37, 29, 934512, tzinfo=utc),
                                   verbose_name='Fecha', help_text='Fecha en que se realiza la compra', null=True),
        ),
    ]
