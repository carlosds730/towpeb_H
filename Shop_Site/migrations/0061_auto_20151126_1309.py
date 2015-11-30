# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0060_auto_20151126_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=sorl.thumbnail.fields.ImageField(verbose_name='Imagen Principal', upload_to='Pictures',
                                                   help_text='Foto del principal producto'),
        ),
        migrations.AlterField(
            model_name='products',
            name='percent',
            field=models.IntegerField(verbose_name='Porciento', null=True, blank=True, default=None),
        ),
    ]
