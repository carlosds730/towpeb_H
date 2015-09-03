# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0010_purchase_on_hold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='visible',
        ),
        migrations.AddField(
            model_name='sale_product',
            name='especial_offer',
            field=models.BooleanField(default=False, help_text='Define si este precio es una oferta especial', verbose_name='Oferta Especial'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='password',
            field=models.CharField(max_length=400, verbose_name='Password', help_text='Password del cliente, NO SE PUEDE EDITAR'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='on_hold',
            field=models.BooleanField(default=True, help_text='Define si la compra no se ha realizado', verbose_name='En espera'),
        ),
    ]
