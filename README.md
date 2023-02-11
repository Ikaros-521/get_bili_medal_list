# 前言
用于实现通过牌子逆向查主播信息这个功能。  
插件基于Nonebot2开发，链接：[https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo](https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo)  

## 目录结构

`get_all_user_info.py` 爬取全b站用户数据，数据写入ori_data.json  
`update_data_medal.py` 用于获取主播牌子信息写入data_medal.py  
`get_data_medal_last_index.py` 用于获取已经加载的最后一个的牌子所对应的data下标  
`update_data.py` 用于将新的vtbs.moe的主播数据，追加入旧的data.py中  

`data/ori_data.json` 存储最新获取的vtbs.moe的主播数据  
`data/new_data.py` 测试用data.py的备份文件  
`data/data.py` 数据源自vtbs.moe + 爬虫追加  
`data/data_medal.py` 用于存储用户结果数据  
`data/follows.json` 爬取的个人关注数据，存储文件  
`data/country.json` 存储各国号码信息  
`data/smstome_phone_list.txt` 存储从smstome爬取的所有的号码接收链接  

`config/config.py` 配置请求头，填入你的cookie，或者代理地址  


## API

`https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByUser?from=0&not_mock_enter_effect=1&room_id=` 传入主播的房间号，解析`json["data"]["medal"]["up_medal"]["medal_name"]`，即可。  


## 使用
  
### 1、爬取全b站用户uid、昵称、直播间号
`python get_all_user_info.py` 运行，爬取的数据写入`ori_data2.json`  

### 2、依赖ori_data.json生成data.py
将待加入的新数据写入`ori_data.json`  
运行`python update_data.py`  

### 3、获取data_medal.py相关信息-最后一个数据下标
`python get_data_medal_last_index.py` 

### 4、依赖data.py生成data_medal.py的牌子数据
编辑`update_data_medal.py`, header1的"cookie" 填入你b站的cookie，步骤3输出的index填入`start_index`(默认自动执行第三步)  
安装相应的第三方库（aiohttp）后，`python update_data_medal.py` 即可。  

## 获取Cookie

### 1、浏览器获取
浏览器登录b站，F12抓包，找请求里带cookie的，复制`SESSDATA`到`config.py`文件。  

### 2、使用biliup软件
项目根目录运行`.\biliup\biliup.exe login`，登录账号，生成`cookie.json`文件，复制里面的`SESSDATA`到`config.py`文件。  

### 3、使用login_get_cookie.py短信登录程序获取
项目根目录运行`python login_get_cookie.py`，根据提示完成短信验证登录。  
期间需要访问[http://geetest.colter.top/](http://geetest.colter.top/)，传入`gt`和`challenge`完成手动的极验校验，获取`validate`和`seccode`。  
最后需要填入手机验证码完成登录即可。  
ps：`python login_get_cookie.py 1`，优化了`validate`和`seccode`的输入，请自行选择执行。  

# 拓展

## 免费接码平台

### [smstome.com](https://smstome.com) 
1、执行`python sms.py`，获取站点所有号码的短信接收链接，存储于`data/smstome_phone_list.txt`  
2、执行`python sms.py 12345678`，后面传入的是号码，获取此号码接收到的最新的2条短信。  

# 参考
[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)  