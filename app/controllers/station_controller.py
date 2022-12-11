from datetime import date

from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user

from app.ext.database import db
from app.models import Station, User


class StationController:    
    
    def station(self):
        
        stations = current_user.stations
        
        return render_template('user/station.html', title='Estações', stations=stations, date=date.today())
    
    def stations_by_user(self,user_id):
        
        user = User.query.get(user_id)
        
        return render_template('admin/station.html', title='Estações', stations=user.stations, user=user)

    def create(self,user_id):

        station = Station()
        station.user_id = user_id
        station.mac_address = request.form.get('mac_address')
        station.altitude = request.form.get('altitude')
        station.altura = request.form.get('altura')
        station.altura_dossel = request.form.get('altura_dossel')
        station.latitude = request.form.get('latitude')
        station.longitude = request.form.get('longitude')
        station.cod_inmet = request.form.get('cod_inmet')
        
        if Station.query.filter_by(mac_address = station.mac_address).first():
            flash('Erro! estação ja cadastrda!','error')
        else:
            db.session.add(station)
            db.session.commit()
            flash('Estação cadastrado com sucesso!','sucess')

        return redirect(url_for('admin.stations_by_user', user_id=user_id))

    def delete(self, id):
        
        station = Station.query.get(id)
        user_id=station.user_id
                
        db.session.delete(station)
        db.session.commit()

        return redirect(url_for('admin.stations_by_user', user_id=user_id))
    
    def edit(self, id):                
        
        station = Station.query.get(id)
        
        return render_template('admin/form_station.html', title='Estação', station=station)
    
    def update(self, id):        
        station = Station.query.get(id)        
        station.mac_address = request.form.get('mac_address')
        station.altitude = request.form.get('altitude')
        station.altura = request.form.get('altura')
        station.altura_dossel = request.form.get('altura_dossel')
        station.latitude = request.form.get('latitude')
        station.longitude = request.form.get('longitude')
        station.cod_inmet = request.form.get('cod_inmet')        
        
        db.session.commit()
                
        flash('Estação atualizada com sucesso!','sucess')
                
        return redirect(url_for('admin.stations_by_user', station_id=id, user_id=station.user_id))
    
 
        
