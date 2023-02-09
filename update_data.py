import json, sys
import time
from functools import reduce

# data.py存储着从vtbs.moe获取的主播数据
from data.data import DATA

# 原始文件路径
src_file_path = "data/ori_data.json"
# 目标文件路径
tgt_file_path = "data/data.py"

def delete_duplicate(data):
    func = lambda x, y: x + [y] if y not in x else x
    data = reduce(func, [[], ] + data)
    return data

# 最新的vtb数据
with open(src_file_path, "r", encoding="utf8") as f:
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

# 数据写入本地喵
with open(tgt_file_path, 'w', encoding="utf-8") as file_object:
    file_object.write("DATA=" + json.dumps(DATA, ensure_ascii=False))
file_object.close()
print("write " + tgt_file_path + " over")
