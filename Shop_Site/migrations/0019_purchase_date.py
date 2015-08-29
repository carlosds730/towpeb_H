# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0018_auto_20150904_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, help_text='Fecha en que se realiza la compra', blank=True, verbose_name='Fecha', default=datetime.datetime(2015, 8, 18, 15, 25, 0, 416498)),
        ),
    ]
