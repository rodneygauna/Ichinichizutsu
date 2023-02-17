'''
    /website/__init__.py
'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from src.users.views import users
from src.core.views import core

app.register_blueprint(core)
app.register_blueprint(users)


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
