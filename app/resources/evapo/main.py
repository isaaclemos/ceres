import os
from base64 import b64encode

from requests import post

os.chdir(f'{os.path.dirname(__file__)}/original/24:F5:AA:5F:5A:34')


with open('2017-11-10 19:00:00.jpg', 'rb') as img_file:

    img_median = b64encode(img_file.read()).decode()
    json = {
        'mac_address': 'B8:27:EB:ED:FE:11',
        'img_median': {
            'file': img_median,
            'format': 'jpg'
        },
        'csv_thermal': '',
        'datetime': '2017-11-10 11:00:00'
    }

    resp = post(url='https://ceres.up.railway.app/api/v1', json=json)
    print(resp)
