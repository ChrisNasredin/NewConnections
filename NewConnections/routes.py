from . import app
from flask import render_template, url_for
from .forms import LoginForm

@app.route('/')
def index():
    return render_template('index.html', title='Главная')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.validate_on_submit())
    return render_template('login.html', form=form)
