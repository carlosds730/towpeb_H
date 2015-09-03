# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0002_auto_20150727_0123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='etiquetas',
            new_name='label',
        ),
    ]
