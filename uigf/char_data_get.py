import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
import requests
from bs4 import BeautifulSoup

url = 'https://wiki.biligame.com/ys/%E7%A5%88%E6%84%BF'
respone = requests.get(url)
soup = BeautifulSoup(respone.content, 'html.parser')
sort_contexts = soup.find_all('table', class_="wikitable")
sort_contexts_ = soup.find('table', class_="wikitable")
tables = soup.find_all('table', class_=lambda x: x and 'wikitable' in x.split())
sort_tables = tables[4:]

char_lst = []
weapon_lst = []
for sort_table in sort_tables:
    weapon_bool = False
    titles = sort_table.find_all('th')
    contexts = sort_table.find_all('td')
    if len(titles)!= len(contexts):
        start_index_offset = -(len(titles)-len(contexts))
    else:
        start_index_offset = 0
    for i, title in enumerate(titles):
        title_text = title.get_text()
        if '时间' in title_text:
            time_ = i
        elif '5星角色' in title_text:
            five_rank_ = i
        elif '4星角色' in title_text:
            four_rank_ = i
        elif '5星武器' in title_text:
            weapon_bool = True
            five_rank_ = i
        elif '4星武器' in title_text:
            weapon_bool = True
            four_rank_ = i
    try:
        time = contexts[time_+start_index_offset].get_text().strip()
        five_rank = contexts[five_rank_+start_index_offset].get_text().strip()
        four_rank = contexts[four_rank_+start_index_offset].get_text().strip()
    except:
        print('没有数据')
        continue
    if weapon_bool:
        weapon_lst.append({
            'time': time,
            'five_rank': five_rank,
            'four_rank': four_rank
            })
    else:
        char_lst.append({
            'time': time,
            'five_rank': five_rank,
            'four_rank': four_rank
            })

path_b = dirname_(abspath_(__file__))

import json
with open(join_(path_b, 'tmp\\char_data_get.json'), 'w', encoding='utf-8') as f, open(join_(path_b, 'tmp\\weapon_data_get.json'), 'w', encoding='utf-8') as g:
    json.dump(char_lst, f, indent=4, ensure_ascii=False)
    json.dump(weapon_lst, g, indent=4, ensure_ascii=False)

