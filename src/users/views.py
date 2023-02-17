'''
    website/users/views.py
'''

from flask import request, redirect, render_template, url_for, Blueprint
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from src.models import Users
from src.users.forms import RegistrationForm, LoginForm
from src import db


users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    '''Route: Login page'''
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = request.args.get('next')

            return redirect(next or url_for('core.todos'))

    return render_template('login.html', title='Ichi-Nichi Zutsu', form=form)


@users.route('/logout')
def logout():
    '''Route: Loggs out the user'''
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    '''Route: Registration page'''
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if user:
            print('Email already in use')
        else:
            new_user = Users(email=email,
                             password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('core.index'))

    return render_template('register.html', title='Register', form=form)
