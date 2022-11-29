from inmetpy.stations import InmetStation


inmet = InmetStation()
# Dia da a q u i s i c a o da imagem
data_ini = "2017-10-11"
data_fim = "2017-10-11"
ordem = "hour"
# Parametro inserido ao cadastrar uma estacao de captura dos dados
cod_estacoes = ["A840"]
# E gerado um dataframe com todos os dados das estacoes
dados = inmet.get_data_station(data_ini, data_fim, ordem, cod_estacoes)
print(dados['TEMP'])
