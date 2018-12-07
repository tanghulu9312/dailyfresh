#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
@author:Administrator
@file:tasks.py.py
@time:2018-12-07 09:35
'''
#使用celery

from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time

#创建一个Celery类的实例对象
app = Celery('celery_tasks_tasks',broker='redis://127.0.0.1:6379/2')

#定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    "发送激活邮件"
    #组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s,欢迎您成为天天生鲜会员</h1>请点击下面链接激活您的账户<br><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username,token,token)
    send_mail(subject,message,sender,receiver,html_message=html_message)
    time.sleep(5)