# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0033_auto_20150903_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='special_offer',
            name='attr',
        ),
        migrations.AddField(
            model_name='attribute',
            name='attr',
            field=models.OneToOneField(to='Shop_Site.Special_Offer', blank=True, related_name='special_offer',
                                       null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 4, 0, 28, 27, 36396, tzinfo=utc), blank=True,
                                   help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha'),
        ),
    ]
