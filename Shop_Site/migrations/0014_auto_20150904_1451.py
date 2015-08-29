# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Shop_Site.models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0013_auto_20150903_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale_info',
            name='product',
        ),
        migrations.AddField(
            model_name='attribute',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='Cantidad de existencias', help_text='Cantidad de existencias del producto', validators=[Shop_Site.models.validate]),
        ),
        migrations.AddField(
            model_name='attribute',
            name='especial_offer',
            field=models.BooleanField(default=False, verbose_name='Oferta Especial', help_text='Define si este precio es una oferta especial'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='price',
            field=models.FloatField(default=0, verbose_name='Precio', help_text='Precio del producto', validators=[Shop_Site.models.validate]),
        ),
        migrations.DeleteModel(
            name='Sale_Info',
        ),
    ]
