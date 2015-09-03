# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0004_auto_20150730_1244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pictures',
            options={'verbose_name_plural': 'Fotos', 'verbose_name': 'Foto'},
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(upload_to='Pictures', help_text='Foto del principal producto', null=True, verbose_name='Imagen Principal', blank=True),
        ),
    ]
