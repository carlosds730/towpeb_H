# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentLog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserVault',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('vault_id', models.CharField(max_length=64, unique=True)),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
