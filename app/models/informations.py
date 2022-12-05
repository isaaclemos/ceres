from app.ext.database import db

class Information(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False) 
    datetime = db.Column(db.DateTime, nullable=False)
    min = db.Column(db.Numeric, nullable=False)
    max = db.Column(db.Numeric, nullable=False)
    mean = db.Column(db.Numeric, nullable=False)
    median = db.Column(db.Numeric, nullable=False)
    std = db.Column(db.Numeric, nullable=False)
    var = db.Column(db.Numeric, nullable=False)
    csv_file = db.Column(db.String, nullable=False)
    img_file = db.Column(db.String, nullable=False)
    


