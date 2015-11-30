# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
import sorl.thumbnail.fields
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0054_auto_20151109_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontImg',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('image',
                 sorl.thumbnail.fields.ImageField(upload_to='Pictures', help_text='Foto para aparecer en la portada',
                                                  verbose_name='Imagen')),
                ('sort_order',
                 models.IntegerField(help_text='Valor para ordenar. Aparecen las 4 fotos de mayor priodidad',
                                     verbose_name='Prioridad')),
            ],
            options={
                'verbose_name': 'Imagen de Portada',
                'verbose_name_plural': 'Imágenes de portada',
                'ordering': ['-sort_order'],
            },
        ),
        migrations.AlterField(
            model_name='lookbookimg',
            name='sort_order',
            field=models.IntegerField(help_text='Valor para ordenar', verbose_name='Orden'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, blank=True,
                                   default=datetime.datetime(2015, 11, 19, 7, 41, 35, 418295, tzinfo=utc),
                                   verbose_name='Fecha', help_text='Fecha en que se realiza la compra'),
        ),
    ]
