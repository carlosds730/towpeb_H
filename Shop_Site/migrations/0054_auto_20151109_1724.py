# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
import sorl.thumbnail.fields
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0053_auto_20151109_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='LookBookImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(help_text='Foto para el lookbook', upload_to='Pictures',
                                                           verbose_name='Imagen')),
                ('sort_order', models.IntegerField(help_text='Valor para ordenar', verbose_name='sort_order')),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'LookBookImage',
                'verbose_name_plural': 'LookBookImages',
            },
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 9, 22, 24, 0, 479678, tzinfo=utc),
                                   help_text='Fecha en que se realiza la compra', null=True, verbose_name='Fecha',
                                   blank=True),
        ),
    ]
