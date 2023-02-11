from bs4 import BeautifulSoup
import sys
import asyncio
import aiohttp

header1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.190.400 QQBrowser/11.5.5240.400'
}

country = [
    "usa", #美国
    "canada", #加拿大
    "united-kingdom", #英国
    "france", #法国
    "sweden", #瑞典
    "finland" #芬兰
]

# 判断是否存在重复数据的函数
def has_duplicate(filename, content):
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == content:
                return True
    return False


async def get_smstome_code(url):
    API_URL = url
    async with aiohttp.ClientSession(headers=header1) as session:
        try:
            async with session.get(url=API_URL, headers=header1) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.text()

                soup = BeautifulSoup(ret, 'html.parser')

                # print(soup)

                trs = soup.select('table.messagesTable tbody tr')
                for tr in trs[::-1]:
                    # print(tr)

                    from_td = tr.select_one('td:nth-of-type(1)')
                    from_value = from_td.text.strip()
                    received_td = tr.select_one('td:nth-of-type(2)')
                    received_value = received_td.text.strip()
                    message_td = tr.select_one('td:nth-of-type(3)')
                    message_value = message_td.text.strip()
                    # 针对b站的短信做了检索，不想要的话可以注释了
                    # code = message_value.split('[bilibili]')[-1]
                    print('From:', from_value)
                    print('Received:', received_value)
                    print('Code:', message_value)
                    print("\n")

                phone = url.split('/phone/')[1].split('/sms/')[0]
                print("号码：" + phone)
        except aiohttp.ClientError as e:
            print(e)
            return False
            
    return True


# 获取smstome.com的号码接受url，传入 url的国家路径
async def get_smstome_phone_list(country):
    API_URL = "https://smstome.com/country/" + country
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=API_URL) as response:
                if response.status != 200:
                    response.raise_for_status()
                ret = await response.text()

                soup = BeautifulSoup(ret, 'html.parser')

                count = 0

                file_path = "data/smstome_phone_list.txt"

                # 将href写入文件
                with open(file_path, 'a', encoding="utf-8") as file_object:
                    for a in soup.select('div.row div.column div.row div.row a'):
                        href = a['href']
                        count += 1
                        # print(href)
                        if not has_duplicate(file_path, href):
                            file_object.write(href + '\n')
                
                file_object.close()

                print("[smstome.com]" + country + " 获取href总数：" + str(count) + "\n写入数据至：" + file_path)
        except aiohttp.ClientError as e:
            print(e)
            return False
            
    return True
    

async def main():
    # 获取命令行传入的参数
    args = sys.argv

    # 输出命令行传入的参数
    print(args)

    # 传参 不传参则获取站点内所有的号码链接；传入1个参数 号码，则进行获取号码收到的短信
    if len(args) >= 2:
        phone = args[1]
    elif len(args) == 1:
        # 获取所有的号码链接
        for i in range(len(country)):
            ret = await get_smstome_phone_list(country[i])
    else:
        print("请传入手机号码")
        return

    file_path = "data/smstome_phone_list.txt"
    with open(file_path, 'r', encoding="utf-8") as file_object:
        for line in file_object:
            if "/" + phone + "/" in line:
                print(line)
                # tbody里面的数据没有拿到，大无语事件
                ret = await get_smstome_code(line)
                break
    file_object.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
