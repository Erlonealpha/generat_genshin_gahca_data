import json
import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
from os.path import basename as basename_

path_b = dirname_(abspath_(__file__))

with open(join_(path_b, 'data_json\\gacha-list-155275124.json'), 'r', encoding='utf-8') as f,\
     open(join_(path_b, 'output\\gacha_limited_char.json'), 'r', encoding='utf-8')   as j, \
     open(join_(path_b, 'output\\gacha_limited_weapon.json'), 'r', encoding='utf-8') as k, \
     open(join_(path_b, 'output\\gacha_permanent.json'), 'r', encoding='utf-8')      as m:
    json_data = json.load(f)
    limited_char = json.load(j)
    limited_weapon = json.load(k)
    permanent = json.load(m)

result = json_data['result']
gacha_301 = result[0]
gacha_302 = result[1]
gacha_200 = result[2]

def assemble_data(gacha_lst):
    return [
        [
            dic['time'], 
            dic['name'], 
            dic['item_type'], 
            int(dic['rank_type']), 
            dic['uigf_gacha_type'], 
            dic['id']
        ] 
            for dic in gacha_lst
    ]

limited_char_new = assemble_data(limited_char)
limited_weapon_new = assemble_data(limited_weapon)
permanent_new = assemble_data(permanent)

gacha_301_new = limited_char_new + gacha_301[1]
gacha_302_new = limited_weapon_new + gacha_302[1]
gacha_200_new = permanent_new + gacha_200[1]

final_301 = ['301', gacha_301_new]
final_302 = ['302', gacha_302_new]
final_200 = ['200', gacha_200_new]

json_data['result'][0] = final_301
json_data['result'][1] = final_302
json_data['result'][2] = final_200
with open(join_(path_b, 'output\\gacha-list-155275124.json'), 'w', encoding='utf-8') as wf:
    json.dump(json_data, wf, ensure_ascii=False, indent=2)

