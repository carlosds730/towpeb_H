# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0027_auto_20150903_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='province',
            field=models.CharField(blank=True, verbose_name='Provincia', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, verbose_name='Ciudad', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2015, 9, 3, 21, 36, 35, 613182, tzinfo=utc),
                                   verbose_name='Fecha', null=True, help_text='Fecha en que se realiza la compra'),
        ),
    ]
