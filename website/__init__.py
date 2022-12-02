from flask import Flask, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from os import path, getenv

db = SQLAlchemy()
DB_NAME = "database.db"

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


def create_app():
    '''Initializes  the application using Flask'''
    app = Flask(__name__)
    # Flask secret key configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    # Flask and SQLAlchemy database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Check if database exists; if not, create database and tables (as classes)
    from .models import Users
    create_database()

    # Initializes the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.login_message = u'You have to login to view this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('users.login'))

    return app


# ------------------------------------------------------------------------------
# Database initialization
# ------------------------------------------------------------------------------
def create_database():
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created database!')
