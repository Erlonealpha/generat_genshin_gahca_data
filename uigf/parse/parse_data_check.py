from typing import List, Dict
import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
import re
import json
from datetime import datetime, timedelta

import pandas as pd

path_b = dirname_(abspath_(__file__))

with open(join_(path_b, '..\\tmp\\char_data_get.json'), 'r', encoding='utf-8') as f, \
    open(join_(path_b, '..\\tmp\\weapon_data_get.json'), 'r', encoding='utf-8') as g:
    char_data: List[dict] = json.load(f)
    weapon_data: List[dict] = json.load(g)
    

def convert_datetime(
        strtime, 
        days:None | int=None,
        minute:None | int=None,
        second:None | int=None,
        operator:None | str=None,
        convert:bool = False,
    ):
    def nomalize_time(time) -> datetime:
        if operator == 'add':
            if days:
                time += timedelta(days=days)
            if minute:
                time += timedelta(minutes=minute)
            if second:
                time += timedelta(seconds=second)
        elif operator == 'sub':
            if days:
                time -= timedelta(days=days)
            if minute:
                time -= timedelta(minutes=minute)
            if second:
                time += timedelta(seconds=second)
        elif days or minute:
            assert 'operator is not add or sub'
        return time

    try:
        # 分开处理需要提前将%H:%M转换为%H:%M:%M，但又需要保留except能正常捕获%H:%M:%S
        if convert:
            date_time = datetime.strptime(strtime, '%Y/%m/%d %H:%M')
            date_time_tmp = date_time.strftime('%Y/%m/%d %H:%M:%M')
            date_time_tmp = datetime.strptime(date_time_tmp, '%Y/%m/%d %H:%M:%S')
            date_time = nomalize_time(date_time_tmp)
            output = date_time.strftime('%Y/%m/%d %H:%M:%M')
        else:
            date_time = datetime.strptime(strtime, '%Y/%m/%d %H:%M')
            date_time = nomalize_time(date_time)
            output = date_time.strftime('%Y/%m/%d %H:%M:%M')
    except ValueError:
        date_time = datetime.strptime(strtime, '%Y/%m/%d %H:%M:%S')
        date_time = nomalize_time(date_time)
        output = date_time.strftime('%Y/%m/%d %H:%M:%S')
    return output


def nomalize_tmp_data(_data: List[dict], real = False):
    # 处理没有具体时间的数据
    for i, data in enumerate(_data):
        if '版本更新后' in data['time']:
            endtime = data['time'].split('~')[-1].strip()
            if '版本更新后' in _data[i+1]['time']:
                start_time = _data[i+2]['time'].split('~')[-1].strip()
            else:
                start_time = _data[i+1]['time'].split('~')[-1].strip()
            # 不闭合时间(真实时间) 由于虚拟数据可能会生成在非卡池时间内，所以添加一个判断
            if real:
                endtime = convert_datetime(endtime)
                starttime = convert_datetime(start_time, days=0.5, second=1, operator='add', convert=True)

            else:
                endtime = convert_datetime(endtime)
                starttime = convert_datetime(start_time, second=1, operator='add', convert=True)

            data['time'] = {'starttime': starttime,
                            'endtime'  : endtime   }
        # 只需要处理时间
        else:
            start_time = data['time'].split('~')[0].strip()
            endtime = data['time'].split('~')[-1].strip()
            endtime = convert_datetime(endtime)
            starttime = convert_datetime(start_time)

            data['time'] = {'starttime': starttime,
                            'endtime'  : endtime   }
        # 只保留名称
        patr = re.compile(r'\([^)]*\)')
        data['five_rank'] = [re.sub(patr, '', name.split('·')[-1]) for name in data['five_rank_list']]
        data['four_rank'] = [re.sub(patr, '', name.split('·')[-1]) for name in data['four_rank_list']]
    return _data

latest_version = char_data[0].get('version')
char_data_ = nomalize_tmp_data(char_data)
weapon_data_ = nomalize_tmp_data(weapon_data)

def merge_data(char_data, keyword):
    lst = []
    for char_data__ in char_data:
        for char in char_data__[keyword]:
            lst.append({'name': char, 'data': char_data__})
    return lst

char_merge_data = merge_data(char_data_, 'four_rank')
weapon_merge_data = merge_data(weapon_data_, 'four_rank')

df_char_data = pd.DataFrame(char_merge_data)
df_weapon_data = pd.DataFrame(weapon_merge_data)
# group by each rank
df_char_group = df_char_data.groupby('name')
df_weapon_group = df_weapon_data.groupby('name')

def group_to_dic_lst(group_: List[dict], dic_b = False):
    group_dic_lst = []
    if dic_b:
        for group in group_:
            time_lst = [dic_['data']['time']['starttime'] for dic_ in group['data']]
            # starttime_lst = [dic.get('starttime') for dic in time_lst]
            earliest_time = min(time_lst)
            group_dic_lst.append({'name': group['name'],
                                  'latest_version': latest_version,
                                  'data': [data['data'] for data in group['data']], 
                                  'earliest_time': earliest_time})
        return group_dic_lst
    else:
        return [{'name': name, 'data': group.to_dict('records')} for name, group in group_]

char_group_dic_lst_ = group_to_dic_lst(df_char_group)
char_group_dic_lst = group_to_dic_lst(char_group_dic_lst_, dic_b=True)
weapon_group_dic_lst_ = group_to_dic_lst(df_weapon_group)
weapon_group_dic_lst = group_to_dic_lst(weapon_group_dic_lst_, dic_b=True)

# 这些最早的角色在公测开始就有的，设置统一的起始时间
earlier_char_lst = ['砂糖','芭芭拉','莱依拉','菲谢尔','行秋','诺艾尔','辛焱','迪奥娜','重云','雷泽','香菱']
# 御三家
char_lst = ['凯亚', '丽萨', '安伯']
earlier_weapon_lst = ['匣里灭辰','匣里龙吟','弓藏','昭心','流浪乐章','祭礼剑',
                      '祭礼大剑','祭礼弓','祭礼残章','笛剑','绝弦','西风剑',
                      '西风大剑','西风猎弓','西风秘典','西风长枪','钟剑','雨裁']

for char_group_dic in char_group_dic_lst:
    if char_group_dic['name'] in earlier_char_lst:
        char_group_dic['earliest_time'] = '2020/09/15 10:00:00'
for weapon_group_dic in weapon_group_dic_lst:
    if weapon_group_dic['name'] in earlier_weapon_lst:
        weapon_group_dic['earliest_time'] = '2020/09/15 10:00:00'
        weapon_group_dic['rank_type'] = 4
        
# 写入三星武器
with open(join_(path_b, '..\\data_json\\weapon_data_with_version.json'), 'r', encoding='utf-8') as j:
    weapon_data_with_version = json.load(j)
match_data = [context for context in weapon_data_with_version[0]['context'] if context['rank_type']==3]
for match_ in match_data:
    weapon_group_dic_lst.append({'name': match_['name'], 
                                 'data': None,
                                 'earliest_time': '2020/09/15 10:00:00',
                                 'rank_type': 3})

with open(join_(path_b, '..\\data_json\\char_data.json'), 'w', encoding='utf-8') as r, \
     open(join_(path_b, '..\\data_json\\weapon_data.json'), 'w', encoding='utf-8') as s:
    json.dump(char_group_dic_lst, r, ensure_ascii=False, indent=4)
    json.dump(weapon_group_dic_lst, s, ensure_ascii=False, indent=4)



