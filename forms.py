from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from models import User
from main import *


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        cur.execute("SELECT username FROM username")
        loginList = cur.fetchall()
        for login in loginList:
            if username.data == login[0]:
                raise ValidationError('Please use a different username.')

class RateForm(FlaskForm):
    rate = IntegerField('Rate', validators=[DataRequired()])
    submit = SubmitField('Оценить')