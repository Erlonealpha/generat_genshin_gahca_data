import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
from os.path import basename as basename_
import json
from typing import List, Dict, Set
import pandas as pd

from datetime import datetime, timedelta
from random import randint

# samplejson: dict = json.load(open('./samplejson.json', encoding='utf-8'))

class TPoolType():
    def __init__(self) -> None:
        self.type = '100' | '200' | '301' | '302' | '400'

class UigfJsonType():
    class uigfinfo():
        def __init__(self) -> None:
            self.uid = None
            self.lang = None
            self.export_time = None
            self.export_timestamp = None
            self.export_app = None
            self.export_app_version = None
            self.uigf_version = None
    class uigflist():
        def __init__(self) -> None:
            self.gacha_type = None
            self.time = None
            self.name = None
            self.item_type = None
            self.rank_type = None
            self.id = None
            self.uigf_gacha_type = None

    def __init__(self) -> None:
        self.info = self.uigfinfo()
        self.list = self.uigflist()
        self.lst_col = []
        self.lst_data = []
        self.time_lst = []
        self.tmpcontex = {
        'info':
            {
            'uid': self.info.uid,
            'lang': self.info.lang,
            'export_time': self.info.export_time,
            'export_timestamp': self.info.export_timestamp,
            'export_app': self.info.export_app,
            'export_app_version': self.info.export_app_version,
            'uigf_version': self.info.uigf_version
            },
        'list':
            {
            'gacha_type': self.list.gacha_type,
            'time': self.list.time,
            'name': self.list.name,
            'item_type': self.list.item_type,
            'rank_type': self.list.rank_type,
            'id': self.list.id,
            'uigf_gacha_type': self.list.uigf_gacha_type
            }
        }
        self.lst = []

    def parse(self, info, list):
        try:
            self.info.uid = info['uid'] if info['uid'] else None
            self.info.lang = info['lang'] if info['lang'] else None
            self.info.export_time = info['export_time'] if info['export_time'] else None
            self.info.export_timestamp = info['export_timestamp'] if info['export_timestamp'] else None
            self.info.export_app = info['export_app'] if info['export_app'] else None
            self.info.export_app_version = info['export_app_version'] if info['export_app_version'] else None
            self.info.uigf_version = info['uigf_version'] if info['uigf_version'] else None

            self.list.gacha_type = list['gacha_type'] if list['gacha_type'] else None
            self.list.time = list['time'] if list['time'] else None
            self.list.name = list['name'] if list['name'] else None
            self.list.item_type = list['item_type'] if list['item_type'] else None
            self.list.rank_type = list['rank_type'] if list['rank_type'] else None
            self.list.id = list['id'] if list['id'] else None
            self.list.uigf_gacha_type = list['uigf_gacha_type'] if list['uigf_gacha_type'] else None
        except:
            pass
        self.lst.append(self.tmpcontex)

        self.parse_to_df_lst()
    
    def parse_to_df_lst(self):
        for key, val in self.tmpcontex['info'].items():
            self.lst_col.append(key)
            self.lst_data.append(val)
        for key_, val_ in self.tmpcontex['list'].items():
            self.lst_col.append(key_)
            self.lst_data.append(val_)
            self.time_lst.append(self.list.time)
# block_bool = False
# if block_bool:
#     for key, val in samplejson.items():
#         if key == "properties":
#             info = val['info']["properties"]
#             list = val['list']["items"]
#             uigf = UigfJsonType()
#             uigf.parse(info, list)

    # # 数据统计
    # df = pd.Series(column= uigf.lst_col, row= uigf.lst_data, index=uigf.time_lst)

path_j = r"F:\Documents\python_script\脚本\genshin_ufgi-fix\uigf_data_fix\uigf\uigf_json\UIGF_1.json"
path_b = dirname_(abspath_(__file__))
with open(join_(path_b, '.\\uigf_json\\UIGF_1.json'), 'r', encoding='utf-8') as f:
    uigf_json: dict = json.load(f)

