import json, sys
import time
from functools import reduce

# data.py存储着从vtbs.moe获取的主播数据
from data import DATA

def delete_duplicate(data):
    func = lambda x, y: x + [y] if y not in x else x
    data = reduce(func, [[], ] + data)
    return data

# 最新的vtb数据
with open("ori_data.json", "r", encoding="utf8") as f:
    ori_data = json.load(f)

print("len(ori_data)=" + str(len(ori_data)))
print("len(DATA)=" + str(len(DATA)))

# 先合并 再去重
# new_data = DATA + ori_data
# print("len(new_data)=" + str(len(new_data)))

# DATA = delete_duplicate(new_data)
# print("duplicate len(DATA)=" + str(len(DATA)))

# 遍历 判断是否存在 后 尾部插入
num = 0
for temp_json in ori_data:
    if temp_json in DATA:
        continue
    else:
        # 追加入json
        DATA.append(temp_json)
        num += 1
        # print(temp_json)

print("add total num=" + str(num))

print("after len(DATA)=" + str(len(DATA)))

filename = 'data.py'
with open(filename, 'w', encoding="utf-8") as file_object:
    file_object.write("DATA=" + json.dumps(DATA, ensure_ascii=False))
file_object.close()
print("write " + filename + " over")
