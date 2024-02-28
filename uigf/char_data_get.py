import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
import requests
from bs4 import BeautifulSoup


def sliceContent(text: str, find: str, tag='/span'):
    res = text.find(find)
    resc = text[res:]
    i = resc.find(tag)
    rec = resc[i+len(tag)+1:].strip()
    return resc


url = 'https://wiki.biligame.com/ys/%E7%A5%88%E6%84%BF'
url = 'https://wiki.biligame.com/ys/%E5%BE%80%E6%9C%9F%E7%A5%88%E6%84%BF'
respone = requests.get(url)
soup = BeautifulSoup(respone.text, 'html.parser')
sort_pos_prayerPools = soup.find("span", class_="mw-headline", id="历史活动祈愿一览")
tables = soup.find_all('table', class_=lambda x: x and 'wikitable' in x.split())
stables = [tab for tab in tables if tab.attrs.get('style')]

# for i, table in enumerate(tables):
#     if table.find('span', id='活动祈愿（当前）'): 
#         print()
#     str_len = len(table.get_text())
#     if str_len > min_c:
#         min_c = str_len
#         index = i
# sort_table = tables[index]
# sort_trs = sort_table.find_all('table', class_='wikitable')

# 去除两边的指定内容(这里为「和」)
def remove_side_str(string, side_str_L='「', side_str_R='」'):
    if string[0] == side_str_L:
        string=string[1:]
    if string[-1] == side_str_R:
        string=string[:-1]
    return string
        
char_lst = []
weapon_lst = []
for sort_tr in stables:
    # weapon_bool = False
    text = sort_tr.get_text()
    text_lst = [[u for u in y.split('\n') if u] for y in [x for x in text.split('时间') if x] if [z for z in y.split('\n') if z]]
    
    for sort_text in text_lst:
        if sort_text[3] == '5星角色':
            five_rank_lst = [remove_side_str(sort_text[4])]
            four_rank_lst = [remove_side_str(x) for x in sort_text[6].split('」「')]
            char_lst.append({
            'time': sort_text[0],
            'version': sort_text[2],
            'five_rank': sort_text[4],
            'four_rank': sort_text[6],
            'five_rank_list': five_rank_lst,
            'four_rank_list': four_rank_lst,
            })
        else:
            five_rank_lst = [remove_side_str(x) for x in sort_text[4].split('」「')]
            four_rank_lst = [remove_side_str(x) for x in sort_text[6].split('」「')]
            weapon_lst.append({
            'time': sort_text[0],
            'version': sort_text[2],
            'five_rank': sort_text[4],
            'four_rank': sort_text[6],
            'five_rank_list': five_rank_lst,
            'four_rank_list': four_rank_lst,
            })


path_b = dirname_(abspath_(__file__))

import json
with open(join_(path_b, 'tmp\\char_data_get.json'), 'w', encoding='utf-8') as f, open(join_(path_b, 'tmp\\weapon_data_get.json'), 'w', encoding='utf-8') as g:
    json.dump(char_lst, f, indent=4, ensure_ascii=False)
    json.dump(weapon_lst, g, indent=4, ensure_ascii=False)

