# -*- coding: utf-8 -*-
# FileName : models
# Author   : 大长胡子
# Date : 2018/9/13 
# SoftWare : PyCharm

from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    # now()是获取服务器第一次运行的时间
    # now  是每次一创建一个类型的时候，都获取当前时间
    creat_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # 引用了User模型，反转的时候，User通过questions去查找用户发表过的问答
    author = db.relationship('User',backref = db.backref('questions'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime,default=datetime.now)
    # 指定关系
    question = db.relationship('Question',backref = db.backref('answers'))
    author = db.relationship('User',backref = db.backref('answers'))
