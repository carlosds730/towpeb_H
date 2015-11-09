# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0045_auto_20151001_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(help_text='Fecha en que se realiza la compra', blank=True,
                                   default=datetime.datetime(2015, 10, 2, 0, 48, 42, 865939, tzinfo=utc), null=True,
                                   verbose_name='Fecha'),
        ),
    ]
