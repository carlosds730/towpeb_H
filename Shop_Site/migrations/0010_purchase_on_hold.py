# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0009_auto_20150807_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='on_hold',
            field=models.BooleanField(help_text='Define si la compra se ha realizado', default=True, verbose_name='En espera'),
        ),
    ]
