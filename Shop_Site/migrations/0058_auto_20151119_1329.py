# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0057_auto_20151119_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='size',
            field=models.CharField(help_text='Talla del producto', max_length=50, verbose_name='Talla',
                                   choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('42', '42'),
                                            ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46')]),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 19, 18, 29, 23, 453623, tzinfo=utc), null=True,
                                   verbose_name='Fecha', blank=True, help_text='Fecha en que se realiza la compra'),
        ),
    ]
