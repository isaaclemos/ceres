from app.ext.database import db
import numpy as np

class Information(db.Model):    
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False) 
    date_time = db.Column(db.DateTime, nullable=False)
    min = db.Column(db.Numeric, nullable=False)
    max = db.Column(db.Numeric, nullable=False)
    mean = db.Column(db.Numeric, nullable=False)
    median = db.Column(db.Numeric, nullable=False)
    std = db.Column(db.Numeric, nullable=False)
    var = db.Column(db.Numeric, nullable=False)
    csv_file = db.Column(db.String, nullable=False)
    img_file = db.Column(db.String, nullable=False)
    station = db.relationship('Station')

    def __init__(self,station_id, date_time, et) -> None:
        self.station_id=station_id
        self.date_time = date_time
        self.min=np.nanmin(et)
        self.max=np.nanmax(et)
        self.std=np.nanstd(et)
        self.mean=np.nanmean(et)
        self.var=np.nanvar(et)
        self.median=np.nanmedian(et)

