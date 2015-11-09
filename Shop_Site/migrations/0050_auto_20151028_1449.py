# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0049_auto_20151025_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 10, 28, 18, 49, 41, 448526, tzinfo=utc), blank=True,
                                   help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha'),
        ),
    ]
