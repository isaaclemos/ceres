import os
from base64 import b64encode

from requests import post

os.chdir('/home/isaac/ceres1')


with open('2022-12-15 19:00_median.jpg', 'rb') as img_file:

    img_median = b64encode(img_file.read()).decode()
    json = {
        'mac_address': 'B8:27:EB:ED:FE:11',
        'img_median': {
            'file': img_median,
            'format': 'jpg'
        },
        'csv_thermal': '',
        'datetime': '2022-12-15 19:00:00'
    }

    resp = post(url='http://localhost:5000/api/v1', json=json)
    print(resp)
