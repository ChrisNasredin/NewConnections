from flask import render_template, redirect, flash, typing as ft, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from flask.views import View
from .services import UserService, RequestService, StatusService, save, DeviceService, CommentService, \
    SourceService
from .forms import RegisterForm, LoginForm, RequestForm, \
    DeviceForm, AddStatusForm, AddVendorForm, CommentForm, AddSourceForm, \
    SearchForm
    

class LoginRequiredMixin:
    
    decorators=[login_required]

class IndexView(LoginRequiredMixin,View):
    
    def dispatch_request(self):
        request_service = RequestService()
        dataset = request_service.get_all()
        return render_template('index.html', 
                           title='Главная', 
                           dataset=dataset)
class SearchView(View):

    def dispatch_request(self):
        search_form = SearchForm()
        if request.method == 'GET' and request.args:
            request_service = RequestService()
            print(request.args.get('source'))
            dataset = request_service.get_request_dataset(address=request.args.get('address'),
                                                          name=request.args.get('name'),
                                                          phone=request.args.get('phone'),
                                                          source=request.args.get('source'),
                                                          base=request.args.get('base'),
                                                          start_date=request.args.get('start-date'),
                                                          end_date=request.args.get('end-date'),
                                                          device=request.args.get('device'),
                                                          status=request.args.get('status')
                                                          )
            print(request.args.get('name'))
            print(type(request.args.get('name')))
        else:
            request_service = RequestService()
            dataset = request_service.get_all()
        return render_template('search.html', 
                            title='Главная', 
                            dataset=dataset,
                            search_form=search_form)
        
class NewRequestView(LoginRequiredMixin, View):
   
    methods=['GET', 'POST']
    
    def dispatch_request(self):
        form = RequestForm()
        request_service = RequestService()
        print(form.validate_on_submit())
        print(form.errors)
        if form.validate_on_submit():
            request_service.create_new_request(address=form.address.data,
                            name=form.name.data,
                            phone=form.phone.data,
                            source=form.source.raw_data[0],
                            coordinates=form.coordinates.data,
                            author_id=current_user.id)
            flash('Заявка успешно создана', 'success')
            return redirect(url_for('index'))
        return render_template('new_request.html', form=form)
    
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
                            role=form.role.raw_data[0]  )
        return render_template('register.html', form=form, title='Регистрация нового пользователя')

class AdminView(View):
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self):
        user_service = UserService()
        device_service = DeviceService()
        status_service = StatusService()
        form_add_status = AddStatusForm()
        form_add_device = DeviceForm()
        form_add_vendor = AddVendorForm()
        form_add_source = AddSourceForm()
        source_service = SourceService()
        users = user_service.get_all_users()
        devices = device_service.get_all_devices()
        vendors = device_service.get_all_vendors()
        statuses = status_service.get_statuses()
        sources = source_service.get_all_sources()
        
        if form_add_status.submit_status.data and form_add_status.validate_on_submit():
            status_service.add_status(form_add_status.item_status.data)
            form_add_status.item_status.data = ''
            flash('Статус успешно добавлен')
            return redirect(url_for('admin_panel'))
            
        if form_add_vendor.submit_vendor.data and form_add_vendor.validate_on_submit():
            device_service.add_vendor(form_add_vendor.item_vendor.data)
            form_add_vendor.item_vendor.data = ''
            flash('Вендор успешно добавлен')
            return redirect(url_for('admin_panel'))
            
        if form_add_device.submit_device.data and form_add_device.validate_on_submit():
            device_service.add_device(form_add_device.item_device.data, form_add_device.vendor_id.raw_data[0])
            form_add_device.item_device.data = ''
            flash('Устройство успешно добавлено')
            return redirect(url_for('admin_panel'))
        
        if form_add_source.submit_source.data and form_add_source.validate_on_submit():
            source_service.add_source(form_add_source.item_source.data)
            form_add_source.item_source.data = ''
            flash('Вендор успешно добавлен')
            return redirect(url_for('admin_panel'))
            
        return render_template('admin.html', 
                        form_add_status=form_add_status,
                        form_add_device=form_add_device,
                        form_add_vendor=form_add_vendor,
                        form_add_source=form_add_source,
                        devices=devices,
                        vendors=vendors,
                        statuses=statuses, 
                        sources=sources,
                        users=users
                        )
        
class AdminViewDeviceDelete(View):
    
    methods = ['POST', 'GET']
    
    def dispatch_request(self):
        if request.method == 'POST':
            device_service = DeviceService()
            device_service.delete_device(request.form['id'])
        return redirect(url_for('admin_panel'))
    
class AdminViewSourceDelete(View):
    
    methods = ['POST', 'GET']
    
    def dispatch_request(self):
        if request.method == 'POST':
            source_service = SourceService()
            source_service.delete_source(request.form['id'])
        return redirect(url_for('admin_panel'))

class AdminViewStatusDelete(View):
    
    methods = ['POST', 'GET']
    
    def dispatch_request(self):
        if request.method == 'POST':
            status_service = StatusService()
            status_service.delete_status(request.form['id'])
        return redirect(url_for('admin_panel'))
            
class AdminViewVendorDelete(View):
    
    methods = ['POST', 'GET']
    
    def dispatch_request(self):
        if request.method == 'POST':
            status_service = DeviceService()
            status_service.delete_vendor(request.form['id'])
        return redirect(url_for('admin_panel'))


class RequestView(View):
    
    methods = ['GET', 'POST']
    
    def dispatch_request(self, request_id):
        
        request_service = RequestService()
        data = request_service.get_request(request_id)
        form = RequestForm()
        comment_form = CommentForm()
        form.address.data = data.address
        form.name.data = data.name
        form.phone.data = data.phone
        form.source.data = data.source_id
        form.coordinates.data = data.coordinates
        form.status.data=data.status
        
        return render_template('show_request.html', data=data, form=form, comments=data.comments, comment_form=comment_form)


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
        form = RequestForm()
        current_request = request_service.get_request(request_id)
        if form.validate_on_submit():
            request_service.edit_request(request_id, form)
            
            return redirect(url_for('request_item', request_id=request_id))
        elif request.method == 'GET':
            form.address.data = current_request.address
            form.name.data = current_request.name
            form.phone.data = current_request.phone
            form.source.data=current_request.source
            form.base.data=current_request.base
            form.device.data=current_request.device
            form.auth_type.data=current_request.auth_type
            form.coordinates.data = current_request.coordinates
            form.status.data=current_request.status
            
            return render_template('edit.html', form=form)
        return redirect(url_for('show_request', request_id=request_id))
    
class AddCommentView(View):
    
    methods = ['POST']

    def dispatch_request(self):
        comment_form = CommentForm()
        comment_service = CommentService()
        if comment_form.validate_on_submit():
            comment_service.add_comment(comment_form.request_id.data,
                                        comment_form.author_id.data,
                                        comment_form.comment_text.data
                                        )
            return redirect(url_for('request_item', request_id=comment_form.request_id.data))
        else:
            return redirect(url_for('index'))