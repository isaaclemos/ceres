import os
from base64 import b64encode

from requests import post

os.chdir(f'{os.path.dirname(__file__)}/station_files')


with open('24:F5:AA:5F:5A:34/2017-11-10 19:00:00.jpg', 'rb') as img_file:

    img_median = b64encode(img_file.read()).decode()
    json = {
        'mac_address': '24:F5:AA:5F:5A:34',
        'img_median': {
            'file': img_median,
            'format': 'jpg'
        },
        'csv_thermal': 'csv_thermal',
        'datetime': '2017-11-10 19:00:00'
    }

    resp = post(url='http://127.0.0.1:5000/receive', json=json)
    print(resp)
