import json
import asyncio
import aiohttp
import time


# 获取关注用户信息，传入uid 页码数 单数个数(最大50) 返回json内容
async def get_follows(uid, page_num, page_size):
    API_URL = "https://api.bilibili.com/x/relation/followings?vmid=" + str(uid) + \
        "&pn=" + str(page_num) + "&ps=" + str(page_size) + "&jsonp=jsonp"
    
    header1 = {
        'content-type': 'text/plain; charset=utf-8',
        # 下方填入你的cookie喵
        'cookie': "",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'
    }

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

async def main():
    print("run over")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())