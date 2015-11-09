# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0040_auto_20150904_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='color',
            field=models.CharField(help_text='Color del producto', max_length=50, verbose_name='Color', default='red'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attribute',
            name='size',
            field=models.CharField(help_text='Talla del producto', max_length=50, verbose_name='Talla',
                                   choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], default='M'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha',
                                   default=datetime.datetime(2015, 9, 18, 1, 0, 10, 263711, tzinfo=utc), blank=True),
        ),
    ]
