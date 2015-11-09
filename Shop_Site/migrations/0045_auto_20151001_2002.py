# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0044_auto_20151001_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='address',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 10, 2, 0, 2, 16, 366286, tzinfo=utc), blank=True,
                                   null=True, help_text='Fecha en que se realiza la compra', verbose_name='Fecha'),
        ),
    ]
