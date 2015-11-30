# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0055_auto_20151119_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontimg',
            name='url',
            field=models.URLField(verbose_name='URL al que debe ir la foto cuando den click sobre ella', blank=True,
                                  null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 19, 8, 28, 11, 272221, tzinfo=utc),
                                   help_text='Fecha en que se realiza la compra', blank=True, verbose_name='Fecha',
                                   null=True),
        ),
    ]
