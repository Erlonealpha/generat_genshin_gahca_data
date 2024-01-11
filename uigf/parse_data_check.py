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

with open(join_(path_b, 'tmp\\char_data_get.json'), 'r', encoding='utf-8') as f, \
    open(join_(path_b, 'tmp\\weapon_data_get.json'), 'r', encoding='utf-8') as g:
    char_data: List[dict] = json.load(f)
    weapon_data: List[dict] = json.load(g)

def nomalize_tmp_data(_data, real = True):
    # 处理没有具体时间的数据
    for i, data in enumerate(_data):
        if '版本更新后' in data['time']:
            endtime = data['time'].split('~')[-1].strip()
            if '版本更新后' in _data[i+1]['time']:
                start_time = _data[i+2]['time'].split('~')[-1].strip()
            else:
                start_time = _data[i+1]['time'].split('~')[-1].strip()
            # 不闭合时间(真实时间) 由于虚拟数据可能会生成在非卡池时间内，所以添加一个判断
            if not real:
                try:
                    tmp_end_time = datetime.strptime(endtime, '%Y/%m/%d %H:%M')
                    endtime = tmp_end_time.strftime('%Y/%m/%d %H:%M:%M')
                except:
                    pass
                try:
                    tmp_time = datetime.strptime(start_time, '%Y/%m/%d %H:%M')
                    starttime = (tmp_time + timedelta(days = 0.5) + timedelta(minutes=1)).strftime('%Y/%m/%d %H:%M:%M')
                except ValueError:
                    tmp_time = datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
                    starttime = (tmp_time + timedelta(days = 0.5) + timedelta(seconds=1)).strftime('%Y/%m/%d %H:%M:%S')
            else:
                # 按照分位补全秒位
                try:
                    tmp_end_time = datetime.strptime(endtime, '%Y/%m/%d %H:%M')
                    endtime = tmp_end_time.strftime('%Y/%m/%d %H:%M:%M')
                except ValueError:
                    pass
                # 起始时间
                try:
                    tmp_time = datetime.strptime(start_time, '%Y/%m/%d %H:%M')
                    starttime = (tmp_time + timedelta(minutes=1)).strftime('%Y/%m/%d %H:%M:%M')
                except ValueError:
                    tmp_time = datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
                    starttime = (tmp_time + timedelta(seconds=1)).strftime('%Y/%m/%d %H:%M:%S')
            data['time'] = {'starttime': starttime,
                            'endtime'  : endtime   }
        # 只需要处理时间
        else:
            start_time = data['time'].split('~')[0].strip()
            endtime = data['time'].split('~')[-1].strip()
            try:
                tmp_end_time = datetime.strptime(endtime, '%Y/%m/%d %H:%M')
                endtime = tmp_end_time.strftime('%Y/%m/%d %H:%M:%M')
            except:
                pass
            try:
                tmp_time = datetime.strptime(start_time, '%Y/%m/%d %H:%M')
                starttime = tmp_time.strftime('%Y/%m/%d %H:%M:%M')
            except ValueError:
                starttime = start_time
            data['time'] = {'starttime': starttime,
                            'endtime'  : endtime   }
        patr = re.compile(r'\([^)]*\)')
        if data['five_rank']:
            if '」「' not in data['five_rank']:
                tmp_data = data['five_rank'].strip('「」')
                name = re.sub(patr, '', tmp_data.split('·')[-1])
                data['five_rank'] = name
            else:
                _tmp_str_lst = []
                _tmp_datas_ = data['five_rank'].split('」「')
                for _tmp_data_ in _tmp_datas_:
                    _tmp_data_ = _tmp_data_.strip('「」')
                    _name_ = re.sub(patr, '', _tmp_data_.split('·')[-1])
                    _tmp_str_lst.append(_name_)
                data['five_rank'] = _tmp_str_lst
                if len(_tmp_str_lst) == 2:
                    data['five_rank_1'] = _tmp_str_lst[0]
                    data['five_rank_2'] = _tmp_str_lst[1]
                else:
                    print('error None type len rank')
                    exit(1)
                
        if data['four_rank']:
            tmp_str_lst = []
            tmp_datas_ = data['four_rank'].split('」「')
            for tmp_data_ in tmp_datas_:
                tmp_data_ = tmp_data_.strip('「」')
                name_ = re.sub(patr, '', tmp_data_.split('·')[-1])
                tmp_str_lst.append(name_)
            data['four_rank'] = tmp_str_lst
            if len(tmp_str_lst) == 3:
                data['four_rank_1'] = tmp_str_lst[0]
                data['four_rank_2'] = tmp_str_lst[1]
                data['four_rank_3'] = tmp_str_lst[2]
            elif len(tmp_str_lst) == 5:
                data['four_rank_1'] = tmp_str_lst[0]
                data['four_rank_2'] = tmp_str_lst[1]
                data['four_rank_3'] = tmp_str_lst[2]
                data['four_rank_4'] = tmp_str_lst[3]
                data['four_rank_5'] = tmp_str_lst[4]
            else:
                print('error None type len rank')
                exit(1)
    return _data

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
            group_dic_lst.append({'name': group['name'], 'data': [data['data'] for data in group['data']], 'earliest_time': earliest_time})
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
for char_group_dic in char_group_dic_lst:
    if char_group_dic['name'] in earlier_char_lst:
        char_group_dic['earliest_time'] = '2020/09/15 10:00:00'
print(df_char_data.head())

