import json
import asyncio
import aiohttp
import time
from itertools import islice

# data.py存储着从vtbs.moe获取的主播数据
from data.data import DATA
# data_medal.py用于存储获取的主播牌子信息
from data.data_medal import DATA_MEDAL
# 配置文件
from config.config import CONFIG_JSON

# 获取主播牌子信息 传入主播房间号
async def get_medal(roomid):
    API_URL = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByUser?from=0&not_mock_enter_effect=1&room_id=' + str(roomid)
    async with aiohttp.ClientSession(headers=header1) as session:
        try:
            async with session.get(url=API_URL, headers=header1, proxy=proxys) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()
        except aiohttp.ClientError as e:
            print(e)
            # 睡眠个3s
            await asyncio.sleep(3)
            # 重试一次
            async with session.get(url=API_URL, headers=header1, proxy=proxys) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()
            
    return ret


# 获取data_medal数据的最后一个下标
def get_data_medal_last_index():
    print("获取data_medal数据的最后一个下标")
    # 存储下标
    index = -1
    json1 = DATA_MEDAL[-1]
    print(json1)
    key = list(json1.keys())[0]
    # print("key=" + key)

    # 获取已经加载的最后一个的牌子所对应的data下标喵
    for data in DATA:
        # print(data)
        try:
            index += 1
            if data["mid"] == json1[key]["mid"]:
                print("last_index=" + str(index))
                return index
        except Exception as e:
            print(e)
            continue

    return 0


async def main():
    global data_medal_json, num, sleep_time

    sleep_time = float(sleep_time)

    # print(type(DATA))

    index = start_index - 1

    # 遍历本地vtb数据 第二个参数的起始值，跳过前n个数据(这个下标可以通过2.py获取已加载到的下标)
    for data in islice(DATA, start_index, None):
        index += 1
        # print(data)

        try:
            roomid = data["roomid"]
        except (KeyError, TypeError, IndexError) as e:
            print("[" + str(index) + "] 解析不到roomid " + str(e))
            # 睡眠
            await asyncio.sleep(sleep_time)
            continue

        # print("roomid=" + str(roomid))

        # 睡眠
        await asyncio.sleep(sleep_time)

        if roomid == 0:
            continue

        json1 = await get_medal(roomid)
        # print(json1)
        try:
            if json1["code"] != 0:
                print("[" + str(index) + "] " + json.dumps(json1, ensure_ascii=False))
                continue

            # print(json1["data"]["medal"]["up_medal"])
            if json1["data"]["medal"]["up_medal"] == None:
                print("[" + str(index) + "] 无牌子信息 ")
                continue

            # 获取牌子名
            medal_name = str(json1["data"]["medal"]["up_medal"]["medal_name"])

            # 拼接新的json串
            temp_json = { medal_name: data }
            try:
                # 判断是否已经存在
                if temp_json in DATA_MEDAL:
                    print("已存在 " + medal_name + " 跳过")
                    continue
                else:
                    # 追加入json
                    data_medal_json.append(temp_json)
            except (KeyError, TypeError, IndexError) as e:
                print("[" + str(index) + "] 追加入data_medal_json失败 " + str(e))
                continue
            # 计数+1
            num += 1
            print("[" + str(index) + "] " + "获取牌子名：" + medal_name)

            # 每获取write_every_num个结果 写入一次数据文件
            if num % write_every_num == 0 and num != 0:
                with open(file_path, 'w', encoding="utf-8") as file_object:
                    file_object.write("DATA_MEDAL = " + json.dumps(data_medal_json, ensure_ascii=False))
                file_object.close()
                print("num=" + str(num) + ", 写入" + file_path)
        except (KeyError, TypeError, IndexError) as e:
            print("[" + str(index) + "] " + str(e))
            continue

    with open(file_path, 'w', encoding="utf-8") as file_object:
        file_object.write("DATA_MEDAL = " + json.dumps(data_medal_json, ensure_ascii=False))
    file_object.close()
    print("num=" + str(num) + ", 写入" + file_path)
    print("数据爬取完毕了，收工回家~")


if __name__ == "__main__":
    # 用于存储牌子数据
    data_medal_json = DATA_MEDAL

    header1 = CONFIG_JSON["header"]

    # 代理地址，没有就改配置文件 proxy = []，或者直接 proxys = None
    if len(CONFIG_JSON["proxy"]) == 0:
        proxys = None
    else:
        proxys = CONFIG_JSON["proxy"][0]

    # 计数用
    num = 0
    # 数据起始下标
    start_index = 0
    # 每获得1个新数据 就写入一次文件
    write_every_num = 10
    # 请求间隔延时
    sleep_time = 1
    # 写入文件路径
    file_path = "data/data_medal.py"

    # 自动获取最后一个的下标 错乱了的话 建议手动填写
    start_index = get_data_medal_last_index()

    print("当前牌子总数：" + str(len(DATA_MEDAL)))
    print("当前用户数据总数：" + str(len(DATA)))

    print("开始获取牌子数据")
    asyncio.run(main())
