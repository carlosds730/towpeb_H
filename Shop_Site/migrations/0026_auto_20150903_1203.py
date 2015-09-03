# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Shop_Site.models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0025_auto_20150901_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='price',
            field=models.DecimalField(validators=[Shop_Site.models.validate], verbose_name='Precio', decimal_places=2, default=0, max_digits=10, help_text='Precio del producto'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.EmailField(verbose_name='Email', help_text='Correo del cliente', max_length=254),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True, default=datetime.datetime(2015, 9, 3, 16, 3, 4, 64660, tzinfo=utc), help_text='Fecha en que se realiza la compra'),
        ),
    ]
