# -*- coding: utf-8 -*-
import random
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    # generate a random number in 0~1000, store it into session.
    session['number'] = random.randint(0, 1000)
    session['times'] = 10
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    times = session['times']
    result = session.get('number')
    form = GuessNumberForm()
    if form.validate_on_submit():
        times -= 1
        session['times'] = times  # update session value
        if times == 0:
            flash(u'你输啦……o(>﹏<)o', 'danger')
            return redirect(url_for('.index'))
        answer = form.number.data
        if answer > result:
            flash(u'太大了！你还剩下%s次机会。' % times, 'warning')
        elif answer < result:
            flash(u'太小了！你还剩下%s次机会。' % times, 'info')
        else:
            flash(u'啊哈，你赢了！V(＾－＾)V', 'success')
            return redirect(url_for('.index'))
    return render_template('guess.html', form=form)


class GuessNumberForm(Form):
    number = IntegerField(u'输入一个整数(0~1000)', validators=[
        Required(u'请输入一个有效的整数！'),
        NumberRange(0, 1000, u'请输入0~1000以内的整数！')])
    submit = SubmitField(u'提交')


if __name__ == '__main__':
    app.run()
