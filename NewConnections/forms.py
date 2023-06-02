from flask_wtf import FlaskForm, Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from wtforms_alchemy import QuerySelectMultipleField, QuerySelectField
from.models import Roles, Statuses


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

class RegisterForm(FlaskForm):
     username = StringField('Имя пользователя', validators=[DataRequired()])
     password = PasswordField('Пароль', validators=[DataRequired()])
     password2 = PasswordField('Повторить пароль', validators=[DataRequired(), EqualTo('password')])
     role = QuerySelectField(query_factory=Roles.choice_roles, 
                            allow_blank=False, 
                            label='Права'
                            )
     submit = SubmitField('Регистрация')
     
class StatusForm(FlaskForm):
    status_desc = StringField('Новый статус:', validators=[DataRequired()])
    submit = SubmitField('Добавить статус')
    
class NewRequestForm(FlaskForm):
    address = StringField('Адрес подключения', validators=[DataRequired()])
    name = StringField('ФИО', validators=[DataRequired()])
    coordinates = StringField('Координаты')
    phone = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Создать')

class ChangeRequestForm(FlaskForm):
    address = StringField('Адрес подключения', validators=[DataRequired()])
    name = StringField('ФИО', validators=[DataRequired()])
    coordinates = StringField('Координаты')
    phone = StringField('Телефон', validators=[DataRequired()])
    status = QuerySelectField(query_factory=Statuses.get_statuses,
                              allow_blank=False,
                              label='Статус')
    submit = SubmitField('Изменить')