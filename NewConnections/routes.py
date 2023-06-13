from . import app
from flask import render_template, url_for, flash, redirect, request
from .forms import LoginForm, RegisterForm, StatusForm, NewRequestForm, ChangeRequestForm
from flask_login import current_user, login_user, logout_user
from .services import UserService, RequestService, StatusService
from .views import IndexView, NewRequestView, LoginView, LogoutView, CreateNewUserView, \
    AdminView, RequestView, DeleteRequestView, EditRequestView

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/new', view_func=NewRequestView.as_view('new'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/admin/create_user', view_func=CreateNewUserView.as_view('create_user'))
app.add_url_rule('/admin', view_func=AdminView.as_view('admin_panel'))
app.add_url_rule('/request/<request_id>', view_func=RequestView.as_view('request_item'))
app.add_url_rule('/request/delete/<request_id>', view_func=DeleteRequestView.as_view('delete_request'))
app.add_url_rule('/request/edit/<request_id>', view_func=EditRequestView.as_view('edit_request'))