gacha_info = uigf_json['info']
gacha_list: List[dict] = uigf_json['list']

df_gacha = pd.DataFrame(gacha_list)
df_gacha.info()
# 显示df前5行
print(df_gacha.head() )

# 新建一个dataframe 根据列 'name' 筛选出唯一的数据
df_gacha_unique = df_gacha.drop_duplicates(subset='name')

# 然后根据 item_type进行分组
df_gacha_unique_group = df_gacha_unique.groupby('item_type')
# 最后将分组的结果存储为列表[字典,...]
result_list = []
for name, group in df_gacha_unique_group:
    result_list.append(group.to_dict('records'))
if result_list[0][0]['item_type'] == '武器':
    weapon_list = result_list[0]
    char_list = result_list[-1]

df_gacha_char = pd.DataFrame(char_list)
df_gacha_weapon = pd.DataFrame(weapon_list)

df_gacha_char_group = df_gacha_char.groupby('rank_type')
df_gacha_weapon_group = df_gacha_weapon.groupby('rank_type')

char_type_list = []
for name, group in df_gacha_char_group:
    print(name)
    char_type_list.append(group.to_dict('records'))

weapon_type_list = []
for name, group in df_gacha_weapon_group:
    print(name)
    weapon_type_list.append(group.to_dict('records'))








time_start, time_end = '2021-01-02 12:00:00', '2022-06-11 22:00:00'
limited_char_time_interval = (time_start, time_end)
limited_cur_char_dic = [
    {'琴':         [79, ['2020-12-23 18:00:30', '2021-01-12 00:00:00']]},  # 第一个五星
    {'魈':         [79, ['2021-02-03 18:00:30', '2021-02-23 00:00:00']]},  # 当时我居然为魈 -648, 好像还充了，忘了多少了
    {'莫娜':       [80, ['2021-03-16 18:00:30']]},                         # 有印象记得是什么时候出的时间区间为准确的一天 (这个我甚至记得是在什么时候出的, 没错就是在卡池刚开没多久)
    {'胡桃':       [71, ['2021-03-16 19:00:30']]},                         # 当时歪莫娜之后，立马充了648把胡桃抽出来了 QAQ
    {'七七':       [33, ['2021-03-17 18:00:30', '2021-04-06 00:00:00']]},  # 好像是一天的中午刚强化完胡桃的圣遗物抽出来的, 还兴奋了挺久
    {'钟离':       [76, ['2021-04-28 18:00:30', '2021-05-18 00:00:00']]},  # 具体时间记不清楚了，但肯定不是卡池出的那一天
    {'七七':       [50, ['2021-05-19 18:00:30']]},  # 这个和优菈是几乎同时出的, 当时我直接跳起来了...
    {'优菈':       [9,  ['2021-05-19 18:03:30']]},  # 第一次10连双金
    {'迪卢克':     [76, ['2021-06-09 18:00:30']]},  # 痛苦的经历，当时家里电脑暂时没法用了就去网吧抽可莉。 结果...
    {'可莉':       [76, ['2021-06-09 18:10:30']]},  # 本人很喜欢可莉, 所以... -648...
    {'枫原万叶':   [11, ['2021-06-29 18:00:30']]},  # 卡池刚开的时候应该是
    {'琴':         [39, ['2021-06-29 18:00:30', '2021-07-21 00:00:00']]},  # 应该和上个卡池隔了半个版本
    {'神里绫华':   [20, ['2021-07-22 18:00:30']]},  # 好像是卡池第二天
    {'宵宫':       [39, ['2021-08-10 18:10:30']]},  # 应该是卡池刚出的时候
    {'珊瑚宫心海': [75, ['2021-09-21 18:00:30', '2021-10-12 00:00:00']]},  # 卡池前中期？
    {'胡桃':       [77, ['2021-11-03 18:00:30', '2021-11-23 00:00:00']]},  # 卡池中后期？
    {'阿贝多':     [36, ['2021-11-24 18:00:30', '2021-12-14 00:00:00']]},  # 应该是卡池刚开的时候
    {'申鹤':       [77, ['2022-01-05 18:00:30', '2022-01-15 00:00:00']]},  # 卡池前中期
    {'甘雨':       [53, ['2022-01-25 18:00:30', '2022-02-15 00:00:00']]},  # 卡池第一天or刚开卡池
    {'八重神子':   [74, ['2022-02-16 18:00:30', '2022-03-08 00:00:00']]},  # 卡池第一天or第二天
    {'雷电将军':   [72, ['2022-03-08 18:00:30', '2022-03-29 00:00:00']]},  # 卡池前中期
    {'刻晴':       [39, ['2022-03-30 18:00:30', '2022-04-19 00:00:00']]},  # 卡池前期  终结了9连没歪
    {'夜兰':       [80, ['2022-05-31 18:00:30', '2022-06-21 00:00:00']]},  # 应该是卡池末期
    {'':           [17, ['2022-06-21 18:00:30', '2022-07-12 00:00:00']]}   # 这个是未出货抽数 #TODO 这里的数据和之后的数据合并可能会出现保底大于180的情况, 得特殊处理
]                                                                        # 还有有半年的数据是丢失的(悲) 但是可以通过已经获取的角色猜测, 歪的是谁就不清楚了，但我只知道琴11命...

