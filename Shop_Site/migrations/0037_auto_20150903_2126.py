# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc

import Shop_Site.models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0036_auto_20150903_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='special_offer',
            name='attr',
        ),
        migrations.AddField(
            model_name='attribute',
            name='new_price',
            field=models.DecimalField(null=True, verbose_name='Precio de oferta',
                                      validators=[Shop_Site.models.validate], blank=True,
                                      help_text='Precio del producto si esta en oferta, sino dejar en blanco',
                                      decimal_places=2, max_digits=10, default=None),
        ),
        migrations.AddField(
            model_name='attribute',
            name='percent',
            field=models.IntegerField(blank=True, verbose_name='Porciento',
                                      help_text='Porciento de la oferta, sino esta en oferta dejar en blanco',
                                      null=True, default=None),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, verbose_name='Fecha', help_text='Fecha en que se realiza la compra',
                                   null=True, default=datetime.datetime(2015, 9, 4, 1, 26, 24, 331629, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Special_Offer',
        ),
    ]
