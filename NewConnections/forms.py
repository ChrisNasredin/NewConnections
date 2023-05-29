from flask_wtf import FlaskForm, Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms_alchemy import ModelForm, ModelFieldList
from .models import Users, Roles
from wtforms.fields import FormField

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

# class RegisterForm(FlaskForm):
#     username = StringField('Имя пользователя', validators=[DataRequired()])
#     password = PasswordField('Пароль', validators=[DataRequired()])
#     password2 = PasswordField('Повторить пароль'validators=[DataRequired(), EqualTo('password')])
#     role = 
#     submit = SubmitField('Регистрация')

class RegisterForm(ModelForm, FlaskForm):
    class Meta:
        model = Users
        exclude = ['password_hash']
    role = ModelFieldList(FormField(Roles))