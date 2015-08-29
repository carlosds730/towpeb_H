# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0020_auto_20150818_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha', blank=True, default=datetime.datetime(2015, 10, 3, 18, 47, 32, 775354, tzinfo=utc)),
        ),
    ]
