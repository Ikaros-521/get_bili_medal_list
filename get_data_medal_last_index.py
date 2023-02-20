from data.data import DATA
from data.data_medal import DATA_MEDAL

# 存储下标
index = -1
json1 = DATA_MEDAL[-1]
print(json1)
key = list(json1.keys())[0]
print("DATA_MEDAL last key=" + key)
print("DATA_MEDAL len=" + str(len(DATA_MEDAL)))

# 获取已经加载的最后一个的牌子所对应的data下标喵
for data in DATA:
    # print(data)
    try:
        index += 1
        if data["mid"] == json1[key]["mid"]:
            print("index=" + str(index))
            break
    except KeyError as e:
        print(e)
        continue