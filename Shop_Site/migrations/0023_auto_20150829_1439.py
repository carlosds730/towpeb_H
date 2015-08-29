# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0022_auto_20151005_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha', blank=True, default=datetime.datetime(2015, 8, 29, 18, 39, 54, 794976, tzinfo=utc)),
        ),
    ]
