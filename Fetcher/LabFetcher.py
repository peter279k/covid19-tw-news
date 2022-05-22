import csv
import json
import requests


lab_url = 'https://od.cdc.gov.tw/icb/%E6%8C%87%E5%AE%9A%E6%8E%A1%E6%AA%A2%E9%86%AB%E9%99%A2%E6%B8%85%E5%96%AE.csv'
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
    response = requests.get(lab_url, verify=False)
    response.encoding = 'big5-hkscs'
    contents = response.text.split('\n')[1:-1]
    counter = 0
    missed = ''
    missed_index = 1

    for content in contents:
        line = list(csv.reader([content]))[0]
        if len(line) < 9:
            missed += ','.join(line)
            if missed_index % 2 == 0:
                missed += '\n'
            missed_index += 1
            continue
        lab_json[str(counter)] = {
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
        counter += 1

    for missed_str in missed.split('\n'):
        line = list(csv.reader([missed_str]))[0]
        if len(line) == 0:
            continue
        lab_json[str(counter)] = {
            'gency_code': line[0],
            'area': line[1],
            'county': line[2],
            'admin_district': line[3],
            'agency_name': line[4],
            'address': line[5],
            'phone_number': line[6].replace('\\', ''),
            'longitude': line[7],
            'latitude': line[8],
        }
        counter += 1

fetch_labs()

lab_json_string = json.dumps(lab_json)
file_handler = open(lab_json_path, 'w')
file_handler.write(lab_json_string + '\n')
file_handler.close()

print('Store ' + lab_json_path + ' has been done.')
