# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0035_auto_20150903_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='special_offer',
        ),
        migrations.AddField(
            model_name='special_offer',
            name='attr',
            field=models.OneToOneField(blank=True, verbose_name='Oferta Especial', to='Shop_Site.Attribute',
                                       related_name='special_offer',
                                       help_text='Define los precios nuevos para una oferta', null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 4, 0, 39, 15, 543714, tzinfo=utc), blank=True,
                                   help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha'),
        ),
    ]
