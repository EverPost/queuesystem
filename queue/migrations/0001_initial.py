# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Access_token',
            fields=[
                ('id', models.IntegerField(default=1, serialize=False, primary_key=True, db_column='FId')),
                ('token', models.CharField(max_length=200, null=True, blank=True)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApointmentOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordertime', models.DateTimeField(null=True, verbose_name='\u9884\u7ea6\u65f6\u95f4', blank=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u9884\u7ea6\u8ba2\u5355',
                'verbose_name_plural': '\u9884\u7ea6\u8ba2\u5355',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=100, null=True, verbose_name='\u7528\u6237\u6807\u8bc6', blank=True)),
                ('nickname', models.CharField(max_length=50, null=True, verbose_name='\u6635\u79f0', blank=True)),
                ('sex', models.IntegerField(null=True, verbose_name='\u6027\u522b', choices=[(0, '\u5973'), (1, '\u7537')])),
                ('headimgurl', models.CharField(max_length=200, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, null=True, verbose_name='\u7f8e\u5bb9\u5e08', blank=True)),
                ('icon', models.ImageField(upload_to='personicon', null=True, verbose_name='\u7167\u7247', blank=True)),
                ('des', models.CharField(max_length=50, null=True, verbose_name='\u7f8e\u5bb9\u5e08\u7b80\u4ecb', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u7f8e\u5bb9\u5e08',
                'verbose_name_plural': '\u7f8e\u5bb9\u5e08',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, verbose_name='\u9879\u76ee\u540d\u79f0', blank=True)),
                ('des', models.CharField(max_length=200, null=True, verbose_name='\u9879\u76ee\u7b80\u4ecb', blank=True)),
                ('waittime', models.DecimalField(default=0.5, verbose_name='\u4f30\u8ba1\u7b49\u5f85\u65f6\u95f4(\u5c0f\u65f6)', max_digits=6, decimal_places=1)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('image', models.ImageField(upload_to='productimage', null=True, verbose_name='\u9879\u76ee\u7167\u7247', blank=True)),
            ],
            options={
                'verbose_name': '\u7f8e\u5bb9\u9879\u76ee',
                'verbose_name_plural': '\u7f8e\u5bb9\u9879\u76ee',
            },
        ),
        migrations.CreateModel(
            name='Queuenumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isacceivequeue', models.BooleanField(default=True, verbose_name='\u662f\u5426\u63a5\u53d7\u9884\u7ea6')),
                ('lastqueuenumber', models.IntegerField(default=1, verbose_name='\u6700\u65b0\u7528\u6237\u53f7\u7801')),
                ('currentnumber', models.IntegerField(default=1, verbose_name='\u6b63\u5728\u63a5\u53d7\u670d\u52a1\u7684\u53f7\u7801')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u5f00\u59cb\u670d\u52a1\u65f6\u95f4')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u7ba1\u7406\u6392\u961f\u53f7\u7801',
                'verbose_name_plural': '\u7ba1\u7406\u6392\u961f\u53f7\u7801',
            },
        ),
        migrations.CreateModel(
            name='QueueOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=1, verbose_name='\u53f7\u7801')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u6392\u961f\u8ba2\u5355',
                'verbose_name_plural': '\u6392\u961f\u8ba2\u5355',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='product',
            field=models.ForeignKey(verbose_name='\u9879\u76ee', to='queue.Product'),
        ),
        migrations.AddField(
            model_name='apointmentorder',
            name='person',
            field=models.ForeignKey(to='queue.Person'),
        ),
        migrations.AddField(
            model_name='apointmentorder',
            name='product',
            field=models.ForeignKey(to='queue.Product'),
        ),
        migrations.AddField(
            model_name='apointmentorder',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
