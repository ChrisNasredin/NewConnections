from . import app
from flask import render_template, url_for, flash, redirect, request
from .forms import LoginForm, RegisterForm, StatusForm, NewRequestForm, ChangeRequestForm
from flask_login import current_user, login_user, logout_user
from .services import UserService, RequestService, StatusService
from .views import IndexView, NewRequestView, LoginView, LogoutView, CreateNewUserView, \
    AdminView, RequestView, CRUDRequestView

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/new', view_func=NewRequestView.as_view('new'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/admin/create_user', view_func=CreateNewUserView.as_view('create_user'))
app.add_url_rule('/admin', view_func=AdminView.as_view('admin_panel'))
app.add_url_rule('/request/<request_id>', view_func=AdminView.as_view('request_item'))
app.add_url_rule('/<model>/<request_id>/<crud_action>', view_func=CRUDRequestView.as_view('crud'))

@app.route('/request/<request_id>', methods=['GET','POST'])
def show_request(request_id):
    request_service = RequestService()
    print(request_id)
    data = request_service.get_request(request_id)
    form = ChangeRequestForm()
    form.address.data = data.address
    form.name.data = data.name
    form.phone.data = data.phone
    form.coordinates.data = data.coordinates
    form.status.data=data.status
    return render_template('show_request.html', data=data, form=form)

@app.route('/delete/<request_id>', methods=['GET','POST'])
def del_request(request_id):
    request_service = RequestService()
    request_service.delete_request(request_id=request_id)
    flash(f'Заявка {request_id} удалена', 'success')
    return redirect(url_for('index'))


@app.route('/edit/<request_id>', methods=['GET','POST'])
def edit_request(request_id):
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
        return redirect(url_for('show_request', request_id=request_id))
    elif request.method == 'GET':
        form.address.data = current_request.address
        form.name.data = current_request.name
        form.phone.data = current_request.phone
        form.coordinates.data = current_request.coordinates
        form.status.data=current_request.status
        return render_template('edit.html', form=form)
    return redirect(url_for('show_request', request_id=request_id))