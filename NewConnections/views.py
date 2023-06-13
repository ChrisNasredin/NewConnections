from flask import render_template, redirect, flash, typing as ft, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from flask.views import View
from .services import UserService, RequestService, StatusService, save
from .forms import RegisterForm, NewRequestForm, LoginForm, StatusForm, ChangeRequestForm

class LoginRequiredMixin:
    
    decorators=[login_required]

class IndexView(LoginRequiredMixin,View):
    
    def dispatch_request(self):
        request_service = RequestService()
        dataset = request_service.get_all()
        return render_template('index.html', 
                           title='Главная', 
                           dataset=dataset)
        
class NewRequestView(LoginRequiredMixin, View):
   
    methods=['GET', 'POST']
    
    def dispatch_request(self):
        form = NewRequestForm()
        request_service = RequestService()
        if form.validate_on_submit():
            request_service.create_new_request(address=form.address.data,
                            name=form.name.data,
                            phone=form.phone.data,
                            coordinates=form.coordinates.data,
                            author_id=current_user.id)
            flash('Заявка успешно создана', 'success')
            return redirect(url_for('index'))
        return render_template('new.html', form=form)
    
class LoginView(View):
    
    methods=['GET', 'POST']
    
    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        user_service = UserService()
        if form.validate_on_submit():
            user = user_service.user_autentification(form.username.data, form.password.data)
            if user:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
            else:
                flash('Логин или пароль не верны', 'fail')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)
    
class LogoutView(View):
    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))
    
class CreateNewUserView(View):
    
    methods=['GET', 'POST']
    
    def dispatch_request(self):
        form = RegisterForm()
        user_service = UserService()
        if form.validate_on_submit():
            print(form.validate_on_submit())
            user_service.create_new_user(username=form.username.data,
                            password=form.password.data,
                            role=form.role.raw_data[0])
        return render_template('register.html', form=form, title='Регистрация нового пользователя')

class AdminView(View):
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self):
        status_service = StatusService()
        form_add_status = StatusForm()
        if form_add_status.validate_on_submit():
            status_service.add_status(form_add_status.status_desc.data)
            flash('Статус успешно добавлен')
            
        statuses = status_service.get_statuses()
        return render_template('admin.html', 
                        form_add_status=form_add_status,
                        statuses=statuses
                        )
class RequestView(View):
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self, request_id):
        
        request_service = RequestService()
        data = request_service.get_request(request_id)
        form = ChangeRequestForm()
        form.address.data = data.address
        form.name.data = data.name
        form.phone.data = data.phone
        form.coordinates.data = data.coordinates
        form.status.data=data.status
        return render_template('show_request.html', data=data, form=form)


class DeleteRequestView(View):
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self, request_id):
        request_service = RequestService()
        if request.method == 'POST':
            print(request.__dict__)
            request_id = request.view_args['request_id']
            request_service.delete_request(request_id=request_id)
            flash(f'Заявка {request_id} удалена', 'success')
            return redirect(url_for('index'))
        elif request.method == 'GET':
            return render_template('сonfirm.html', id=request_id)
            

class EditRequestView(View):
    
    methods = ['POST', 'GET']
        
    def dispatch_request(self,request_id):
        request_service = RequestService()
        current_request = request_service.get_request(request_id=request_id)
        form = ChangeRequestForm()
        print(form.validate_on_submit())
        if form.validate_on_submit():
            current_request.address = form.address.data 
            current_request.name = form.name.data
            current_request.phone = form.phone.data 
            current_request.coordinates = form.coordinates.data
            current_request.status_id = form.status.raw_data[0]
            save()
            return redirect(url_for('request_item', request_id=request_id))
        elif request.method == 'GET':
            form.address.data = current_request.address
            form.name.data = current_request.name
            form.phone.data = current_request.phone
            form.coordinates.data = current_request.coordinates
            form.status.data=current_request.status
            return render_template('edit.html', form=form)
        return redirect(url_for('show_request', request_id=request_id))