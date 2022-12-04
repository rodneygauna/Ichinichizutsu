'''
    website/users/forms.py
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from website.models import Users


class RegistrationForm(FlaskForm):
    '''Form - Register User'''
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired(), Length(
        min=6), EqualTo('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField(
        'Confirm Password *', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        '''checks if the email is already in use'''
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered')


class LoginForm(FlaskForm):
    '''Form - Login'''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
