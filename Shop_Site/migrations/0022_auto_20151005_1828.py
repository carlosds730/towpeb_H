# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0021_auto_20151003_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale_product',
            name='amount',
            field=models.IntegerField(default=0, blank=True, verbose_name='Cantidad', null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(help_text='Fecha en que se realiza la compra', blank=True, verbose_name='Fecha', null=True, default=datetime.datetime(2015, 10, 5, 22, 28, 25, 128902, tzinfo=utc)),
        ),
    ]
