# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0034_auto_20150903_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='attr',
        ),
        migrations.AddField(
            model_name='attribute',
            name='special_offer',
            field=models.OneToOneField(null=True, help_text='Define los precios nuevos para una oferta',
                                       related_name='attribute', verbose_name='Oferta Especial',
                                       to='Shop_Site.Special_Offer', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 4, 0, 31, 9, 378423, tzinfo=utc), null=True,
                                   verbose_name='Fecha', blank=True, help_text='Fecha en que se realiza la compra'),
        ),
    ]
