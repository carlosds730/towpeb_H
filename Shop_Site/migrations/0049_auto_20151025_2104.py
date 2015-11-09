# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0048_auto_20151012_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, help_text='Fecha en que se realiza la compra', verbose_name='Fecha',
                                   default=datetime.datetime(2015, 10, 26, 1, 3, 58, 711042, tzinfo=utc), blank=True),
        ),
    ]
