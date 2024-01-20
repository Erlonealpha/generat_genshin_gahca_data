import random

def random_4rank(gacha_len: int, g4rank_len: int | None =None, luck_w_c: int=0.051):
                                        # 4星基础概率(角色和武器)
    luck_c_up = 0.5  # 4星up概率(抽到4星后为up角色的概率)
    up_luck = luck_w_c
    gacha_lst = []   # 抽取结果
    # 连续抽取3星数目
    consequent_3rank_count = 0
    
    gacha_num = 0    # 抽取次数
    while gacha_num < gacha_len - 2: # 抽卡次数-2
        try:
            if consequent_3rank_count == 9:
                consequent_3rank_count = 0
                one_gacha = random.choices([4,5], weights=[luck_c_up, luck_c_up], k=1)
                gacha_lst.append(one_gacha[0]) # 未up4星
            else:
                if consequent_3rank_count == 7:
                    luck_w_c = up_luck
                one_gacha = random.choices([3,4], weights=[1-luck_w_c, luck_w_c], k=1)
                if one_gacha[0] == 3: # 3星
                    gacha_lst.append(3)
                    consequent_3rank_count += 1
                else:
                    one_gacha = random.choices([4,5], weights=[luck_c_up, luck_c_up], k=1)
                    gacha_lst.append(one_gacha[0])

        finally:
            # 计数 复位基础概率
            gacha_num += 1
            if luck_w_c != luck_w_c:
                luck_w_c = luck_w_c
                
    # 保证第一和最后一抽为4星，避免出现合并数据后连接处出现大于10抽未出4星的情况
    one_gacha = random.choices([4,5], weights=[luck_c_up, luck_c_up], k=1)
    gacha_lst.insert(0, one_gacha)
    one_gacha = random.choices([4,5], weights=[luck_c_up, luck_c_up], k=1)
    gacha_lst.append(one_gacha[0])
    
    rank4_len = len([x for x in gacha_lst if x == 4 or x == 5])
    if g4rank_len:
        if g4rank_len == rank4_len:
            return gacha_lst
        elif g4rank_len > rank4_len and not abs(g4rank_len - rank4_len) > 6:
            replenish_count = g4rank_len - rank4_len
            rank3_index = []
            for i, x in enumerate(gacha_lst):
                if x ==3:
                    rank3_index.append(i)
            random_index_lst = random.sample(rank3_index, replenish_count)
            for i in random_index_lst:
                gacha_lst[i] = 4
            return gacha_lst
        else:
            return random_4rank(gacha_len=gacha_len, g4rank_len=g4rank_len, luck_w_c=luck_w_c-0.001)
    else:
        return rank4_len

# 选择性强化逼近概率生成
def chose_luck(ori_luck, stride, count, limit_count=300):
    if ori_luck < 7 and ori_luck > 6.5:
        luck = 0.066
    elif ori_luck < 6.5 and ori_luck > 6:
        luck = 0.077
    else:
        luck = 0.051
    gacha_num = stride
    limit_ = 0
    while limit_ < limit_count:
        try:
            num = 0
            for _ in range(count):
                num += random_4rank(gacha_num, luck_w_c=luck)
            luck_pred = gacha_num/(num/count)
            if abs(ori_luck - luck_pred) < 0.01:
                return luck
            elif ori_luck - luck_pred > 0:
                luck -= 0.00002
            elif ori_luck - luck_pred < 0:
                luck += 0.00002
        finally:
            limit_ += 1
            if limit_ > 10000:
                return luck

def chose_luck_np(ori_luck, stride, count, limit_count=300):
    if ori_luck < 7 and ori_luck > 6.5:
        luck = 0.066
    elif ori_luck < 6.5 and ori_luck > 6:
        luck = 0.077
    else:
        luck = 0.051
    
    gacha_num = stride
    limit_ = 0
    offset = 0.00002
    while limit_ < limit_count:
        try:
            num = 0
            for _ in range(count):
                num += random_4rank(gacha_num, luck_w_c=luck)
            luck_pred = gacha_num/(num/count)
            offset_pred = ori_luck - luck_pred
            
            ratio = offset_pred/0.001
            
            if abs(offset_pred) < 0.01:
                return luck
            elif offset_pred > 0:
                luck -= offset*ratio
            elif offset_pred < 0:
                luck += offset*ratio
        finally:
            limit_ += 1
    return luck

if __name__ == '__main__':
    # 统计df_gacha中的4星次数
    # from main import gacha_list
    # rank4_data = [gacha for gacha in gacha_list if gacha['rank_type'] == '4' and gacha['uigf_gacha_type'] == '301']
    # type_301 = len([x for x in gacha_list if x['uigf_gacha_type'] == '301'])
    # ori_luck = type_301 / len(rank4_data)
    # print(ori_luck, len(rank4_data) / type_301)
    ori_luck = 1315/177
    
    # luck = chose_luck(ori_luck, stride=100, count = 2500) # 0.049549999999999955
    # luck = chose_luck(ori_luck, stride=100, count = 2500) # 0.04959999999999996
    # gacha_lst = random_4rank(1315, g4rank_len=177, luck_w_c = 0.04959999999999996)
 
    random_4rank(1315, g4rank_len=177)
    
    chose_luck_np(ori_luck, 360, 250)
