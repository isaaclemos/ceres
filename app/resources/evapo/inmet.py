from inmetpy.stations import InmetStation
from datetime import datetime

cod_estacoes = "A840"

def get_inmet_data(date_time: datetime, cod_station: str):
    inmet = InmetStation()    
    
    data = inmet.get_data_station(str(date_time.date()), str(date_time.date()), 'hour', [cod_station])    

    filter={}

    for index, row in data.iterrows():
        if str(row['DATETIME']).__contains__(date_time.time()):
            filter = {'temp': row['TEMP'], 'vento': row['WSPD']}
    return filter
