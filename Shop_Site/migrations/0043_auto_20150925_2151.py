# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0042_auto_20150925_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 26, 1, 51, 8, 400042, tzinfo=utc), blank=True,
                                   verbose_name='Fecha', null=True, help_text='Fecha en que se realiza la compra'),
        ),
    ]
