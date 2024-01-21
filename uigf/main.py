import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
from os.path import basename as basename_
import json
from typing import List, Dict, Set
import pandas as pd

from datetime import datetime, timedelta
import random

from randomTime import *
from random_4rank import random_4rank, chose_luck_np

# samplejson: dict = json.load(open('./samplejson.json', encoding='utf-8'))

path_j = r"F:\Documents\python_script\脚本\genshin_ufgi-fix\uigf_data_fix\uigf\uigf_json\UIGF_1.json"
path_b = dirname_(abspath_(__file__))

def load_analyze_data(path):
    #=================================================================
    # 读取json文件
    with open(join_(path_b, path), 'r', encoding='utf-8') as f:
        uigf_json: dict = json.load(f)
    # 数据分析
    gacha_info = uigf_json['info']
    gacha_list: List[dict] = uigf_json['list']

    df_gacha = pd.DataFrame(gacha_list)
    # df_gacha.info()

    df_gacha_type_group = df_gacha.groupby('uigf_gacha_type')
    df_gacha_type_lst = []
    for name, group in df_gacha_type_group:
        df_gacha_type_lst.append(group.to_dict('records'))

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
        char_type_list.append(group.to_dict('records'))

    weapon_type_list = []
    for name, group in df_gacha_weapon_group:
        weapon_type_list.append(group.to_dict('records'))
    #=================================================================


#=================================================================
# 临时的目标数据
limited_gacha_count_dic = {
    '五星': 23,
    '四星': 177,
    '三星': 1138,
    '四星武器': 52,
    '四星角色': 125
}

limited_weapon_gacha_count_dic = {
    '五星': 7,
    '四星': 65,
    '三星': 330,
    '四星武器': 55,
    '四星角色': 10
}

permanent_gacha_count_dic = {
    '五星': 6,
    '四星': 56,
    '三星': 365,
    '五星角色': 3,
    '五星武器': 3,
    '四星武器': 29,
    '四星角色': 27
}

