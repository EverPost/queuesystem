# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuenumber',
            name='isreset',
            field=models.BooleanField(default=False, verbose_name='\u91cd\u7f6e\u6392\u961f\u7cfb\u7edf'),
        ),
    ]
