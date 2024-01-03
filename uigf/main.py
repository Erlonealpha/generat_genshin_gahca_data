import os
import json
from typing import List, Dict, Set

samplejson = json.load(open('./samplejson.json', encoding='utf-8'))

print()
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
        self.contex = {
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

    def parse(self, info, list):
        self.info.uid = info['uid']
        self.info.lang = info['lang']
        self.info.export_time = info['export_time']
        self.info.export_timestamp = info['export_timestamp']
        self.info.export_app = info['export_app']
        self.info.export_app_version = info['export_app_version']
        self.info.uigf_version = info['uigf_version']

        self.list.gacha_type = list['gacha_type']
        self.list.time = list['time']
        self.list.name = list['name']
        self.list.item_type = list['item_type']
        self.list.rank_type = list['rank_type']
        self.list.id = list['id']
        self.list.uigf_gacha_type = list['uigf_gacha_type']



for key, val in samplejson.items():
    if key == "properties":
        info = val['info']["properties"]
        list = val['list']["items"]
        uigf = UigfJsonType()
        uigf.parse(info, list)

        