# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TShirt',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('_type', models.CharField(verbose_name='Tipo', help_text='Define el tipo de las camisas', max_length=100)),
                ('price', models.FloatField(default=0, verbose_name='Precio', help_text='Precio de las camisa')),
                ('description', models.TextField(verbose_name='Descripcion', help_text='Breve descripcion de la camisa', max_length=300)),
                ('image', models.ImageField(verbose_name='Imagen', upload_to='Pictures', help_text='Foto de la Camisa')),
            ],
            options={
                'verbose_name': 'T-Shirt',
                'verbose_name_plural': 'T-Shirts',
            },
        ),
    ]
