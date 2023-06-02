from . import app
from flask import render_template, url_for, flash, redirect, request
from .forms import LoginForm, RegisterForm, StatusForm, NewRequestForm, ChangeRequestForm
from .services import create_new_user, get_statuses, add_status, user_autentification, get_dataset, \
    create_new_request, get_request, set_request_status, delete_request, save
from flask_login import current_user, login_user, logout_user

@app.route('/')
def index():
    dataset = get_dataset()
    return render_template('index.html', 
                           title='Главная', 
                           dataset=dataset)

@app.route('/new', methods=['GET', 'POST'])
def new():
    form = NewRequestForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        create_new_request(address=form.address.data,
                           name=form.name.data,
                           phone=form.phone.data,
                           coordinates=form.coordinates.data,
                           author_id=current_user.id)
        flash('Заявка успешно создана', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = user_autentification(form.username.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Логин или пароль не верны')
            print('login fail')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    

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

@app.route('/request/<request_id>', methods=['GET','POST'])
def show_request(request_id):
    data = get_request(request_id)
    form = ChangeRequestForm()
    form.address.data = data.address
    form.name.data = data.name
    form.phone.data = data.phone
    form.coordinates.data = data.coordinates
    form.status.data=data.status
    return render_template('show_request.html', data=data, form=form)

@app.route('/delete/<request_id>', methods=['GET','POST'])
def del_request(request_id):
    delete_request(request_id=request_id)
    flash(f'Заявка {request_id} удалена', 'success')
    return redirect(url_for('index'))


@app.route('/edit/<request_id>', methods=['GET','POST'])
def edit_request(request_id):
    current_request = get_request(request_id=request_id)
    form = ChangeRequestForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        current_request.address = form.address.data 
        current_request.name = form.name.data
        current_request.phone = form.phone.data 
        current_request.coordinates = form.coordinates.data
        current_request.status_id = form.status.raw_data[0]
        save()
        return redirect(url_for('show_request', request_id=request_id))
    elif request.method == 'GET':
        form.address.data = current_request.address
        form.name.data = current_request.name
        form.phone.data = current_request.phone
        form.coordinates.data = current_request.coordinates
        form.status.data=current_request.status
        return render_template('edit.html', form=form)
    return redirect(url_for('show_request', request_id=request_id))