import json
import asyncio
import aiohttp
import random

header1 = {
    'content-type': 'text/plain; charset=utf-8',
    # 下方填入你的cookie喵
    'cookie': "",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 '
}

# 代理地址，没有就改成 proxys = None
proxys = "http://127.0.0.1:10811"

# 存储关注的用户数据
user_info = []

# 获取用户信息，传入uid 获取 昵称 直播间号
async def get_user_info(uid):
    API_URL = "https://api.bilibili.com/x/space/wbi/acc/info?mid=" + str(uid)

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
            async with session.get(url=API_URL, headers=header1) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()

    return ret


async def main():
    global user_info
    # 每多少个新数据 就写入文件
    write_num = 10
    # 起始的uid
    uid = 1903
    # 延时 秒
    wait_time = 1
    # 新数据计数
    num = 0
    filename = "ori_data2.json"

    with open(filename, "r", encoding="utf8") as f:
        user_info = json.load(f)

    print("len(user_info)=" + str(len(user_info)))

    while True:
        json1 = await get_user_info(uid)
        uid += 1
        try:
            if json1["code"] != 0:
                print(json1)
                # print("异常中止运行")
                if json1["code"] == -401:
                    print("IP被禁 或 账号被限制请求，run")
                    return
                continue

            if "live_room" in json1["data"]:
                temp_json = {"mid": json1["data"]["mid"], "uname": json1["data"]["name"], "roomid": json1["data"]["live_room"]["roomid"]}
                
                if temp_json in user_info:
                    continue
                else:
                    user_info.append(temp_json)
                    num += 1

            if num != 0 and num % write_num == 0:
                with open(filename, 'w', encoding="utf-8") as file_object:
                    file_object.write(json.dumps(user_info, ensure_ascii=False))
                file_object.close()
                print("write " + filename + " over")

            random_time = float(random.randint(0, 100) / 1000)
            # print(random_time)
            await asyncio.sleep(wait_time + random_time)
        except (KeyError, TypeError, IndexError) as e:
            print(e)
            # print("异常中止运行")
            continue


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())