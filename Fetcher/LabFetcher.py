import csv
import json
import requests


lab_url = 'http://od.cdc.gov.tw/icb/%E6%8C%87%E5%AE%9A%E6%8E%A1%E6%AA%A2%E9%86%AB%E9%99%A2%E6%B8%85%E5%96%AE.csv'
lab_json_path = './datasets/covid19_labs.json'
lab_json = {}
json_keys = [
    'gency_code',
    'area',
    'county',
    'admin_district',
    'agency_name',
    'address',
    'phone_number',
    'longitude',
    'latitude',
]

def fetch_labs():
    response = requests.get(lab_url)
    response.encoding = 'utf-8'
    contents = response.text.split('\n')[1:-1]
    for content in contents:
        line = list(csv.reader([content]))[0]
        lab_json[line[0]] = {
            'gency_code': line[0],
            'area': line[1],
            'county': line[2],
            'admin_district': line[3],
            'agency_name': line[4],
            'address': line[5],
            'phone_number': line[6],
            'longitude': line[7],
            'latitude': line[8],
        }

fetch_labs()

lab_json_string = json.dumps(lab_json)
file_handler = open(lab_json_path, 'w')
file_handler.write(lab_json_string + '\n')
file_handler.close()

print('Store ' + lab_json_path + ' has been done.')
