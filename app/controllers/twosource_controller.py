import os
from base64 import b64decode
from datetime import datetime

import numpy as np
from flask import make_response, request

from app.ext.database import db
from app.models import Information, Station
from app.resources.evapo.et import two_source_model
from app.resources.evapo.inmet import get_inmet_data
from app.resources.evapo.sun import solar_position


class TwosourceController:
    
    def api_v1(self):

        # JSON struct from POST
        # {'mac_address':'','img_median':{'file':'','format': ''},'csv_thermal':'','datetime':''}

        mac_address = request.json['mac_address']

        station = Station.query.filter_by(mac_address=mac_address).first()

        if station:
            path =f'{os.path.abspath(os.curdir)}/app/resources/station_files/{mac_address}'

            json = request.json

            if not os.path.exists(path):
                os.makedirs(path)

            timedate = datetime.strptime(json['datetime'], '%Y-%m-%d %H:%M:%S')

            file_name = f"{timedate}.{json['img_median']['format']}"
            
            with open(f'{path}/{file_name}', 'wb') as img_file:
                img_file.write(b64decode(json['img_median']['file']))
                img_file.close()

            data_inmet = get_inmet_data(
                date=str(timedate.date()), time=str(timedate.time()), cod_station=station.cod_inmet)
        

            sun_values = solar_position(timedate.month, timedate.day, timedate.year,
                                        timedate.hour, timedate.minute, station.latitude, station.longitude)

            et = two_source_model(image=file_name, station=station, sun_values=sun_values,
                                vento=data_inmet['vento'], temp_kelvin=(273.15+data_inmet['temp']))

            info = Information(station_id=station.id, date=timedate.date(), time=timedate.time(), min=np.nanmin(et), max=np.nanmax(et),
                            std=np.nanstd(et), mean=np.nanmean(et),  var=np.nanvar(et),  median=np.nanmedian(et))
            info.img_file = file_name
            info.csv_file = file_name

            db.session.add(info)
            db.session.commit()

            return make_response('{}', 200)
        else:
            return make_response('', 400)
