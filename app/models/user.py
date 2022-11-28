from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.ext.database import db


class User(db.Model, UserMixin):    
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    user_name = db.Column(db.String, nullable=False) 
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    stations = db.relationship('Station')

    def __init__(self, email, user_name, password, is_admin=False):
        self.email = email
        self.user_name = user_name
        self.set_password(password)
        self.is_admin = is_admin
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)