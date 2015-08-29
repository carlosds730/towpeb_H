# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0015_auto_20150904_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='mark',
            field=models.CharField(max_length=200, help_text='Marca del producto', null=True, verbose_name='Marca', blank=True),
        ),
    ]
