# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0028_auto_20150903_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2015, 9, 3, 22, 33, 41, 875325, tzinfo=utc),
                                   verbose_name='Fecha', help_text='Fecha en que se realiza la compra', null=True),
        ),
    ]
