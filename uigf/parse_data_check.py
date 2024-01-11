from typing import List, Dict
import os
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
import re
import json

import pandas as pd

path_b = dirname_(abspath_(__file__))

with open(join_(path_b, 'tmp\\char_data_get.json'), 'r', encoding='utf-8') as f, \
    open(join_(path_b, 'tmp\\weapon_data_get.json'), 'r', encoding='utf-8') as g:
    char_data: List[dict] = json.load(f)
    weapon_data: List[dict] = json.load(g)

df_char_data = pd.DataFrame(char_data)
df_weapon_data = pd.DataFrame(weapon_data)

print(df_char_data.head())

