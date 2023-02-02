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
    'cookie': "buvid3=03B61D80-728A-F624-4E0A-A4B4B08E7A4337263infoc; LIVE_BUVID=AUTO2316286811743991; b_nut=100; CURRENT_FNVAL=4048; _uuid=610858735-9F16-F1095-3725-2910F29F10E2E666516infoc; rpdid=|(umRk|YRl~k0J'uY~k)R|Y~|; buvid_fp_plain=undefined; i-wanna-go-back=-1; buvid4=3BAB2F68-8053-2774-F523-69F10688E42868094-023010421-FRmBv7s/ltlUOUm2FQ5gBA==; b_ut=5; hit-new-style-dyn=0; hit-dyn-v2=1; nostalgia_conf=-1; bp_video_offset_29358975=752554467477422100; fingerprint=ae8f5a001194a29f7643be0a7c85e267; DedeUserID=3493123013479368; DedeUserID__ckMd5=fada9586cce73bf3; buvid_fp=b2d4152d6ca63e49af48acb0698c70a2; bp_video_offset_3493123013479368=757874514610618400; PVID=1; b_lsid=2E26CA31_18610A5E06F; SESSDATA=2fef4700,1690870678,fa1b8*22; bili_jct=36d263eb09bd0b095dd16d6d000e9be9; sid=qkuwihbh",
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
