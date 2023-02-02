import json
import asyncio
import aiohttp
import time
from itertools import islice

# data.py存储着从vtbs.moe获取的主播数据
from data import DATA
# data_medal.py用于存储获取的主播牌子信息
from data_medal import DATA_MEDAL

# 用于存储牌子数据
data_medal_json = DATA_MEDAL
# 请求头
header1 = {
    'content-type': 'text/plain; charset=utf-8',
    # 下方填入你的cookie喵
    'cookie': "",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
}
# 计数用
num = 0
# 数据起始下标
start_index = 4851
# 每获得1个新数据 就写入一次文件
write_every_num = 1

# 获取主播牌子信息 传入主播房间号
async def get_medal(roomid):
    global header1

    API_URL = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByUser?from=0&not_mock_enter_effect=1&room_id=' + str(roomid)
    async with aiohttp.ClientSession(headers=header1) as session:
        try:
            async with session.get(url=API_URL, headers=header1) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()
        except aiohttp.ClientError as e:
            print(e)
            # 睡眠个3s
            await asyncio.sleep(3)
            # 重试一次
            async with session.get(url=API_URL, headers=header1) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()
            
    return ret


async def main():
    global data_medal_json, num

    # print(type(DATA))

    index = start_index - 1

    # 遍历本地vtb数据 第二个参数的起始值，跳过前n个数据(这个下标可以通过2.py获取已加载到的下标)
    for data in islice(DATA, start_index, None):
        index += 1
        # print(data)

        try:
            roomid = data["roomid"]
        except (KeyError, TypeError, IndexError) as e:
            print("[" + str(index) + "] " + str(e))
            continue

        if roomid == 0:
            continue

        # 睡眠个0.5s
        await asyncio.sleep(0.3)
        json1 = await get_medal(roomid)
        # print(json1)
        try:
            if json1["code"] != 0:
                print("[" + str(index) + "] " + json1)
                continue

            # 获取牌子名
            medal_name = str(json1["data"]["medal"]["up_medal"]["medal_name"])
            # 拼接新的json串
            temp_json = { medal_name: data }
            try:
                # 判断是否已经存在
                if temp_json in DATA_MEDAL:
                    # print("已存在 " + medal_name + " 跳过")
                    continue
                else:
                    # 追加入json
                    data_medal_json.append(temp_json)
            except (KeyError, TypeError, IndexError) as e:
                print("[" + str(index) + "] " + str(e))
                continue
            # 计数+1
            num += 1
            print("[" + str(index) + "] " + "获取牌子名：" + medal_name)

            # 每获取write_every_num个结果 写入一次数据文件
            if num % write_every_num == 0 and num != 0:
                filename = 'data_medal.py'
                with open(filename, 'w', encoding="utf-8") as file_object:
                    file_object.write("DATA_MEDAL = " + json.dumps(data_medal_json, ensure_ascii=False))
                file_object.close()
                print("num=" + str(num) + ", 写入" + filename)
        except (KeyError, TypeError, IndexError) as e:
            print("[" + str(index) + "] " + str(e))
            continue

    filename = 'data_medal.py'
    with open(filename, 'w', encoding="utf-8") as file_object:
        file_object.write("DATA_MEDAL = " + json.dumps(data_medal_json, ensure_ascii=False))
    file_object.close()
    print("num=" + str(num) + ", 写入" + filename)
    print("数据爬取完毕了，收工回家~")


if __name__ == "__main__":
    asyncio.run(main())
