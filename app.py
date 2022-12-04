'''
    /app.py
'''

import os
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import login_user, LoginManager, UserMixin, logout_user

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'You have to login to view this page'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    '''Queries the user's id for use with LoginManager'''
    user = User.query.get(email)
    user.id = email
    return user


@login_manager.unauthorized_handler
def unauthorized():
    '''If the user isn't authorized, will be redirected to the login page'''
    return redirect(url_for('login'))


@app.cli.command('db_create')
def db_create():
    '''Use "flask db_create" to create the database in the terminal'''
    db.create_all()
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    '''Use "flask db_drop" to drop the database in the terminal'''
    db.drop_all()
    print('Databased dropped')


@app.route('/', methods=['GET'])
def index():
    '''Route: Index page'''
    return render_template('index.html',
                           title='Ichi-Nichi Zutsu')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Route: Login page'''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)

            next = request.args.get('next')

            return redirect(next or url_for('index'))

    return render_template('login.html',
                           title='Ichi-Nichi Zutsu',
                           form=form)


@app.route('/logout')
def logout():
    '''Route: Loggs out the user'''
    logout_user()
    return redirect(url_for('index'))


class LoginForm(FlaskForm):
    '''Form - Login'''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Route: Registration page'''
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            print('Email already in use')
        else:
            new_user = User(email=email,
                            password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('register.html',
                           title='Register',
                           form=form)


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
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered')


class User(db.Model, UserMixin):
    '''SQL Table Model: Users'''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    def check_password(self, password):
        '''Checks the hash of the user's password'''
        return check_password_hash(self.password, password)


if __name__ == '__main__':
    app.run(debug=True)
