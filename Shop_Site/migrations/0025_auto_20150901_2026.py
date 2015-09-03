# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Site', '0024_auto_20150829_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(null=True, verbose_name='Nombre', max_length=100, blank=True)),
                ('last_name', models.CharField(null=True, verbose_name='Apellidos', max_length=200, blank=True)),
                ('address', models.CharField(null=True, verbose_name='Dirección', max_length=400, blank=True)),
                ('company', models.CharField(null=True, verbose_name='Compañía', max_length=100, blank=True)),
                ('apt_suite', models.CharField(null=True, verbose_name='Apartamento/Suite', max_length=50, blank=True)),
                ('city', models.CharField(null=True, verbose_name='Ciudad', max_length=50, blank=True)),
                ('country', models.CharField(null=True, verbose_name='País', max_length=100, blank=True)),
                ('postal_code', models.CharField(null=True, verbose_name='Código Postal', max_length=50, blank=True)),
                ('phone', models.CharField(null=True, verbose_name='Télefono', max_length=50, blank=True)),
            ],
            options={
                'verbose_name': 'Dirección',
                'verbose_name_plural': 'Direcciones',
            },
        ),
        migrations.RemoveField(
            model_name='clients',
            name='address',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(help_text='Fecha en que se realiza la compra', default=datetime.datetime(2015, 9, 2, 0, 26, 11, 236797, tzinfo=utc), null=True, verbose_name='Fecha', blank=True),
        ),
        migrations.AddField(
            model_name='address',
            name='cliente',
            field=models.ForeignKey(related_name='addresses', to='Shop_Site.Clients', null=True, verbose_name='Cliente', blank=True),
        ),
    ]
