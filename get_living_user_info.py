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

# 获取分区id为area_id的 第page页的 正在直播中的用户信息
async def get_live_list_info(area_id, page):
    API_URL = "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=" + \
        str(area_id)  + "&page=" + str(page)

    # 可以不带cookie请求
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
    # 延时 秒
    wait_time = 1
    # 分区id表
    area_ids = [1, 2, 3, 5, 6, 9, 10, 11, 13, 300]
    # 临时修改用
    area_ids = [1, 2, 3, 5, 6, 9, 10, 11, 13, 300]
    # 分区id 下标
    area_id_index = 0
    # 起始页数
    page = 1

    with open(file_path, "r", encoding="utf8") as f:
        # user_info = json.load(f)
        user_info = json.loads(f.read())

    f.close()

    print("len(user_info)=" + str(len(user_info)))
    print("———— 开始获取分区id=" + str(area_ids[area_id_index]) + "的数据")

    while True:
        random_time = float(random.randint(0, 100) / 1000)
        json1 = await get_live_list_info(area_ids[area_id_index], page)

        page += 1

        try:
            if json1["code"] != 0:
                print(json1)
                # print("异常中止运行")
                if json1["code"] == -401:
                    print("IP被禁 或 账号被限制请求，run")

                return

            if "list" in json1["data"]:
                # print(json1["data"])
                if json1["data"]["list"] == None:
                    print("没有直播间数据")

                    if area_id_index == (len(area_ids) - 1):
                        print("所有分区获取完毕，收工~")    
                        return
                    else:
                        area_id_index += 1
                        page = 1
                        print("———— 开始获取分区id=" + str(area_ids[area_id_index]) + "的数据")
                        continue

                for data in json1["data"]["list"]:
                    temp_json = {"mid": data["uid"], "uname": data["uname"], "roomid": data["roomid"]}

                    if temp_json in user_info:
                        # print("已经存在此数据 " + data["uname"])
                        print(".", end="", flush=True)
                    else:
                        user_info.append(temp_json)
                        # print(temp_json)
                        print("+", end="", flush=True)
                
                with open(file_path, 'w', encoding="utf-8") as file_object:
                    file_object.write(json.dumps(user_info, ensure_ascii=False))
                file_object.close()
                # print("写入 " + file_path + " 完毕")
                print("|", end="", flush=True)

                # 不足20说明到底了
                if len(json1["data"]["list"]) < 20:
                    print("此分区数据获取完毕")

                    if area_id_index == (len(area_ids) - 1):
                        print("所有分区获取完毕，收工~")    
                        return
                    else:
                        area_id_index += 1
                        page = 1
                        print("———— 开始获取分区id=" + str(area_ids[area_id_index]) + "的数据")
                        continue

                # print(random_time)
                await asyncio.sleep(wait_time + random_time)
        except Exception as e:
            print(e)
            return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())