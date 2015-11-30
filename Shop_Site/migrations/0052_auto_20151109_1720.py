# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc
import sorl.thumbnail.fields


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0051_auto_20151109_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='LookBookImg',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image',
                 sorl.thumbnail.fields.ImageField(help_text='Foto para el lookbook', upload_to='Pictures', null=True,
                                                  verbose_name='Imagen', blank=True)),
                ('sort_order', models.IntegerField(help_text='Valor para ordenar', verbose_name='sort_order')),
            ],
            options={
                'verbose_name': 'LookBookImage',
                'ordering': ['sort_order'],
                'verbose_name_plural': 'LookBookImages',
            },
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, help_text='Fecha en que se realiza la compra', verbose_name='Fecha',
                                   default=datetime.datetime(2015, 11, 9, 22, 20, 5, 686019, tzinfo=utc), blank=True),
        ),
    ]
