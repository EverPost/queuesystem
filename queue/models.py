# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    '''服务项目'''
    name = models.CharField(verbose_name=u'项目名称',max_length=50,null=True,blank=True)
    des = models.CharField(verbose_name=u'项目简介',max_length=200,null=True,blank=True)
    waittime = models.DecimalField(max_digits=6,decimal_places=1,default=0.5,verbose_name=u"估计等待时间(小时)")
    create_time = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    image = models.ImageField(upload_to='productimage',null=True,blank=True,verbose_name=u'项目照片')

    class Meta:
        verbose_name = u'美容项目'
        verbose_name_plural = u'美容项目'

    def __unicode__(self):
        return self.name


class Person(models.Model):
    '''美容师'''
    name = models.CharField(verbose_name=u'美容师', max_length=10, null=True, blank=True,)
    icon = models.ImageField(upload_to='personicon', null=True,blank=True, verbose_name=u'照片')
    des = models.CharField(verbose_name=u'美容师简介', max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product,verbose_name=u'项目')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'美容师'
        verbose_name_plural = u'美容师'

    def __unicode__(self):
        return self.name


class QueueOrder(models.Model):
    '''排队订单'''
    #获取时间晚于Queuenumber.updatetime 的排队才是有效的
    user = models.ForeignKey(User)
    number = models.IntegerField(verbose_name=u'号码',default=1)
    create_time = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    class Meta:
        verbose_name = u'排队订单'
        verbose_name_plural = u'排队订单'
        #降
        ordering = ['-create_time']

    def __unicode__(self):
        return self.user.username

class Queuenumber(models.Model):
    '''管理排队号码'''
    isacceivequeue = models.BooleanField(verbose_name=u'是否接受预约', default=True)
    lastqueuenumber = models.IntegerField(verbose_name=u'最新用户号码', default=1)
    currentnumber = models.IntegerField(verbose_name=u'正在接受服务的号码', default=1)
    create_time = models.DateTimeField(verbose_name=u'开始服务时间', default=timezone.now)
    updatetime = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    isreset = models.BooleanField(verbose_name=u'重置排队系统',default=False)

    class Meta:
        verbose_name = u'管理排队号码'
        verbose_name_plural = u'管理排队号码'
        ordering = ['-create_time']


class ApointmentOrder(models.Model):
    '''预约'''
    product = models.ForeignKey(Product)
    person = models.ForeignKey(Person)
    user = models.ForeignKey(User)
    ordertime = models.DateTimeField(verbose_name=u'预约时间', null=True,blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now=True)

    def isexpried(self):
        return timezone.now() > self.ordertime

    class Meta:
        verbose_name = u'预约订单'
        verbose_name_plural = u'预约订单'
        ordering = ['-create_time']


    def __unicode__(self):
        return self.product.name


def on_delete(sender, instance, **kwargs):
    instance.image.delete(save=False)

models.signals.post_delete.connect(on_delete, sender=Product)

def on_deleteicon(sender, instance, **kwargs):
    instance.icon.delete(save=False)

models.signals.post_delete.connect(on_deleteicon, sender=Person)

class Access_token(models.Model):
    id = models.IntegerField(primary_key=True, db_column='FId',default=1)
    token = models.CharField(max_length=200,null=True, blank=True)
    time = models.DateTimeField(auto_now=True)



class CustomUser(models.Model):
    sex = (
        (0,u'女'),
        (1,u'男'),
    )
    user = models.ForeignKey(User)
    openid = models.CharField(verbose_name='用户标识',max_length=100,null=True,blank=True)
    nickname = models.CharField(verbose_name='昵称',max_length=50,null=True,blank=True)
    sex = models.IntegerField(choices=sex,verbose_name='性别',null=True)
    headimgurl = models.CharField(max_length=200,null=True,blank=True)

