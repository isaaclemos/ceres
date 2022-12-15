import os
from base64 import b64decode
from datetime import datetime

from flask import make_response, request

from app.ext.database import db
from app.models import Information, Station
from app.resources.evapo.et import two_source_model
from app.resources.evapo.inmet import get_inmet_data
from app.resources.evapo.sun import solar_position


class TwosourceController:

    def api_v1(self):

        json_pattern = {'mac_address': '', 'img_median': {
            'file': '', 'format': ''}, 'csv_thermal': '', 'datetime': ''}

        mac_address = request.json['mac_address'].upper()

        station = Station.query.filter_by(mac_address=mac_address).first()

        if station:
            path = os.path.abspath("station_files")
            
            json = request.json

            date_time = datetime.fromisoformat(json['datetime'])

            file_name = f"{mac_address} {date_time}.{json['img_median']['format']}"

            with open(f'{path}/{file_name}', 'wb') as img_file:
                img_file.write(b64decode(json['img_median']['file']))
                img_file.close()

            data_inmet = get_inmet_data(date_time=date_time, cod_station=station.cod_inmet)

            sun_values = solar_position(date_time, station.latitude, station.longitude)

            et = two_source_model(image=f'{path}/{file_name}', station=station, sun_values=sun_values,
                                  vento=data_inmet['vento'], temp_kelvin=(273.15+data_inmet['temp']))

            info = Information(station_id=station.id, date_time=date_time, et=et)
            info.img_file = file_name
            info.csv_file = file_name

            db.session.add(info)
            db.session.commit()

            return make_response('{}', 200)
        else:
            return make_response(json_pattern, 400)
    

