import json, time
import asyncio
import aiohttp
import random

from config.config import CONFIG_JSON

header1 = CONFIG_JSON["header"]

# 代理地址，没有就改配置文件 proxy = []，或者直接 proxys = None
if len(CONFIG_JSON["proxy"]) == 0:
    proxys = None
else:
    proxys = CONFIG_JSON["proxy"][0]

# 存储关注的用户数据
user_info = []
# 写入文件路径
file_path = "data/ori_data.json"
# cookie总数
cookie_total_num = len(CONFIG_JSON["cookies"])
# cookie下标
cookie_index = 0

header1["cookie"] = CONFIG_JSON["cookies"][cookie_index]

# 获取用户信息，传入uid 获取 昵称 直播间号
async def get_user_info(uid):
    API_URL = "https://api.bilibili.com/x/space/wbi/acc/info?mid=" + str(uid)

    # 可以不带cookie请求，不过被ban后可以用带cookie解决问题
    # header1["cookie"] = ""

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
    global user_info, cookie_index, header1
    # 每多少个新数据 就写入文件
    write_num = 10
    # 起始的uid
    uid = 103507
    # 延时 秒
    wait_time = 0.5
    # 新数据计数
    num = 0
    # 每获取n个数据，进行一次睡眠
    sleep_every_num = 30
    # 每获取n个数据后 进行一次睡眠的秒数
    sleep_every_num_time = 3
    # 更换cookie前的等待时间
    change_ck_sleep_time = 10
    # cookie全寄后的重新循环的等待时间
    ck_die_sleep_time = 1200

    with open(file_path, "r", encoding="utf8") as f:
        user_info = json.load(f)
    f.close()

    print("len(user_info)=" + str(len(user_info)))

    while True:
        random_time = float(random.randint(0, 100) / 1000)
        json1 = await get_user_info(uid)
        uid += 1
        try:
            if json1["code"] != 0:
                print(json1)
                # print("异常中止运行")
                if json1["code"] == -401:
                    print("IP被禁 或 账号被限制请求，run")
                    with open(file_path, 'w', encoding="utf-8") as file_object:
                        file_object.write(json.dumps(user_info, ensure_ascii=False))
                    file_object.close()
                    print("写入 " + file_path + " 完毕, uid=" + str(uid - 1))

                    cookie_index += 1
                    if cookie_index < cookie_total_num:
                        print("等待" + str(change_ck_sleep_time) + "秒后 更换cookie")
                        await asyncio.sleep(change_ck_sleep_time)
                        header1["cookie"] = CONFIG_JSON["cookies"][cookie_index]
                        print("更换下一个cookie，下标=" + str(cookie_index))
                    else:
                        print("cookie全寄了，等待" + str(ck_die_sleep_time) + "秒后 重新循环")
                        # 等待
                        await asyncio.sleep(ck_die_sleep_time)
                        # 重头开始
                        cookie_index = 0
                        
                continue

            if "live_room" in json1["data"]:
                # print(json1["data"])
                if json1["data"]["live_room"] != None:
                    temp_json = {"mid": json1["data"]["mid"], "uname": json1["data"]["name"], "roomid": json1["data"]["live_room"]["roomid"]}
                else:
                    # print("没有直播间数据")
                    continue

                if temp_json in user_info:
                    print("已经存在此数据")
                    continue
                else:
                    user_info.append(temp_json)
                    num += 1
                    print(temp_json)
            else:
                print("不存在live_room")

            if num != 0 and num % write_num == 0:
                with open(file_path, 'w', encoding="utf-8") as file_object:
                    file_object.write(json.dumps(user_info, ensure_ascii=False))
                file_object.close()
                print("写入 " + file_path + " 完毕")

            if num != 0 and num % sleep_every_num == 0:
                print("新获取到" + str(sleep_every_num) + "个数据，睡眠" + str(sleep_every_num_time) + "秒")
                await asyncio.sleep(sleep_every_num_time)

            # print(random_time)
            await asyncio.sleep(wait_time + random_time)
        except (KeyError, TypeError, IndexError) as e:
            print(e)
            # print("异常中止运行")
            await asyncio.sleep(wait_time + random_time)
            continue


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())