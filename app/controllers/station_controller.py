from datetime import date

from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user

from app.ext.database import db
from app.models import Station, User


class StationController:

    def station(self):

        stations = current_user.stations
        return render_template('user/station.html', title='Estações', stations=stations, date=date.today())

    def stations_by_user(self, user_id):

        user = User.query.get(user_id)
        
        if user:
            return render_template('admin/station.html', title='Estações', stations=user.stations, user=user)
        else:
            return redirect(url_for('admin.user_show'))

    def create(self, user_id):

        self.create_station(self, user_id=user_id)

        return redirect(url_for('admin.stations_by_user', user_id=user_id))

    def delete(self, id):

        station = Station.query.get(id)
        user_id = station.user_id

        db.session.delete(station)
        db.session.commit()

        return redirect(url_for('admin.stations_by_user', user_id=user_id))

    def edit(self, id, user_id):

        station = Station.query.filter_by(id=id, user_id=user_id).first()
        if station:
            return render_template('admin/form_station.html', title='Estação', station=station)
        else:
            return redirect(url_for('admin.stations_by_user', user_id=user_id))

    def update(self, id):

        station = self.create_station(id=id, update=True)

        return redirect(url_for('admin.stations_by_user', station_id=id, user_id=station.user_id))

    def create_station(self, id, user_id=None, update=False):

        mac_address = request.form.get('mac_address').upper()
        altitude = request.form.get('altitude')
        altura = request.form.get('altura')
        altura_dossel = request.form.get('altura_dossel')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        cod_inmet = request.form.get('cod_inmet').upper()

        if update:
            station = Station.query.get(id)
        else:
            station = Station.query.filter_by(mac_address=mac_address).first()

        if station and not update:
            flash('Erro! estação ja cadastrda!', 'error')
        elif len(mac_address) != 17:
            flash('Erro! MAC Address invalido', 'error')

        elif len(cod_inmet) < 1:
            flash('Erro! Codigo INMET invalido', 'error')
        elif not self.is_number(altitude):
            flash('Erro! Os valores de altitude é numerico', 'error')
        elif not self.is_number(altura):
            flash('Erro! Os valores de altura é numerico', 'error')
        elif not self.is_number(altura_dossel):
            flash('Erro! Os valores de altura dossel é numerico', 'error')
        elif not self.is_number(latitude):
            flash('Erro! Os valores de latitude é numerico', 'error')
        elif not self.is_number(longitude):
            flash('Erro! Os valores de logitude é numerico', 'error')
        else:
            if not update:
                station = Station()
                station.user_id = user_id
                db.session.add(station)
                flash('Estação cadastrado com sucesso!', 'sucess')
            else:
                flash('Estação atualizada com sucesso!', 'sucess')
            
            station.mac_address = mac_address
            station.altitude = altitude
            station.altura = altura
            station.altura_dossel = altura_dossel
            station.latitude = latitude
            station.longitude = longitude
            station.cod_inmet = cod_inmet

            db.session.commit()

        return station

    def is_number(self, value: str):
        is_number = False
        try:
            float(value)
            is_number = True
        except:
            pass
        return is_number
