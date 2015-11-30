# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import sorl.thumbnail.fields

import Shop_Site.models


class Migration(migrations.Migration):
    dependencies = [
        ('Shop_Site', '0059_auto_20151119_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='size',
            field=models.CharField(
                choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('44', '44'), ('46', '46'), ('48', '48'),
                         ('50', '50'), ('52', '52'), ('54', '54'), ('56', '56'), ('única', 'única')], max_length=50,
                verbose_name='Talla', help_text='Talla del producto'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, verbose_name='Imagen Principal',
                                                   validators=[Shop_Site.models.validate_image], null=True,
                                                   help_text='Foto del principal producto', upload_to='Pictures'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True, blank=True, verbose_name='Fecha',
                                   help_text='Fecha en que se realiza la compra', default=django.utils.timezone.now),
        ),
    ]
