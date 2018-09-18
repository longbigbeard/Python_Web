# -*- coding: utf-8 -*-
# FileName : app
# Author   : 大长胡子
# Date : 2018/9/12
# SoftWare : PyCharm

from flask import Flask,render_template,request,url_for,redirect,session
import config
from models import *
from exts import db
from decorations import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)







@app.route('/')
@login_required
def index():
    context = {
        'questions': Question.query.all()
    }
    return render_template('index.html',**context)


@app.route('/login/',methods =['GET','POST'] )
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone==telephone,User.password ==password).first()
        if user:
            session['user_id'] = user.id
            # r如果31天内不需要登录
            # session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误！'



@app.route('/regist/',methods =['GET','POST'] )
def regist():
    if request.method =='GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 =request.form.get('password1')
        password2 =request.form.get('password2')

        # 手机号码验证是否注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册,更换手机号码'
        else:
            # 验证注册 密码是否相等
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # 注册成功之后，跳转到登录页面
                return redirect(url_for('login'))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        return {'user':user}
    else:
        return {}


# 注销，清除session
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html',question = question_model)


@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('detail',question_id = question_id))








if __name__ == '__main__':
    app.run()
