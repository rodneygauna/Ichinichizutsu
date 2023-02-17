'''
    website/models.py
'''

from datetime import datetime
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    '''Queries the user's id for use with LoginManager'''
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    '''SQL Table: users'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(255), nullable=False, default='default_profile.jpg')
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default='Active')
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def check_password(self, password):
        '''Checks the password during login'''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Email: {self.email}"


class Todos(db.Model):
    '''SQL Table: todos'''
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Not Started')
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    # Relationships
    user = db.relationship('Users', backref=db.backref('todos'), lazy=True)

    def __repr__(self):
        return f"Title: {self.title}"
