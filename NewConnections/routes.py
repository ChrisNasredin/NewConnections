from . import app
from flask import render_template, url_for, flash, redirect
from .forms import LoginForm, RegisterForm, StatusForm
from .services import create_new_user, get_statuses, add_status
from flask_login import current_user, login_user

@app.route('/')
def index():
    return render_template('index.html', title='Главная')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_autentificated:
        redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        pass
        # Сюда нужно написать логику проверки имени и пароля
        # Но пока не понятно, как работать с моделью
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.validate_on_submit())
        create_new_user(username=form.username.data,
                        password=form.password.data,
                        role=form.role.raw_data[0])
    return render_template('register.html', form=form, title='Регистрация нового пользователя')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    form_add_status = StatusForm()
    if form_add_status.validate_on_submit():
        add_status(form_add_status.status_desc.data)
        flash('Статус успешно добавлен')
        
    statuses = get_statuses()
    return render_template('admin.html', 
                    form_add_status=form_add_status,
                    statuses=statuses
                    )