time_start_, time_end_ = '2020-11-28 12:00:00', '2022-05-19 22:00:00'
limited_weapon_time_interval = (time_start_, time_end_)
weapon_cur_dic = {
    '和璞鸢':       [35, ['2021-02-03 18:00:30', '2021-02-23 00:00:00']], # 当时充剩下的还抽了武器
    '狼的末路':     [65, ['2021-03-16 19:30:30', '2021-03-16 19:30:30']], # 抽护摩歪了
    '天空之刃':     [68, '2021'], # 好像是给可莉抽四风的时候歪的
    '终末嗟叹之诗': [43, '2021'], # 
    '护摩之杖':     [65, '2021'], # 第二次抽胡桃出的
    '薙草之稻光':   [53, '2021'], # 雷神池末期
    '天空之傲':     [71, '2021'], # 
    '':             [2, '2021']
}

time_start__, time_end__ = '2020-11-28 12:00:00', '2022-06-11 22:00:00'
limited_permanent_time_interval = (time_start__, time_end__)
permanent_cur_char_dic = {
    '琴':       [79, '2021'], # 常驻第一个，忘了什么时候了
    '天空之卷': [83, '2021'], # 这里的可以根据抽卡数大致推断时间
    '七七':     [79, '2021'],
    '风鹰剑':   [16, '2021'],
    '天空之傲': [73, '2021'],
    '':         [19, '2021']
}




def nomalize_data(data: List[dict], item_type: str) -> dict:
    """
    处理数据, 按照特定规则随机补全缺失数据
    :param data:
    :return:
    """
    gacha_lst = []
    for dic in data:
        v = list(dic.values())[0]
        if len(v[1])>1:
            time = random_time(v[1][0], v[1][1])
        else:
            time = v[1][0]
        new_dic = {
            'gacha_type': None,
            'time': time,
            'name': list(dic.keys())[0],
            'item_name': None,
            'item_type': item_type,
            'rank_type': None,
            'id': None,
            'uigf_gacha_type': None 
        }
        gacha_lst.append(new_dic)
    return gacha_lst
    
    


def random_time(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    time_between_dates = end - start

    random_second = randint(0, time_between_dates.total_seconds())
    random_date = start + timedelta(seconds=random_second)

    random_date_str = random_date.strftime('%Y-%m-%d %H:%M:%S')
    return random_date_str



def fill_data_to_uigf() -> dict:

    ...
    
lst = nomalize_data(limited_cur_char_dic, '角色')

print()
