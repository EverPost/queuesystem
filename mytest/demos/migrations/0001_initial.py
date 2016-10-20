# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestTransteaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': '\u6d4b\u8bd5\u4e8b\u7269',
                'verbose_name_plural': '\u6d4b\u8bd5\u4e8b\u7269',
            },
        ),
    ]
