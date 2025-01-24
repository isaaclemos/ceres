# Sistema Web de Código Aberto para Estimativa de Evapotranspiração

Este projeto é o resultado de um Trabalho de Conclusão de Curso (TCC) que desenvolve um sistema web de código aberto para monitoramento contínuo da evapotranspiração. O sistema foi projetado para ser uma ferramenta acessível, de baixo custo e adaptável, especialmente voltada para pequenos e médios produtores agrícolas.

## Objetivo

Criar um sistema que permita o monitoramento em tempo real da evapotranspiração, utilizando dados capturados por sensores termais e de infravermelho próximo, processados em um servidor web e disponibilizados via interface web.

## Funcionalidades

- Monitoramento em tempo real da evapotranspiração.
- Integração com sensores Raspberry Pi NoIR e Flir Lepton 3.
- Processamento dos dados utilizando o Modelo de Duas Fontes (TSM).
- Armazenamento em banco de dados PostgreSQL.
- Interface web para consulta de dados gráficos e estatísticos.
- Suporte a diferentes estações de captura conectadas via Internet.

## Tecnologias Utilizadas

### Hardware
- **Raspberry Pi 3**: Unidade de processamento.
- **Câmeras**: Raspberry Pi NoIR e Flir Lepton 3.

### Software
- **Linguagem de Programação**: Python.
- **Framework Web**: Flask.
- **Bibliotecas**:
  - Flask-Login e Flask-SQLAlchemy.
  - NumPy, Rasterio e Plotly.
  - InmetPy (para dados meteorológicos do INMET).
- **Banco de Dados**: PostgreSQL.

## Estrutura do Sistema

1. **Estação de Captura**: Realiza a aquisição de dados e transmite ao servidor.
2. **Servidor Web**: Processa os dados recebidos, calcula a evapotranspiração e armazena os resultados.
3. **Interface Web**: Permite o acesso remoto às informações armazenadas, com exibição gráfica e tabelas.

## Conclusão

O sistema demonstrou ser uma solução viável para o monitoramento contínuo da evapotranspiração, contribuindo para o manejo eficiente da irrigação e a sustentabilidade dos recursos hídricos. É flexível e pode ser adaptado para diferentes sensores e culturas agrícolas.

## Trabalhos Futuros

- Validação dos dados em ambientes controlados.
- Expansão para áreas agrícolas de grande porte.
- Integração com grids de sensores.
- Desenvolvimento de artigos científicos para divulgação do sistema.

## Como Contribuir

Sinta-se à vontade para colaborar com o projeto. Abra uma issue ou envie um pull request com sugestões ou melhorias.

---

**Desenvolvido por:** Isaac Lemos da Silva  
**Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Sul - Campus Rio Grande**  
**Orientador:** Prof. Luciano Vargas Gonçalves

