# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc

import Shop_Site.models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0031_auto_20150903_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Special_Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('new_price', models.DecimalField(help_text='Precio del producto para la oferta', default=0,
                                                  validators=[Shop_Site.models.validate], decimal_places=2,
                                                  verbose_name='Precio de oferta', max_digits=10)),
                ('percent', models.IntegerField(verbose_name='Porciento', help_text='Porciento de la oferta')),
                ('attr',
                 models.OneToOneField(null=True, related_name='special_offer', to='Shop_Site.Attribute', blank=True)),
            ],
            options={
                'verbose_name': 'Oferta Especial',
                'verbose_name_plural': 'Ofertas Especiales',
            },
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(verbose_name='Fecha', blank=True, null=True,
                                   default=datetime.datetime(2015, 9, 4, 0, 10, 37, 709650, tzinfo=utc),
                                   help_text='Fecha en que se realiza la compra'),
        ),
    ]
