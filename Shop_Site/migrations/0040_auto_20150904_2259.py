# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0039_auto_20150903_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter_clients',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email',
                                    help_text='Email al que mandar las noticias'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2015, 9, 5, 2, 59, 46, 228027, tzinfo=utc),
                                   verbose_name='Fecha', null=True, help_text='Fecha en que se realiza la compra'),
        ),
    ]