time_start, time_end = '2021-01-02 12:00:00', '2022-06-11 22:00:00'
limited_char_time_interval = (time_start, time_end)
limited_cur_char_dic = [
    {'category': '起始时间',   'data': {'fill_len': 0,  'time': ['2020-11-28 18:00:00', '2020-12-22 00:00:00']}, 'item_type': '角色'},
    {'category': '琴',         'data': {'fill_len': 79, 'time': ['2020-12-23 18:00:30', '2021-01-12 00:00:00']}, 'item_type': '角色'},  # 第一个五星
    {'category': '魈',         'data': {'fill_len': 79, 'time': ['2021-02-03 18:00:30', '2021-02-23 00:00:00']}, 'item_type': '角色'},  # 当时我居然为魈 -648, 好像还充了，忘了多少了
    {'category': '莫娜',       'data': {'fill_len': 80, 'time': ['2021-03-16 18:00:30']}                       , 'item_type': '角色'},  # 有印象记得是什么时候出的时间区间为准确的一天 (这个我甚至记得是在什么时候出的, 没错就是在卡池刚开没多久)
    {'category': '胡桃',       'data': {'fill_len': 71, 'time': ['2021-03-16 19:00:30']}                       , 'item_type': '角色'},  # 当时歪莫娜之后，立马充了648把胡桃抽出来了 QAQ
    {'category': '七七',       'data': {'fill_len': 33, 'time': ['2021-03-17 18:00:30', '2021-04-06 00:00:00']}, 'item_type': '角色'},  # 好像是一天的中午刚强化完胡桃的圣遗物抽出来的, 还兴奋了挺久
    {'category': '钟离',       'data': {'fill_len': 76, 'time': ['2021-04-28 18:00:30', '2021-05-18 00:00:00']}, 'item_type': '角色'},  # 具体时间记不清楚了，但肯定不是卡池出的那一天
    {'category': '七七',       'data': {'fill_len': 50, 'time': ['2021-05-19 18:00:30']}                       , 'item_type': '角色'},  # 这个和优菈是几乎同时出的, 当时我直接跳起来了...
    {'category': '优菈',       'data': {'fill_len': 9,  'time': ['2021-05-19 18:03:30']}                       , 'item_type': '角色'},  # 第一次10连双金
    {'category': '迪卢克',     'data': {'fill_len': 76, 'time': ['2021-06-09 18:00:30']}                       , 'item_type': '角色'},  # 痛苦的经历，当时家里电脑暂时没法用了就去网吧抽可莉。 结果...
    {'category': '可莉',       'data': {'fill_len': 76, 'time': ['2021-06-09 18:10:30']}                       , 'item_type': '角色'},  # 本人很喜欢可莉, 所以... -648...
    {'category': '枫原万叶',   'data': {'fill_len': 11, 'time': ['2021-06-29 18:00:30']}                       , 'item_type': '角色'},  # 卡池刚开的时候应该是
    {'category': '琴',         'data': {'fill_len': 39, 'time': ['2021-06-29 18:00:30', '2021-07-21 00:00:00']}, 'item_type': '角色'},  # 应该和上个卡池隔了半个版本
    {'category': '神里绫华',   'data': {'fill_len': 20, 'time': ['2021-07-22 18:00:30']}                       , 'item_type': '角色'},  # 好像是卡池第二天
    {'category': '宵宫',       'data': {'fill_len': 39, 'time': ['2021-08-10 18:10:30']}                       , 'item_type': '角色'},  # 应该是卡池刚出的时候
    {'category': '珊瑚宫心海', 'data': {'fill_len': 75, 'time': ['2021-09-21 18:00:30', '2021-10-12 00:00:00']}, 'item_type': '角色'},  # 卡池前中期？
    {'category': '胡桃',       'data': {'fill_len': 77, 'time': ['2021-11-03 18:00:30', '2021-11-23 00:00:00']}, 'item_type': '角色'},  # 卡池中后期？
    {'category': '阿贝多',     'data': {'fill_len': 36, 'time': ['2021-11-24 18:00:30', '2021-12-14 00:00:00']}, 'item_type': '角色'},  # 应该是卡池刚开的时候
    {'category': '申鹤',       'data': {'fill_len': 77, 'time': ['2022-01-05 18:00:30', '2022-01-15 00:00:00']}, 'item_type': '角色'},  # 卡池前中期
    {'category': '甘雨',       'data': {'fill_len': 53, 'time': ['2022-01-25 18:00:30', '2022-02-15 00:00:00']}, 'item_type': '角色'},  # 卡池第一天or刚开卡池
    {'category': '八重神子',   'data': {'fill_len': 74, 'time': ['2022-02-16 18:00:30', '2022-03-08 00:00:00']}, 'item_type': '角色'},  # 卡池第一天or第二天
    {'category': '雷电将军',   'data': {'fill_len': 72, 'time': ['2022-03-08 18:00:30', '2022-03-29 00:00:00']}, 'item_type': '角色'},  # 卡池前中期
    {'category': '刻晴',       'data': {'fill_len': 39, 'time': ['2022-03-30 18:00:30', '2022-04-19 00:00:00']}, 'item_type': '角色'},  # 卡池前期  终结了9连没歪
    {'category': '夜兰',       'data': {'fill_len': 80, 'time': ['2022-05-31 18:00:30', '2022-06-21 00:00:00']}, 'item_type': '角色'},  # 应该是卡池末期
    {'category': '已抽未出数', 'data': {'fill_len': 17, 'time': ['2022-06-21 18:00:30', '2022-07-12 00:00:00']}, 'item_type': '角色'}   # 这个是未出货抽数 #TODO 这里的数据和之后的数据合并可能会出现保底大于180的情况, 得特殊处理
]                                                                        # 还有有半年的数据是丢失的(悲) 但是可以通过已经获取的角色猜测, 歪的是谁就不清楚了，但我只知道琴11命...

