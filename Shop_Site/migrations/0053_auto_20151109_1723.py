# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0052_auto_20151109_1720'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LookBookImg',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(verbose_name='Fecha', help_text='Fecha en que se realiza la compra',
                                   default=datetime.datetime(2015, 11, 9, 22, 23, 31, 489516, tzinfo=utc), null=True,
                                   blank=True),
        ),
    ]
