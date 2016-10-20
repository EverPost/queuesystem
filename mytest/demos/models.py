#coding:utf-8
from django.db import models

# Create your models here.

#测试事
class TestTransteaction(models.Model):
    number = models.IntegerField(default=1)

    class Meta:
        verbose_name = "测试事物"
        verbose_name_plural = "测试事物"