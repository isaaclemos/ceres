import os
from base64 import b64encode

from requests import post

os.chdir(f'{os.path.dirname(__file__)}/images')


with open('10-11-2017_20-00_mediana.jpg', 'rb') as file:
    content = file.read()
    b64 = b64encode(content).decode()
    json = {
        'mac_address': '24:F5:AA:5F:5A:34',        
            'file': b64,
            'format': 'jpg',       
        'datetime':  '2017-11-10 20:00:00'
    }
    resp = post(url='http://127.0.0.1:5000/receive', json=json)

    print(resp)
