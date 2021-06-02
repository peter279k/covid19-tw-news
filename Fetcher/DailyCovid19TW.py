import csv
import json
import requests


url = 'https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.csv'

def fetch_daily_covid19():
    response = requests.get(url)
    response.encoding = 'utf-8'
    csv_string = response.text
    csv_rows = csv_string.split('\n')[0:-1]

    json_obj = {}
    index = '0'
    for csv_row in csv_rows:
        csv_row_arr = csv.reader(csv_row[0:-1], delimiter=',')
        tmp = ''
        tmp_row_arr = []
        for column in csv_row_arr:
            if len(column) == 2 and column[0] == '' and column[0] == '':
                tmp_row_arr.append(tmp)
                tmp = ''
            tmp += column[0]

        if tmp == '':
            tmp = '0'
        tmp_row_arr.append(tmp)
        json_obj[index] = tmp_row_arr
        index = str(int(index) + 1)

    return json_obj

json_obj = fetch_daily_covid19()
json_file_path = './datasets/DayConfirmationAgeCountyGender19CoV.json'

file_handler = open(json_file_path, 'w')
json_str = json.dumps(json_obj)
file_handler.write(json_str + '\n')
file_handler.close()

print('Storing ' + json_file_path + ' has been done.')
