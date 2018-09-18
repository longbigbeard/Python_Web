# -*- coding: utf-8 -*-
# FileName : config
# Author   : 大长胡子
# Date : 2018/9/12 
# SoftWare : PyCharm
import os

USER = "root"
PASSED = "a12345"
HOST = "127.0.0.1"
PORT = "3306"
DATABASENAME = "demo_zhizhi"

DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USER,PASSED,HOST,PORT,DATABASENAME)
SQLALCHEMY_DATABASE_URI = DB_URI



SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

SECRET_KEY = os.urandom(24)
