# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc

import Shop_Site.models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0041_auto_20150917_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='color',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='old_price',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='percent',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='price',
        ),
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.CharField(default='red', max_length=50, verbose_name='Color', help_text='Color del producto'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='old_price',
            field=models.DecimalField(default=None, verbose_name='Precio antiguo de oferta', blank=True,
                                      decimal_places=2,
                                      help_text='Precio anterior del producto si esta en oferta, sino dejar en blanco',
                                      null=True, max_digits=10, validators=[Shop_Site.models.validate]),
        ),
        migrations.AddField(
            model_name='products',
            name='percent',
            field=models.IntegerField(default=None, null=True, verbose_name='Porciento', blank=True,
                                      help_text='Porciento de la oferta, sino dejar en blanco'),
        ),
        migrations.AddField(
            model_name='products',
            name='price',
            field=models.DecimalField(default=0, verbose_name='Precio actual', decimal_places=2,
                                      help_text='Precio real del producto', max_digits=10,
                                      validators=[Shop_Site.models.validate]),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 26, 1, 13, 6, 869095, tzinfo=utc), null=True,
                                   verbose_name='Fecha', blank=True, help_text='Fecha en que se realiza la compra'),
        ),
    ]
