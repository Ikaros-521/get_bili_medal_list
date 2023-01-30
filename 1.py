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
    'cookie': "buvid3=FA0A27F9-013A-565C-E786-460DBC0B099794205infoc; b_nut=1672812193; _uuid=D8D2107A5-D9410-1054E-8CB2-26F45B6E895201028infoc; buvid_fp_plain=undefined; i-wanna-go-back=-1; hit-new-style-dyn=0; hit-dyn-v2=1; dy_spec_agreed=1; LIVE_BUVID=AUTO6516729151672170; CURRENT_FNVAL=4048; rpdid=|(umRk|YRl~k0J'uY~kmJRJJu; buvid4=01EACFC4-6188-B683-B4A1-B144212C238B75877-022041118-8pvL0cFl5EhNFD0%2BiK411w%3D%3D; nostalgia_conf=-1; bp_video_offset_6170679=755481504860078100; bp_video_offset_679213705=755746431342477300; b_ut=5; bp_video_offset_3493128476560053=undefined; SESSDATA=85f628b1%2C1690369264%2C9c91f%2A12; bili_jct=3716d26cc36474b1128cfb9471653241; DedeUserID=3493128470268708; DedeUserID__ckMd5=6bbc6ae7979550ee; CURRENT_QUALITY=16; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1674737770,1674824526,1674911822,1674980056; PVID=1; bp_video_offset_3493128470268708=756588562745393300; innersign=1; fingerprint=248884ebea92ed37387eceeee20bcf48; sid=5qyjne5r; b_lsid=7894F3210_1860154250E; buvid_fp=248884ebea92ed37387eceeee20bcf48",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
}
# 计数用
num = 0

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

    # 遍历本地vtb数据 第二个参数的起始值，跳过前n个数据(这个下标可以通过2.py获取已加载到的下标)
    for data in islice(DATA, 4849, None):
        print(data)

        try:
            roomid = data["roomid"]
        except (KeyError, TypeError, IndexError) as e:
            print(e)
            continue

        if roomid == 0:
            continue

        # 睡眠个0.5s
        await asyncio.sleep(0.5)
        json1 = await get_medal(roomid)
        # print(json1)
        try:
            if json1["code"] != 0:
                print(json1)
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
                print(e)
                continue
            # 计数+1
            num += 1
            print("获取牌子名：" + medal_name)

            # 每获取10个结果 写入一次数据文件
            if num % 10 == 0 and num != 0:
                filename = 'data_medal.py'
                with open(filename, 'w', encoding="utf-8") as file_object:
                    file_object.write("DATA_MEDAL = " + json.dumps(data_medal_json, ensure_ascii=False))
                file_object.close()
                print("num=" + str(num) + ", 写入" + filename)
        except (KeyError, TypeError, IndexError) as e:
            print(e)
            continue

    filename = 'data_medal.py'
    with open(filename, 'w', encoding="utf-8") as file_object:
        file_object.write("DATA_MEDAL = " + json.dumps(data_medal_json, ensure_ascii=False))
    file_object.close()
    print("num=" + str(num) + ", 写入" + filename)
    print("数据爬取完毕了，收工回家~")


if __name__ == "__main__":
    asyncio.run(main())
