#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
@author:Administrator
@file:base_model.py
@time:2018-12-06 09:57
'''
from django.db import models

class BaseModel(models.Model):
    '''抽象模型基类'''
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_created=True,verbose_name="更新时间")
    is_delete = models.BooleanField(default=False,verbose_name="删除标记")

    class Meta:
        #说明是一个抽象模型类
        abstract = True