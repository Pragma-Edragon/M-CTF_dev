from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Data required')])
    password = PasswordField('Password', validators=[DataRequired(message='Data required')])
    submit = SubmitField('Sign in')


class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Data required')])
    password = PasswordField('Password', validators=[
        DataRequired(message='Data required'),
        EqualTo('copy_password', message='Passwords must match'),
        Length(min=6, max=32, message="Password length must be between [6] and [32]")])
    copy_password = PasswordField('Repeat Password')
    submit = SubmitField('Sign up')


class AnswersForm(FlaskForm):
    answer = StringField('answer', validators=[DataRequired(message='Data required')])
    submit = SubmitField('Send to server')
