import random

def random_4rank(gacha_len: int, g4rank_len: int | None =None, luck_w_c: int=0.051):
                                        # 4星基础概率(角色和武器)
    luck_c_up = 0.5  # 4星up概率(抽到4星后为up角色的概率)
    up_luck = luck_w_c
    gacha_lst = []   # 抽取结果
    # 连续抽取3星数目
    consequent_3rank_count = 0
    
    gacha_num = 0    # 抽取次数
    while gacha_num < gacha_len:
        try:
            if consequent_3rank_count == 9:
                consequent_3rank_count = 0
                one_gacha = random.choices([4,5], weights=[luck_c_up, luck_c_up], k=1)
                if one_gacha[0] == 4: # 4星保底
                    gacha_lst.append(4) # 未up4星
                elif one_gacha[0] == 5:
                    gacha_lst.append(5) # up4星角色
            else:
                if consequent_3rank_count == 7:
                    luck_w_c = up_luck
                one_gacha = random.choices([3,4], weights=[1-luck_w_c, luck_w_c], k=1)
                if one_gacha[0] == 3: # 3星
                    gacha_lst.append(3)
                    consequent_3rank_count += 1
                else:
                    one_gacha = random.choices([4,5], weights=[luck_c_up, luck_c_up], k=1)
                    if one_gacha[0] == 4:
                        gacha_lst.append(4)
                    elif one_gacha[0] == 5:
                        gacha_lst.append(5)
        finally:
            # 计数 复位基础概率
            gacha_num += 1
            if luck_w_c != luck_w_c:
                luck_w_c = luck_w_c
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
            return random_4rank(gacha_len=gacha_len, g4rank_len=g4rank_len, luck_w_c=luck_w_c)
    else:
        return rank4_len

# 选择性强化逼近概率生成
def chose_luck(ori_luck, stride, count, limit_count=100):
    luck = 0.051
    gacha_num = stride
    count = 1000
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
                luck -= 0.00005
            elif ori_luck - luck_pred < 0:
                luck += 0.00005
        finally:
            limit_ += 1
            if limit_ > 10000:
                return 0.051
        

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
    gacha_lst = random_4rank(1315, g4rank_len=177, luck_w_c = 0.04959999999999996)
