from inmetpy.stations import InmetStation

cod_estacoes = ["A840"]

def get_inmet_data(date, time,cod_station):
    inmet = InmetStation()    
    
    data = inmet.get_data_station(date, date, 'hour', [cod_station])    

    filter={}

    for index, row in data.iterrows():
        if str(row['DATETIME']).__contains__(time):
            filter = {'temp': row['TEMP'], 'vento': row['WSPD']}
    return filter
