# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0050_auto_20151028_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='is_ghost',
            field=models.BooleanField(verbose_name='Fantasma',
                                      help_text='Es para cuando un cliente pidió no salvar sus datos', default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(verbose_name='Fecha', null=True, help_text='Fecha en que se realiza la compra',
                                   blank=True, default=datetime.datetime(2015, 11, 9, 17, 14, 10, 314936, tzinfo=utc)),
        ),
    ]