time_start_, time_end_ = '2020-11-28 12:00:00', '2022-05-19 22:00:00'
limited_weapon_time_interval = (time_start_, time_end_)
limited_weapon_cur_dic = [
    {'category': '起始时间',     'data':{'fill_len': 0,  'time': ['2020-11-28 18:00:00', '2021-02-02 00:00:00']}, 'item_type': '武器'},
    {'category': '和璞鸢',       'data':{'fill_len': 35, 'time': ['2021-02-03 18:00:30', '2021-02-23 00:00:00']}, 'item_type': '武器'}, # 当时充剩下的还抽了武器
    {'category': '狼的末路',     'data':{'fill_len': 65, 'time': ['2021-03-16 19:30:30', '2021-03-16 19:30:30']}, 'item_type': '武器'}, # 抽护摩歪了
    {'category': '天空之刃',     'data':{'fill_len': 68, 'time': ['2021-06-09 10:30:00', '2021-06-29 17:59:59']}, 'item_type': '武器'}, # 好像是给可莉抽四风的时候歪的
    {'category': '终末嗟叹之诗', 'data':{'fill_len': 43, 'time': ['2021-06-29 17:59:59', '2021-11-02 18:00:00']}, 'item_type': '武器'}, # 
    {'category': '护摩之杖',     'data':{'fill_len': 65, 'time': ['2021-11-02 18:00:00', '2021-11-23 14:59:59']}, 'item_type': '武器'}, # 第二次抽胡桃出的
    {'category': '薙草之稻光',   'data':{'fill_len': 53, 'time': ['2022-03-08 18:00:00', '2022-03-29 14:59:00']}, 'item_type': '武器'}, # 雷神池末期
    {'category': '天空之傲',     'data':{'fill_len': 71, 'time': ['2022-04-29 14:59:00', '2022-05-17 22:00:00']}, 'item_type': '武器'}, # 
    {'category': '已抽未出数',   'data':{'fill_len': 2,  'time': ['2022-05-17 22:00:00', '2022-05-17 22:00:00']}, 'item_type': '武器'}
]

time_start__, time_end__ = '2020-11-28 12:00:00', '2022-06-11 22:00:00'
limited_permanent_time_interval = (time_start__, time_end__)
permanent_cur_char_dic = [
    {'category': '起始时间',    'data': {'fill_len': 0,  'time':  ['2020-11-28 18:00:00', '2020-12-22 00:00:00']}, 'item_type': ''},
    {'category': '琴',          'data': {'fill_len': 79, 'time':  ['2020-12-22 00:00:00', '2021-01-12 00:00:00']}, 'item_type': '角色'}, # 常驻第一个，忘了什么时候了
    {'category': '天空之卷',    'data': {'fill_len': 83, 'time':  ['2021-02-12 00:00:00', '2021-03-25 00:00:00']}, 'item_type': '武器'}, # 这里的可以根据抽卡数大致推断时间
    {'category': '七七',        'data': {'fill_len': 79, 'time':  ['2021-04-15 00:00:00', '2021-06-15 00:00:00']}, 'item_type': '角色'},
    {'category': '风鹰剑',      'data': {'fill_len': 16, 'time':  ['2021-07-01 00:00:00', '2021-07-25 00:00:00']}, 'item_type': '武器'},
    {'category': '琴',          'data': {'fill_len': 78, 'time':  ['2021-09-25 00:00:00', '2021-11-25 00:00:00']}, 'item_type': '角色'},
    {'category': '天空之傲',    'data': {'fill_len': 73, 'time':  ['2021-12-25 00:00:00', '2022-03-01 22:00:00']}, 'item_type': '武器'},
    {'category': '已抽未出数',  'data': {'fill_len': 19, 'time':  ['2022-05-01 22:00:00', '2022-06-11 22:00:00']}, 'item_type': ''}
]
#=================================================================

class SectionContext():
    def __init__(self):
        self.section: str = str
        self.context: List[str] = []


def parse_input_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    section_lst = []
    remove_index_lst = []
    ignore = False
    for i,line in enumerate(lines):
        for j,strr in enumerate(line):
            if strr =='/' and j != (len(line)-1) and line[j+1]=='*':
                st = i
                ignore = True
                continue
            if strr=='*' and j != (len(line)-1) and line[j+1]=='/':
                remove_index_lst.append([i, st])
                ignore = False
                break
            if strr == ';':
                line = line[:j] + '\n'
                lines[i] = line
        if line.startswith('[') and line.endswith(']\n') and not ignore:
            section_lst.append([line.strip('[]\n'), i])
            continue
        if line == '\n' and not ignore:
            remove_index_lst.append([i,i])
            continue
    for remove_index in reversed(remove_index_lst):
        i = remove_index[0]
        st = remove_index[1]
        for k in range(i, st-1, -1):
            lines.pop(k)
        st-=1
        for section in section_lst:
            offset = i-st if i-st!=0 else 1
            if section[1] > i:
                section[1] -= offset
    lines = [x.strip('\n') for x in lines]
    input_data_lst = []
    for i,section in enumerate(section_lst):
        end_index = section_lst[i+1][1]-1 if i+1<len(section_lst) else len(lines)-1
        input_data = SectionContext()
        input_data.section = section[0]
        lines_ = lines[section[1]:end_index+1]
        lines_.pop(0)
        input_data.context = lines_
        input_data_lst.append(input_data)

    return input_data_lst

