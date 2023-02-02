import json
import asyncio
import aiohttp
import time

header1 = {
    'content-type': 'text/plain; charset=utf-8',
    # 下方填入你的cookie喵
    'cookie': "",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
}

# 存储关注的用户数据
user_info = []

# 获取关注用户信息，传入uid 页码数 单数个数(最大50) 返回json内容
async def get_follows(uid, page_num, page_size):
    API_URL = "https://api.bilibili.com/x/relation/followings?vmid=" + str(uid) + \
        "&pn=" + str(page_num) + "&ps=" + str(page_size) + "&jsonp=jsonp"

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


# 传入uid获取用户直播间房间号
async def get_room_id(uid):
    try:
        API_URL = 'https://api.live.bilibili.com/room/v2/Room/room_id_by_uid?uid=' + uid
        async with aiohttp.ClientSession(headers=header1) as session:
            async with session.get(url=API_URL, headers=header1) as response:
                ret = await response.json()
        
        try:
            room_id = ret['data']['room_id']
        except TypeError:
            return 0
            
        return room_id
    except aiohttp.ClientError as e:
        return 0


async def main():
    # 填入你的uid
    uid = "3493123013479368"

    num = -1
    page_size = 50

    while True:
        num += 1
        json1 = await get_follows(uid, (num + 1), page_size)
        try:
            if json1["code"] != 0:
                print(json1)
                print("异常中止运行")
                return

            for data in json1["data"]["list"]:
                temp_json = {"mid": data["mid"], "uname": data["uname"], "roomid": 0}
                user_info.append(temp_json)
            
            if len(json1["data"]["list"]) < 50:
                # print(user_info)
                print(len(user_info))

                temp_user_info = []

                num = 0
                for data in user_info:
                    room_id = await get_room_id(str(data["mid"]))
                    data["roomid"] = room_id
                    temp_user_info.append(data)

                    num += 1
                    print("get room_id num " + str(num))
                    await asyncio.sleep(0.1)

                filename = 'follows.json'
                with open(filename, 'w', encoding="utf-8") as file_object:
                    file_object.write(json.dumps(temp_user_info, ensure_ascii=False))
                file_object.close()
                print("write " + filename + " over")

                return
            
            print("get " + str(num + 1) + " page data")
            await asyncio.sleep(0.1)
        except (KeyError, TypeError, IndexError) as e:
            print(e)
            print("异常中止运行")
            return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())