# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0026_auto_20150903_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='cliente',
            field=models.OneToOneField(related_name='address', null=True, to='Shop_Site.Clients',
                                       verbose_name='Cliente', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(verbose_name='Fecha', blank=True,
                                   default=datetime.datetime(2015, 9, 3, 21, 31, 56, 423179, tzinfo=utc), null=True,
                                   help_text='Fecha en que se realiza la compra'),
        ),
    ]