def InputData_to_gacha_data(input_data_lst: List[SectionContext]):
    global limited_cur_char_dic
    global limited_weapon_cur_dic
    global permanent_cur_char_dic
    global limited_gacha_count_dic
    global limited_weapon_gacha_count_dic
    global permanent_gacha_count_dic
    def to_dic(count_bool=False):
        lst = []
        try:
            if count_bool:
                for line in section_context.context:
                    line_split = [x for x in line.split(',') if x]
                    if len(line_split) != 2:
                        raise Exception('Error in context: %s\n存在单个内容长度错误'%section_context.context)
                    lst.append({line_split[0]: line_split[1]})
            else:
                for line in section_context.context:
                    line_split = [x for x in line.split(',') if x]
                    if len(line_split) != 4:
                        raise Exception('Error in context: %s\n存在单个内容长度错误'%section_context.context)
                    
                    time = [line_split[2].split("'")[1], line_split[2].split("'")[3]] if len(line_split[2].split("'"))==5 else [line_split[2].strip("[]'")]

                    lst.append(
                        {'category': line_split[0], 
                            "data": {
                                "fill_len": int(line_split[1]),
                                "time": time,
                        },
                        "item_type": line_split[3]
                    })
        except:
            raise Exception('Error in context: %s\n无效的内容'%section_context.context)
        return lst
    for section_context in input_data_lst:
        if section_context.section == 'char_limited_gacha':
            limited_cur_char_dic = to_dic()
        elif section_context.section == 'weapon_limited_gacha':
            limited_weapon_cur_dic = to_dic()
        elif section_context.section == 'limited_permanent_gacha':
            permanent_cur_char_dic = to_dic()
        elif section_context.section == 'char_limited_gacha_count':
            limited_gacha_count_dic = to_dic(count_bool=True)
        elif section_context.section == 'weapon_limited_gacha_count':
            limited_weapon_gacha_count_dic = to_dic(count_bool=True)
        elif section_context.section == 'limited_permanent_gacha_count':
            permanent_gacha_count_dic = to_dic(count_bool=True)
        else:
            raise Exception('Unknown section: %s'%section_context.section)




def nomalize_data(
        data: List[dict], 
        gacha_type: str
    ) -> dict:
    """
    处理数据, 按照特定规则随机补全缺失数据
    :param data:
    :return:
    """
    
    if gacha_type == '100':   # 新手池
        uigf_gacha_type = '100'
    elif gacha_type == '200': # 常驻池
        uigf_gacha_type = '200'
    elif gacha_type == '301' or gacha_type == '400': # 限定池
        uigf_gacha_type = '301'
    elif gacha_type == '302': # 限定武器池
        uigf_gacha_type = '302'
    
    gacha_lst = []
    for dic in data:
        name    = dic['category']
        context = dic['data']
        # 根据时间区间随机一个时间
        if name == '起始时间' or name == '已抽未出数':
            time = context['time']
        elif len(context['time'])>1:
            time = random_time(context['time'][0], context['time'][1])
        else:
            time = context['time'][0]
        
        if name == '已抽未出数': # 已抽未出数不需要减去五星自身
            fill_len = context['fill_len']
        else:
            fill_len = context['fill_len']-1 if context['fill_len']-1 >= 0 else 0
        
        new_dic = {
            'gacha_type': gacha_type,
            'time': time,
            'name': name,
            'item_type': dic['item_type'],
            'rank_type': '5',
            'id': None,
            'uigf_gacha_type': uigf_gacha_type,
            'fill_len': fill_len
        }
        gacha_lst.append(new_dic)
    return gacha_lst


