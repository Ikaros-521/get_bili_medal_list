import json, time
import asyncio
import aiohttp
import random


header1 = {
    'content-type': 'text/plain; charset=utf-8',
    'cookie': '',
    "referer": "https://www.douyin.com/user/MS4wLjABAAAABQgcUfPiVh1wRP5vUw3vub-oM_FzusGg1EezxpsFXvA",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.190.400 QQBrowser/11.5.5240.400'
}


async def get_info():
    API_URL = "https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAABQgcUfPiVh1wRP5vUw3vub-oM_FzusGg1EezxpsFXvA&max_cursor=1577456071000&locate_query=false&show_live_replay_strategy=1&count=10&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2048&screen_height=1152&browser_language=zh-CN&browser_platform=Win32&browser_name=QQBrowser&browser_version=11.5.5240.400&browser_online=true&engine_name=Blink&engine_version=94.0.4606.71&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=150&webid=7189962210821998095&msToken=GEQjT5xsClEUO01sAlGf6lpApHo7203hhR-cFhME6T9hO4mV36nvMTY1yfGRoWDUa8TeyaHyNgyfX-cuCaaxdg089TY1gIfScqpK8mrkU9yUvao7kg_4WXA_UOHjkYWN&X-Bogus=DFSzsdVE2TJANCklShc0ZKXAIQ22"


    # 可以不带cookie请求
    # header1["cookie"] = ""

    async with aiohttp.ClientSession(headers=header1) as session:
        try:
            async with session.get(url=API_URL, headers=header1, proxy=None) as response:
                if response.status != 200:
                    response.raise_for_status()
                print(await response.text())
                ret = await response.json()

                return ret
        except Exception as e:
            print(e)
            return None

    


async def main():
    json1 = await get_info()
    print(json1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())