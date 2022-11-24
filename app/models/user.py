from app.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):    
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    user_name = db.Column(db.String, nullable=False) 
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    stations = db.relationship('Station')