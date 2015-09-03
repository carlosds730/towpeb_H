# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0005_auto_20150730_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=sorl.thumbnail.fields.ImageField(verbose_name='Imagen', upload_to='Pictures', help_text='Foto de la categoría', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='image',
            field=sorl.thumbnail.fields.ImageField(verbose_name='Imagen', upload_to='Pictures', help_text='Foto del producto', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=sorl.thumbnail.fields.ImageField(verbose_name='Imagen Principal', upload_to='Pictures', help_text='Foto del principal producto', null=True, blank=True),
        ),
    ]
