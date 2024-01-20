import json
import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
from os.path import basename as basename_

path_b = dirname_(abspath_(__file__))


with open(join_(path_b, 'output\\gacha-list_re_format.json'), 'w', encoding='utf-8')    as wf, \
     open(join_(path_b, 'output\\gacha_merge.json'), 'r', encoding='utf-8')    as f, \
     open(r"F:\2-Games tools\抽卡记录分析工具\Genshin impact\userData\item-id-dict.json", 'r', encoding='utf-8') as k:
    json_data = json.load(f)
    item_id_dict = json.load(k)
    for data in json_data['list']:
        match_id_pair = item_id_dict['lang'][0][1]
        match_id = [x[1] for x in match_id_pair if x[0] == data['name']]
        if match_id:
            match_id = match_id[0]
        data['item_id'] = match_id
    
    json.dump(json_data, wf, ensure_ascii=False, indent=2)