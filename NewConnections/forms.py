from flask_wtf import FlaskForm, Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from wtforms_alchemy import QuerySelectMultipleField, QuerySelectField
from.models import Roles, Statuses
from .services import StatusService, UserService, DeviceService


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

class RegisterForm(FlaskForm):
    
    user_service = UserService()
    
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторить пароль', validators=[DataRequired(), EqualTo('password')])
    role = QuerySelectField(query_factory=user_service.get_roles, 
                            allow_blank=False, 
                            label='Права')
    submit = SubmitField('Регистрация')
     
class AddItemForm(FlaskForm):
    pass
    
class AddStatusForm(AddItemForm):
    item_status = StringField('Добавить новый:', validators=[DataRequired()])
    submit_status = SubmitField('Добавить')
    
class AddVendorForm(AddItemForm):
    item_vendor = StringField('Добавить новый:', validators=[DataRequired()])
    submit_vendor = SubmitField('Добавить')
    
class DeviceForm(FlaskForm):
    device_service = DeviceService()
    item_device = StringField('Название устройства', validators=[DataRequired()])
    vendor_id = QuerySelectField(query_factory=device_service.get_all_vendors,
                                 allow_blank=True, 
                                 label='Вендор')
    submit_device = SubmitField('Добавить устройство')
    
class VendorForm(FlaskForm):
    vendor_name = StringField('Имя вендора', validators=[DataRequired()])
    submit = SubmitField('Добавить вендора')
    
class NewRequestForm(FlaskForm):
    address = StringField('Адрес подключения', validators=[DataRequired()])
    name = StringField('ФИО', validators=[DataRequired()])
    coordinates = StringField('Координаты')
    phone = StringField('Телефон', validators=[DataRequired()])
    device = StringField('Оборудование')
    base = StringField('Базовая станция')
    auth = StringField('Тип Авторизации')
    submit = SubmitField('Создать')

class ChangeRequestForm(FlaskForm):
    
    status_service = StatusService()
    
    address = StringField('Адрес подключения', validators=[DataRequired()])
    name = StringField('ФИО', validators=[DataRequired()])
    coordinates = StringField('Координаты')
    phone = StringField('Телефон', validators=[DataRequired()]) 
    status = QuerySelectField(query_factory=status_service.get_statuses,
                              allow_blank=False,
                              label='Статус')
    submit = SubmitField('Изменить')
    
class CommentForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit_comment = SubmitField('Отправить комментарий')