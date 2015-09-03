# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0003_auto_20150727_0135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, verbose_name='Imagen', help_text='Foto del producto', upload_to='Pictures')),
            ],
            options={
                'verbose_name': 'Picture',
                'verbose_name_plural': 'Pictures',
            },
        ),
        migrations.AlterField(
            model_name='products',
            name='cod_ref',
            field=models.CharField(max_length=100, help_text='Código único que define a un producto', verbose_name='Código de referencia'),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(max_length=300, blank=True, null=True, help_text='Descripción del producto', verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, null=True, verbose_name='Imagen Principal', help_text='Foto del producto principal', upload_to='Pictures'),
        ),
        migrations.AlterField(
            model_name='products',
            name='label',
            field=models.CharField(max_length=200, blank=True, null=True, help_text='Palabras claves que describan al producto que lo ayuden a ser encontrado facilmente por los buscadores', verbose_name='Etiquetas'),
        ),
        migrations.AlterField(
            model_name='products',
            name='short_description',
            field=models.TextField(max_length=100, blank=True, null=True, help_text='Breve descripción del producto', verbose_name='Descripción breve'),
        ),
        migrations.AddField(
            model_name='pictures',
            name='product',
            field=models.ForeignKey(blank=True, null=True, to='Shop_Site.Products', verbose_name='Producto'),
        ),
    ]
