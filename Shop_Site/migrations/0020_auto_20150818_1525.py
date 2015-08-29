# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0019_purchase_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, help_text='Fecha en que se realiza la compra', default=datetime.datetime(2015, 8, 18, 19, 25, 58, 657905, tzinfo=utc), blank=True, verbose_name='Fecha'),
        ),
    ]
