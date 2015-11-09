# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0038_auto_20150903_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter_Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email',
                 models.EmailField(verbose_name='Email', max_length=254, help_text='Email al que mandar las noticias')),
            ],
            options={
                'verbose_name_plural': 'Clientes de noticias',
                'verbose_name': 'Cliente de noticias',
            },
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(blank=True, verbose_name='Fecha', null=True,
                                   help_text='Fecha en que se realiza la compra',
                                   default=datetime.datetime(2015, 9, 4, 2, 37, 50, 916456, tzinfo=utc)),
        ),
    ]
