#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
@author:Administrator
@file:storage.py
@time:2019-01-05 13:53
'''
from django.core.files.storage import Storage
from django.conf import settings
import pyhdfs

class HDFSStorage(Storage):
    def __init__(self):
        '''初始化'''
        self.hosts = settings.HDFS_HOSTS
        self.user_name = settings.HDFS_USERNAME
        self.file_url = settings.HDFS_FILE_URL
        self.hdfs_url = settings.HDFS_URL

    def _open(self, name, mode='rb'):
        '''打开文件时用'''
        pass
    def _url(self):
        pass

    def _save(self, name, content):
        '''保存文件时用'''
        # name，选择上传文件的名字
        # content,包含上传文件内容的File对象

        # 创建一个hdfs_client对象
        client = pyhdfs.HdfsClient(hosts=self.hosts,user_name=self.user_name)
        #判断文件是否上传，如果没有上传就上传
        if not client.exists(self.file_url+content.name):
            client.create(self.file_url+content.name,content)
        #否则文件已上传则不用上传，直接返回文件名
        filename=self.file_url+content.name
        return filename

    def exists(self, name):
        '''django判断文件名是否可用'''
        return False

    def url(self, name):
        '''返回访问文件的URL路径'''
        return self.hdfs_url +name+'?op=open'
