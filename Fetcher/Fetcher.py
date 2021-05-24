import os
import re
import json
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup


heho_url = 'https://heho.com.tw/page/page_number/?s=%E5%85%A8%E5%8F%B0%E6%9F%93%E7%96%AB%E8%B6%B3%E8%B7%A1%E4%B8%80%E6%AC%A1%E7%9C%8B+'
keyword = '全台染疫足跡一次看'
footprint_keyword = '確診足跡'
confirmed_back_keyword = '校正回歸'
county_keyword = '雙北市'
footprint_lists = {}
correct_back_number = 0
start_correct_back_date = '2021-05-22'
datetime_format = '%Y-%m-%d'
county_lists = [
    '新北市',
    '臺北市',
    '桃園市',
    '新竹市',
    '新竹縣',
    '苗栗縣',
    '臺中市',
    '彰化縣',
    '雲林縣',
    '嘉義縣',
    '臺南市',
    '高雄市',
    '屏東縣',
    '南投縣',
    '宜蘭縣',
    '花蓮縣',
    '臺東縣',
    '連江縣',
    '澎湖縣',
    '金門縣',
]
removed_indexes = {}

def strip_title(title):
    title = str(title)
    strip_tags = ['\n', '\t', '<h5 class="post-title is-large">', '</h5>']
    for strip_tag in strip_tags:
        title = title.replace(strip_tag, '')

    return title

def strip_link(link):
    strip_tags = ['\n', '\t']
    for strip_tag in strip_tags:
        link['href'] = link['href'].replace(strip_tag, '')

    return link['href']

def check_keyword(title):
    title = str(title)
    return keyword in title

def fetch_date(date):
    pattern = re.compile('(\w+-\w+-\w+)')
    matched_date = pattern.findall(date.text)[0]

    return matched_date

def fetch_daily_footprint():
    page = 1
    while True:
        global correct_back_number
        response = requests.get(heho_url.replace('page_number', str(page)))
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.select('h5[class="post-title is-large"]')
        dom_links = soup.select('div[class="col post-item"] a')

        check_keyword_result = list(map(check_keyword, titles))
        if check_keyword_result.count(True) == 0:
            break

        titles = list(map(strip_title, titles))
        links = list(map(strip_link, dom_links))

        soup = BeautifulSoup(str(dom_links), 'html.parser')
        dates = soup.select('p[style="font-size: .5em;margin-bottom: 1em;"]')
        dates = list(map(fetch_date, dates))

        global removed_indexes
        for date in dates:
            removed_indexes[date] = []

        for index,date in enumerate(dates):
            if keyword not in titles[index]:
                continue
            texts = fetch_confirmed_case_texts(links[index])
            confirmed_counts = fetch_confirmed_counts(texts, date)
            confirmed_total_counts = sum(confirmed_counts)
            new_texts = []
            for index_text,case_text in enumerate(texts):
                if index_text in removed_indexes[date]:
                    continue
                new_texts.append(case_text)

            footprint_lists[date] = {
                'index': index + 1,
                'date': date,
                'link': links[index],
                'modal': '#Modal' + date.replace('-', ''),
                'modal_id': 'Modal' + date.replace('-', ''),
                'title': titles[index][5:],
                'confirmed_case_texts': new_texts,
                'confirmed_counts': confirmed_counts,
                'confirmed_total_counts': confirmed_total_counts,
            }
        page += 1

def fetch_confirmed_case_texts(link):
    response = requests.get(link)
    if confirmed_back_keyword in response.text:
        fetch_confirmed_back_case_texts(response.text)
    else:
        global correct_back_number
        correct_back_number = 0
    soup = BeautifulSoup(response.text, 'html.parser')
    confirmed_case_texts = soup.select('span[style="color: #3a7a3b;"] > strong')
    confirmed_list_texts = soup.select('div[class="entry-content single-page"] > ul > li')
    if len(confirmed_list_texts) != 0:
        confirmed_case_texts = list(confirmed_list_texts)

    news_texts = []
    result_texts = list(map(fetch_case_text, confirmed_case_texts))
    global county_lists
    is_county = False
    for result_text in result_texts:
        for county_name in county_lists:
            if county_name in result_text:
                is_county = True
                break

        if is_county is False:
            continue

        if county_keyword in result_text:
            tmp_arr = result_text.split('、')
            news_texts.append(tmp_arr[0])
            news_texts.append(tmp_arr[1])
        else:
            news_texts.append(result_text)

    return news_texts

def fetch_confirmed_back_case_texts(response_contents):
    soup = BeautifulSoup(response_contents, 'html.parser')
    confirmed_back_case_texts = soup.select('div[class="entry-content single-page"] > p')
    splitted_text = confirmed_back_case_texts[0].text.split(confirmed_back_keyword)[0]
    confirmed_number_pattern = re.compile('\d+')
    global correct_back_number
    correct_back_number = int(confirmed_number_pattern.findall(splitted_text)[-1])

def fetch_confirmed_counts(texts, date):
    global removed_indexes
    text_lists = list(map(fetch_confirmed_number, texts))
    result = []
    for index,number in enumerate(text_lists):
        if number == 0:
            removed_indexes[date].append(index)
            continue
        result.append(number)

    return result

def fetch_confirmed_number(text):
    if text[-1] != '例' and '最多' not in text and '為多' not in text:
        return 0
    confirmed_number_pattern = re.compile('\d+')
    matched_result = confirmed_number_pattern.findall(text)
    if len(matched_result) == 0:
        return 0
    return int(matched_result[0])

def fetch_case_text(strong_texts):
    return strong_texts.text

fetch_daily_footprint()

dataset_dir = './datasets'
json_file_path = '%s/covid19_data.json' % (dataset_dir)
if os.path.isdir(dataset_dir) is False:
    print('This ' + dataset_dir + ' directory is not existed!')
    exit()

file_handler = open(json_file_path, 'w')
file_handler.write(json.dumps(footprint_lists) + '\n')
file_handler.close()

print(json_file_path + ' has been stored.')
