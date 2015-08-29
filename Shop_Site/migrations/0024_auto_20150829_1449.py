# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0023_auto_20150829_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 8, 29, 18, 49, 55, 723250, tzinfo=utc), blank=True, help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha'),
        ),
    ]
