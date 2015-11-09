# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0032_auto_20150903_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='especial_offer',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2015, 9, 4, 0, 15, 27, 749848, tzinfo=utc),
                                   verbose_name='Fecha', help_text='Fecha en que se realiza la compra', null=True),
        ),
    ]
