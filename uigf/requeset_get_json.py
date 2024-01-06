import requests
import json
from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_
from os.path import basename as basename_

def get_json(url):
    response = requests.get(url)
    data = response.json()
    return data

game = 'genshin'
text = ''
lang = 'chs'

path_b = dirname_(abspath_(__file__))
url = f'https://api.uigf.org/dict/{game}/{lang}.json'
# url = f'https://api.uigf.org/identify/{game}/{text}'
data = get_json(url)
print()

with open(join_(path_b, 'item\\item_json.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=4))
request_body = {
    'game': game,
    'text': text,
    'lang': lang
}

