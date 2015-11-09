# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0029_auto_20150903_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='cliente',
        ),
        migrations.AddField(
            model_name='address',
            name='client',
            field=models.OneToOneField(to='Shop_Site.Clients', related_name='address', null=True,
                                       verbose_name='Clientes', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, help_text='Fecha en que se realiza la compra', verbose_name='Fecha',
                                   default=datetime.datetime(2015, 9, 3, 22, 41, 52, 116721, tzinfo=utc), blank=True),
        ),
    ]
