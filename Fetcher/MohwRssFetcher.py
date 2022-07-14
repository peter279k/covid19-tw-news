import os
import json
import requests
from xml.dom import minidom


rss_url = 'https://www.mohw.gov.tw/rss-16-1.html'

json_file_name = './datasets/mohw_rss.json'
response = requests.get('https://github.com/peter279k/covid19-tw-news/raw/master/datasets/mohw_rss.json')
file_handler = open(json_file_name, 'w')
file_handler.write(response.text)
file_handler.close()


def fetch_mohw_rss():
    response = requests.get(rss_url, verify=False)
    response.encoding = 'urf-8'
    return response.text

rss_text = fetch_mohw_rss()
json_dict = {}
xml_parser = minidom.parseString(rss_text)
item_lists = xml_parser.getElementsByTagName('item')

index = len(item_lists)
for item in item_lists:
    title = item.getElementsByTagName('title')[0].firstChild.nodeValue
    link = item.getElementsByTagName('link')[0].firstChild.nodeValue
    description = item.getElementsByTagName('description')[0].firstChild.nodeValue
    news_id = item.getElementsByTagName('NewsID')[0].firstChild.nodeValue
    department_name = item.getElementsByTagName('DeptName')[0].firstChild.nodeValue
    pub_date = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue
    json_dict[pub_date + news_id] = {
        'index': index,
        'news_id': 'modal_' + news_id,
        'modal_news_id': '#modal_' + news_id,
        'pub_date': pub_date,
        'title': title,
        'link': link,
        'description': description,
        'department_name': department_name,
    }
    index -= 1

original_json_text = ''
if os.path.isfile(json_file_name) is True:
    file_handler = open(json_file_name, 'r')
    original_json_text = file_handler.read()
    file_handler.close()

if len(original_json_text) != 0:
    original_json_object = json.loads(original_json_text)
    for json_dict_key in list(json_dict.keys()):
        if json_dict_key not in list(original_json_object.keys()):
            original_json_object[json_dict_key] = dict(json_dict[json_dict_key])
    json_dict = dict(original_json_object)

json_text = json.dumps(json_dict)
file_handler = open(json_file_name, 'w')
file_handler.write(json_text)
file_handler.close()

print('Storing ' + json_file_name + ' has been done.')
