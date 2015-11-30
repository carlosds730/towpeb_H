# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0067_auto_20151126_1447'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clients',
            options={'ordering': ['name', 'last_name'], 'verbose_name_plural': 'Clientes', 'verbose_name': 'Cliente'},
        ),
        migrations.AddField(
            model_name='purchase',
            name='monto',
            field=models.DecimalField(decimal_places=2, default=0, max_length=50, verbose_name='Monto', max_digits=10),
            preserve_default=False,
        ),
    ]