def fill_data_to_uigf(lst: List[dict]) -> dict:
    gacha_lst = []
    for i, dic in enumerate(lst):
        if dic['name'] == '起始时间':
            starttime = dic['time'][0]
            starttime_front = starttime
            continue
        elif dic['name'] == '已抽未出数':
            starttime = starttime_front
            endtime = dic['time'][1]
            fill_len = dic['fill_len']
        else:
            starttime = starttime_front
            fill_len = dic['fill_len']
            endtime = dic['time']
            starttime_front = endtime
        random_times = generate_random_times(starttime, endtime, fill_len)
        for time in random_times:
            new_dic = {
                'gacha_type': dic['gacha_type'],
                'time': time,
                'name': None,
                'item_type': None,
                'rank_type': None,
                'id': None,
                'uigf_gacha_type': dic['uigf_gacha_type'],
            }
            gacha_lst.append(new_dic)
    return gacha_lst


#===============================================================
# *随机物品逻辑部分：
# 按照数量随机生成4星物品填充，随机的物品按照当期的up概率填充具体物品
# 3星同理，但只需要全部随机即可
# 
# *流程：
# 1. 随机4星的位置
# 2. 4星具体物品根据概率填充
# 3. 随机3星的位置
# 4. 3星具体物品全局随机填充
#
# *一些细节：
# 4星物品的具体选择包含：常驻(御三家)或up(按照当期的4星up)
#===============================================================
def random_rank_4(
        gacha_lst: List[dict], 
        gacha_count_dic: List[dict], 
        luck_input: bool=None, 
        weapon_pool: bool=False, 
        pp_bool: bool=False):
    '''
    输入:
        * luck_input:  输入基础概率,为了快速随机抽取的索引 | 没有输入则会根据频率计算
        * weapon_pool: 输入卡池为武器池的情况
        * pp_bool:     输入卡池为常驻池的情况
        
    输出:
        * gacha_lst:   生成的4星物品列表
    '''
    
    # 随机获取4星,根据四星占比获取基础概率
    if not luck_input:
        ori_luck = len(gacha_lst)/gacha_count_dic['四星']
        luck = chose_luck_np(ori_luck, 360, 250)
        print('调优后的概率: %d'%luck)
    else:
        luck = luck_input
    # 随机部分, 使用了正向迭代
    gacha_lst_index = random_4rank(len(gacha_lst), g4rank_len=gacha_count_dic['四星'], luck_w_c=luck)
    random_index_lst = []
    for i, x in enumerate(gacha_lst_index):
        if x==4 or x==5:
            random_index_lst.append(i)
    random_index_lst.sort()
    random_index_char_lst = random.sample(random_index_lst, gacha_count_dic['四星角色'])
    random_index_char_lst.sort()
    random_index_weapon_lst = [index for index in random_index_lst if index not in random_index_char_lst]
    # random_index_weapon_lst = random.sample(random_index_lst_, gacha_count_dic['四星武器'])
    random_index_weapon_lst.sort()
    
    bool_ = weapon_pool if not pp_bool else pp_bool
    for index in random_index_char_lst:
        gacha_lst[index]['rank_type'] = '4'
        gacha_lst[index]['item_type'] = '角色'
        gacha_lst[index]['name'] = random_obj_with_timeInteval(gacha_lst[index], char_data, weapon_pool=bool_)
    for index in random_index_weapon_lst:
        gacha_lst[index]['rank_type'] = '4'
        gacha_lst[index]['item_type'] = '武器'
        gacha_lst[index]['name'] = random_obj_with_timeInteval(gacha_lst[index], weapon_data_rank_4, weapon_bool=True, weapon_pool=pp_bool)
    return gacha_lst

