from flask_login import UserMixin

from app.ext.database import db


class Station(db.Model, UserMixin):    
       
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mac_address = db.Column(db.String, nullable=False, unique=True) 
    altitude = db.Column(db.Numeric(scale=2), nullable=False)
    altura = db.Column(db.Numeric(scale=2), nullable=False)
    altura_dossel = db.Column(db.Numeric(scale=2), nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    cod_inmet = db.Column(db.String, nullable=False)    
    


        