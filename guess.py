# -*- coding: utf-8 -*-
import random
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'
bootstrap = Bootstrap(app)  # 初始化Flask-Bootstap扩展

times = 10


@app.route('/')
def index():
    global times
    session['number'] = random.randint(0, 1000)  # 生成一个0~1000的随机数，存储到session变量里。
    times = 10
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    global times
    result = session.get('number')  # 从session变量里获取在index函数里生成的随机数。
    form = GuessNumberForm()
    if form.validate_on_submit():
        times -= 1
        if times == 0:
            flash(u'你输了！')
            return redirect(url_for('.index'))
        answer = form.number.data  # 获取表单的数据
        if answer > result:
            flash(u'太大了！你还剩下%s次机会' % times)
        elif answer < result:
            flash(u'太小了！你还剩下%s次机会' % times)
        else:
            flash(u'你赢了！')
            return redirect(url_for('.index'))
    return render_template('guess.html', form=form)


class GuessNumberForm(Form):
    number = IntegerField(u'输入数字：', validators=[
        # 传入验证函数和相应的错误提示信息。
        Required(u'输入一个有效的数字！'),
        NumberRange(0, 1000, u'请输入0~1000以内的数字！')])
    submit = SubmitField(u'提交')