def random_obj_with_timeInteval(gacha, time_interval_dic_lst, weapon_bool=False, weapon_pool=False):
    target_time = datetime.strptime(gacha['time'], '%Y-%m-%d %H:%M:%S')
    probability_dic = {}
    probability_dic['permanent'] = []
    probability_dic['up'] = []
    # 所有符合起始时间的角色/武器
    random_name_lst = []
    # up角色/武器
    probability_up_lst = []
    for data_dic in  time_interval_dic_lst:
        tmp_time = datetime.strptime(data_dic['earliest_time'], '%Y/%m/%d %H:%M:%S')
        if target_time >= tmp_time:
            # FIXED 将单次卡池内的所有4星角色/武器加入列表
            match_  = [data['four_rank'] for data in  [data_lst for data_lst in data_dic['data']] if data['time']['starttime']==data_dic['earliest_time']]
            if match_:
                random_name_lst += match_[0]
            else:
                random_name_lst.append(data_dic['name'])
            # probability_dic['permanent'].append({'name': data_dic['name'], 'probability': Permanentprobability})
        if data_dic['data']:
            for data in data_dic['data']:
                starttime = datetime.strptime(data['time']['starttime'], '%Y/%m/%d %H:%M:%S')
                endtime = datetime.strptime(data['time']['endtime'], '%Y/%m/%d %H:%M:%S')
                if target_time >= starttime and target_time <= endtime:
                    probability_up_lst += data['four_rank']
    # 御三家
    if not weapon_bool:
        for char_ in char_lst:
            probability_dic['permanent'].append({'name': char_, 'probability': Permanentprobability_})
    
    # 去除重复的角色/武器
    probability_up_lst = list(set(probability_up_lst))
    random_name_lst = list(set(random_name_lst))
    # 从常驻去除up角色/武器
    if not weapon_pool:
        for char in probability_up_lst:
            try:
                random_name_lst.remove(char)
            except:
                print(f'ERROR: random_obj_with_timeInteval() up角色在匹配角色列表找不到 char: {char}')
                pass
    
    for pp in random_name_lst:
        probability_dic['permanent'].append({'name': pp, 'probability': Permanentprobability})
    
    for up_name in probability_up_lst:
        probability_dic['up'].append({'name': up_name, 'probability': UPprobability})
    
    fianl_char_name = random_obj_with_probability(probability_dic, noup=weapon_pool)
    return fianl_char_name

def random_obj_with_probability(probability_dic, noup=False):
    all_item_lst_withprobability = probability_dic['permanent'] + probability_dic['up'] if not noup else probability_dic['permanent']
    probabilities = [item['probability'] for item in all_item_lst_withprobability]
    item_names = [item['name'] for item in all_item_lst_withprobability]
    chosen_item = random.choices(item_names, weights=probabilities, k=1)[0]
    return chosen_item

def random_rank_3(gacha_lst):
    for match in gacha_lst:
        if not match['name']:
            match['name'] = random.choices(rank_3_lst, k=1)[0]
            match['rank_type'] = '3'
            match['item_type'] = '武器'
    return gacha_lst

# start_id = '1600000000000000024'
# end_id   = '1670342760000470524' # 2022-12-07 00:10:59

# end_id_bottom = 4705
# end_id_  = '1702483560000397824' # 2023-12-14 00:25:42
def fill_id(gacha_lst):
    first_time = gacha_lst[0]['time']
    end_time = gacha_lst[-1]['time']
    # 这里的前缀不需要全部随机
    random_id_front_lst = random.sample(range(start_id_front, end_id_front), int(len(gacha_lst)/4))
    random_id_front_lst += random_id_front_lst*3
    random_id_front_lst.sort()
    if len(random_id_front_lst) != len(gacha_lst):
        offset = len(gacha_lst) - len(random_id_front_lst)
        if offset > 0:
            tmp = [random_id_front_lst[-1]]*offset
            random_id_front_lst += tmp
        else:
            random_id_front_lst = random_id_front_lst[:len(random_id_front_lst)-1+offset]

    random_id_bottom_lst = random.sample(range(0000, 9999), len(gacha_lst))
    random_id_bottom_lst.sort()
    for random_id_front, random_id_bottom, gacha in zip(random_id_front_lst, random_id_bottom_lst, gacha_lst):
        random_id_bottom = fill_num(str(random_id_bottom))
        random_id = '1' + str(random_id_front) + '0000' + random_id_bottom + '24'
        gacha['id'] = random_id
    return gacha_lst
def fill_num(string):
    if len(string) == 4:
        return string
    else:
        return fill_num('0' + string)

def fill_full_data(gacha_lst: List[dict], cur_dic: List[dict]):
    gacha_lst_fill = []
    index = 0
    for dic in cur_dic:
        if dic['name'] != '起始时间' and dic['name'] != '已抽未出数':
            gacha_lst_fill += gacha_lst[index:index + dic['fill_len']]
            # 五星id复制上一个的id
            tmp_dic = dic.copy()
            tmp_dic.pop('fill_len')
            tmp_dic['id'] = gacha_lst_fill[-1]['id']
            gacha_lst_fill.append(tmp_dic)
            index += dic['fill_len']
        elif dic['name'] == '已抽未出数' and dic['fill_len'] != 0:
            gacha_lst_fill += gacha_lst[index:]
    return gacha_lst_fill

