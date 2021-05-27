import json
import requests
from xml.dom import minidom

rss_url = 'https://www.mohw.gov.tw/rss-16-1.html'
json_file_name = './datasets/mohw_rss.json'

def fetch_mohw_rss():
    response = requests.get(rss_url)
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

json_text = json.dumps(json_dict)
file_handler = open(json_file_name, 'w')
file_handler.write(json_text)
file_handler.close()

print('Storing ' + json_file_name + ' has been done.')
