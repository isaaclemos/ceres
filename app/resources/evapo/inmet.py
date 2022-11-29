from inmetpy.inmet_stations import InmetStation


inmet = InmetStation()
# Dia da a q u i s i c a o da imagem
data_ini = "2022-6-30"
data_fim = "2022-6-30"
ordem = "hour"
# Parametro inserido ao cadastrar uma estacao de captura dos dados
cod_estacoes = [" A840 "]
# E gerado um dataframe com todos os dados das estacoes
dados = inmet.get_data_station(data_ini, data_fim, ordem, cod_estacoes)
1
