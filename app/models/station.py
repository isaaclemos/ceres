from app import db
from flask_login import UserMixin

class Station(db.Model, UserMixin):    
       
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mac_address = db.Column(db.String, nullable=False) 
    altitude = db.Column(db.Numeric(scale=2), nullable=False)
    altura = db.Column(db.Numeric(scale=2), nullable=False)
    altura_dossel = db.Column(db.Numeric(scale=2), nullable=False)
    coordenadas = db.Column(db.String, nullable=False)
    cod_inmet = db.Column(db.String, nullable=False)    
    


        