def wirte_to_json(gacha_list, name):
    if not os.path.exists(join_(path_b, 'output')):
        os.makedirs(join_(path_b, 'output'))
    with open(join_(path_b, f'output\\{name}.json'), 'w', encoding='utf-8') as f:
        json.dump(gacha_list, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    #=============================================================================================
    # 加载角色，武器数据                                                                          
    # 数据需要更新时, 运行char_data_get.py获取原始数据, 然后运行parse_data_check.py 解析数据并规范化
    #=============================================================================================
    with open(join_(path_b, 'data_json\\char_data.json'), 'r', encoding='utf-8')as j,\
        open(join_(path_b, 'data_json\\weapon_data.json'), 'r', encoding='utf-8')as k:
        char_data = json.load(j)
        weapon_data = json.load(k)
        weapon_data_rank_4 = [x for x in weapon_data if x['data']]
        rank_3_lst = [x['name'] for x in weapon_data if not x['data']]
    
    print(f"当前数据更新到了: {char_data[0]['latest_version']}"
          "\n如果版本不正确请按顺序运行char_data_get.py和parse_data_check.py更新数据")
    input('按回车键继续')
    # 御三家
    char_lst = ['凯亚', '丽萨', '安伯']
    
    # 加载输入数据, 加载数据前请按照示例填写数据
    input_data_lst = parse_input_data(join_(path_b, 'input\\input.txt'))
    InputData_to_gacha_data(input_data_lst)

    # 概率
    UPprobability = 0.75
    Permanentprobability = 0.25
    Permanentprobability_ = 0.06
    
    #=============================================================================================
    # 设置项
    # 需要手动设置的id区间
    start_id_front = 60000000 # 起始id前缀
    end_id_front  = 67034276 # 结束id前缀
    
    target_pool = permanent_cur_char_dic # 目标池
    target_count_dic  = permanent_gacha_count_dic # 目标池中的物品数量字典
    target_gacha_type = '200' # 目标池type  100   200  301或400      302
    random_gacha = True       #              ^     ^      ^           ^
                              #           新手池 常驻池 角色限定池 武器限定池
    #=============================================================================================
    if random_gacha:
        # 按照时间区间随机每个物品的抽卡时间
        lst_momalized = nomalize_data(target_pool, target_gacha_type)
        gacha_rank34_lst = fill_data_to_uigf(lst_momalized)
        
        # luck_input=0.050249999999999975 # limited char 限定
        # luck_input=0.07950000000000007  # limited weapon 武器限定
        # luck_input=0.04159668117033296  # pp 常驻
        
        # 由于使用到了正向随机生成(也就是正向模拟抽卡逼近正确的抽卡数据), 
        # 需要先得到一个调优后的概率(原概率为0.051), 没有luck_input输入时会进行概率的计算并打印概率
        pp_bool = True if target_gacha_type == '200' else False
        gacha_rank34_fill_lst = random_rank_4(gacha_rank34_lst, target_count_dic, weapon_pool=False, 
                                              pp_bool=pp_bool, luck_input=0.04159668117033296)
        gacha_rank34_fill_lst = random_rank_3(gacha_rank34_fill_lst)
        gacha_rank34_fill_lst = fill_id(gacha_rank34_fill_lst)
        
        gacha_lst_final = fill_full_data(gacha_rank34_fill_lst, lst_momalized)
        wirte_to_json(gacha_lst_final, 'gacha_permanent')

    merge_data_bool = True
    if merge_data_bool:
        with open(join_(path_b, 'output\\gacha_limited_char.json'), 'r', encoding='utf-8')   as j, \
             open(join_(path_b, 'output\\gacha_limited_weapon.json'), 'r', encoding='utf-8') as k, \
             open(join_(path_b, 'output\\gacha_permanent.json'), 'r', encoding='utf-8')      as m:
            limited_char = json.load(j)
            limited_weapon = json.load(k)
            permanent = json.load(m)

        merge_data = limited_char + limited_weapon + permanent
        wirte_to_json(merge_data, 'gacha_merge')
    
    
