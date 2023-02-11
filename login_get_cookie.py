import json
import asyncio
import aiohttp
import sys, re
from itertools import islice

header1 = {
    'content-type': 'application/x-www-form-urlencoded',
    "referer": "https://space.bilibili.com",
    "Origin": "https://space.bilibili.com",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 '
}

proxys = None

# 国家id转对应的cid
async def get_cid(country_id):
    with open("data/country.json", "r", encoding="utf8") as f:
        country_data = json.load(f)
    
    for common in country_data["data"]["common"]:
        if common["country_id"] == country_id:
            return common["id"]
    
    return 1

# 获取验证码相关信息
async def get_check():
    API_URL = 'https://passport.bilibili.com/x/passport-login/captcha?source=main_web'
    async with aiohttp.ClientSession(headers=header1) as session:
        try:
            async with session.get(url=API_URL, headers=header1, proxy=proxys) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()
        except aiohttp.ClientError as e:
            print(e)
            return {"code": -1}
            
    return ret


# 获取captcha_key喵
async def get_captcha_key(post_data):
    API_URL = 'https://passport.bilibili.com/x/passport-login/web/sms/send'
    async with aiohttp.ClientSession(headers=header1) as session:
        try:
            async with session.post(url=API_URL, headers=header1, proxy=proxys, data=post_data) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.json()
        except aiohttp.ClientError as e:
            print(e)
            return {"code": -400}
            
    return ret


# 登录
async def login(post_data):
    API_URL = 'https://passport.bilibili.com/x/passport-login/web/login/sms'
    async with aiohttp.ClientSession(headers=header1) as session:
        try:
            async with session.post(url=API_URL, headers=header1, proxy=proxys, data=post_data) as response:
                if response.status != 200:
                    response.raise_for_status()

                print("\n返回的cookie如下")
                print(response.cookies)
                
                ret = await response.json()
        except aiohttp.ClientError as e:
            print(e)
            return {"code": -400}
            
    return ret

async def main():
    banner = r"""
            \\         //
            \\       //
        #####################     ________   ___   ___        ___   ________   ___   ___        ___
        ##                 ##    |\   __  \ |\  \ |\  \      |\  \ |\   __  \ |\  \ |\  \      |\  \
        ##    //     \\    ##    \ \  \|\ /_\ \  \\ \  \     \ \  \\ \  \|\ /_\ \  \\ \  \     \ \  \
        ##   //       \\   ##     \ \   __  \\ \  \\ \  \     \ \  \\ \   __  \\ \  \\ \  \     \ \  \
        ##                 ##      \ \  \|\  \\ \  \\ \  \____ \ \  \\ \  \|\  \\ \  \\ \  \____ \ \  \
        ##       www       ##       \ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\
        ##                 ##        \|_______| \|__| \|_______| \|__| \|_______| \|__| \|_______| \|__|
        #####################
            \/         \/                               哔哩哔哩 (゜-゜)つロ 干杯~
    """

    # 获取captcha_key的传参
    post_data1 = {
        "cid": "86",
        "tel" : "0",
        "source" : "main-fe-header",
        "token" : "",
        "challenge" : "",
        "validate" : "",
        "seccode" : ""
    }
    # 登录传参
    post_data2 = {
        "cid": "86",
        "tel" : "0",
        "code" : 0,
        "source" : "main-fe-header",
        "captcha_key" : ""
    }

    print(banner + "\n")

    # 获取命令行传入的参数
    args = sys.argv

    # 输出命令行传入的参数
    # print(args)

    country_id = input("请输入手机的国家代码(不填默认 86)：")
    tel = input("请输入手机号码：")

    if country_id == "":
        # post_data1["cid"] = 1
        country_id = "86"

    # 获取下cid
    # post_data1["cid"] = await get_cid(country_id)
    post_data1["cid"] = country_id

    if tel == "":
        print("输入手机号啊！kora！")
        return
    else:
        post_data1["tel"] = tel

    print("[开始获取验证信息]")
    token_json = await get_check()
    print(json.dumps(token_json, indent=2, ensure_ascii=False))

    if token_json["code"] != 0:
        print("获取校验信息失败，取名为寄喵~")
        return

    try:
        post_data1["token"] = token_json["data"]["token"]
        gt = post_data1["challenge"] = token_json["data"]["geetest"]["gt"]
        post_data1["challenge"] = token_json["data"]["geetest"]["challenge"]

        print("\n请访问：http://geetest.colter.top/ 继续验证码的校验，获取validate和seccode")
        print("gt=\n" + gt)
        print("challenge=\n" + post_data1["challenge"])
        print("\n")

        # 传参 不传参则是普通模式；传入1个参数 任何内容，则定制优化模式
        if len(args) >= 2:
            validate_seccode = input("请输入快捷复制的validate&seccode：")
            match = re.search('validate=(.*)&seccode=(.*)', validate_seccode)
            validate = match.group(1)
            seccode = match.group(2)
        else:
            validate = input("请输入验证后的validate：")
            seccode = input("请输入验证后的seccode：")

        if validate == "" or seccode == "":
            print("空值是达咩的啦~如果验证失败，可以重新运行重试~")
            return

        post_data1["validate"] = validate
        post_data1["seccode"] = seccode

        print(json.dumps(post_data1, indent=2, ensure_ascii=False))
        print("[传参内容集齐啦！开冲！]\n")
        
        captcha_key_json = await get_captcha_key(post_data1)

        try:
            if captcha_key_json["code"] != 0:
                print("失败了喵~，请求返回如下")
                print(json.dumps(captcha_key_json, indent=2, ensure_ascii=False))
                return

            print("短信验证码发送成功！")
            print(json.dumps(captcha_key_json, indent=2, ensure_ascii=False))

            print("\n请在5分钟内完成验证哦~")
            code = input("请输入手机收到的验证码：")

            if code == "":
                print("空验证码？？？")
                return
            else:
                post_data2["code"] = code

            post_data2["cid"] = post_data1["cid"]
            post_data2["tel"] = post_data1["tel"]
            post_data2["captcha_key"] = captcha_key_json["data"]["captcha_key"]


            login_json = await login(post_data2)

            try:
                if login_json["code"] != 0:
                    print("\n登录失败喵~请求返回如下")
                    print(json.dumps(login_json, indent=2, ensure_ascii=False))
                    return
                
                # print(json.dumps(login_json, indent=2, ensure_ascii=False))

                print("\n登录成功！！！")

                if login_json["data"]["is_new"] == True:
                    print("新注册用户")
            except Exception as e:
                print(e)
                return

        except Exception as e:
            print(e)
            return


    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
