# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0046_auto_20151001_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='transaction_id',
            field=models.CharField(verbose_name='Id de la Transacción', max_length=500,
                                   help_text='Numero de la transacción', default=''),
        ),
        migrations.AlterField(
            model_name='clients',
            name='last_name',
            field=models.CharField(verbose_name='Apellidos', max_length=200, help_text='Apellidos del cliente'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='name',
            field=models.CharField(verbose_name='Nombre', max_length=200, help_text='Nombre del cliente'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, verbose_name='Fecha', help_text='Fecha en que se realiza la compra',
                                   null=True, default=datetime.datetime(2015, 10, 12, 20, 2, 49, 695563, tzinfo=utc)),
        ),
    ]
