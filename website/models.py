from werkzeug.security import check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from website import db, SECRET_KEY


class Users(db.Model, UserMixin):
    '''SQL Table: users'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(255), nullable=False, default='default_profile.jpg')

    # Data Points - Login
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(128), nullable=False)

    # Data Points - Main
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default='Active')
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Password Hash Check

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # For Reset/Forgot Password
    def get_token(self, expires_sec=900):
        serial = Serializer(SECRET_KEY, expires_in=expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(SECRET_KEY)
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # Represent
    def __repr__(self):
        return f"Email: {self.email}"
