# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0017_auto_20150904_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale_Product',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('attribute', models.ForeignKey(to='Shop_Site.Attribute', blank=True, null=True, verbose_name='Atributo')),
                ('product', models.ForeignKey(to='Shop_Site.Products', blank=True, null=True, verbose_name='Producto')),
            ],
            options={
                'verbose_name_plural': 'Productos vendidos',
                'verbose_name': 'Producto vendido',
            },
        ),
        migrations.AlterField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(related_name='purchase', help_text='Los productos que pertenecen a una compra', blank=True, to='Shop_Site.Sale_Product', verbose_name='Productos'),
        ),
    ]
