from os.path import join as join_
from os.path import dirname as dirname_
from os.path import abspath as abspath_

import json

path_b = dirname_(abspath_(__file__))
def load_tmp_data(path):
    with open(path, 'r', encoding='utf-8')as f:
        
        lines = f.readlines()
        # i = 0
        # while i < len(lines):
        #     j = 0
        #     line_cont_1 = lines[i].split('\t')
        #     line_cont_2 = lines[i+1].split('\t')
        #     line_cont_3 = lines[i+2].split('\t')
        #     if line_cont_1[4] == '祈愿' or line_cont_1[4] == '限定祈愿':
        #         pass
        #     else:
        #         i+=3
        #         continue
        #     if line_cont_1[3] == '5星.png':
        #         rank_type = 5
        #     elif line_cont_1[3] == '4星.png':
        #         rank_type = 4
        #     elif line_cont_1[3] == '3星.png':
        #         rank_type = 3
        #         print('error')
        #     dic = {
        #         'name': line_cont_1[1],
        #         'type': line_cont_1[2],
        #         'rank_type': rank_type
        #     }
        #     lst.append(dic)
        #     i += 3
        contents = []
        first = True
        for i, line in enumerate(lines):
            if line.startswith('['):
                section_name = line.strip('[]\n')
                contents.append({
                    'section': section_name,
                    'indexL': i+1,
                    'indexR': None
                })
                if not first:
                    if contents[len(contents)-2]['indexL'] >= i-1:
                        contents[len(contents)-2]['indexR'] = contents[len(contents)-2]['indexL']
                    else:
                        contents[len(contents)-2]['indexR'] = i-1
                    
                first = False
            if i == len(lines)-1:
                contents[len(contents)-1]['indexR'] = i
        content_lst = []
        for content in contents:
            if not content['indexL'] == content['indexR']:
                content_lst.append({'name': content['section'],
                                    'context':lines[content['indexL']:content['indexR']], 
                                    })
        lst_vall = []
        for content in content_lst:
            lst = []
            cur_contents = [line.split('\t') for line in content['context'] if line.split('\t')[0].endswith('.png')]
            for cur_content in cur_contents:
                if cur_content[4] == '祈愿' or cur_content[4] == '限定祈愿':
                    pass
                else:
                    continue
                if cur_content[3] == '5星.png':
                    rank_type = 5
                    continue
                elif cur_content[3] == '4星.png':
                    rank_type = 4
                elif cur_content[3] == '3星.png':
                    rank_type = 3
                dic = {
                    'name': cur_content[1],
                    'type': cur_content[2],
                    'rank_type': rank_type
                }
                lst.append(dic)
            if lst:
                lst_vall.append({
                    "version": content['name'],
                    "context": lst})
    return lst_vall

tmp_data = load_tmp_data(join_(path_b, '..\\tmp\\tmp_data.txt'))
with open(join_(path_b, '..\\data_json\\weapon_data_with_version.json'), 'w', encoding='utf-8')as f:
    json.dump(tmp_data, f, ensure_ascii=False, indent=4)