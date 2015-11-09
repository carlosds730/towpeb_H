# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0047_auto_20151012_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, verbose_name='Fecha',
                                   default=datetime.datetime(2015, 10, 12, 20, 25, 37, 935503, tzinfo=utc), null=True,
                                   help_text='Fecha en que se realiza la compra'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='transaction_id',
            field=models.CharField(verbose_name='Id de la Transacción', default='',
                                   help_text='Numero de la transacción', max_length=700),
        ),
    ]
