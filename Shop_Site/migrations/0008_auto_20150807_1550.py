# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0007_auto_20150807_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='password',
            field=models.CharField(verbose_name='Password', max_length=400, help_text='Password del cliente', default='a'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.EmailField(verbose_name='Email', max_length=254, default='a@gmail.com'),
            preserve_default=False,
        ),
    ]
