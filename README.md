# 前言
用于实现通过牌子逆向查主播信息这个功能。  
插件基于Nonebot2开发，链接：[https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo](https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo)  

## 目录结构

get_all_user_info.py 爬取全b站用户数据，数据写入ori_data.json  
update_data_medal.py 用于获取主播牌子信息写入data_medal.py  
get_data_medal_last_index.py 用于获取已经加载的最后一个的牌子所对应的data下标  
update_data.py 用于将新的vtbs.moe的主播数据，追加入旧的data.py中  

data/ori_data.json 存储最新获取的vtbs.moe的主播数据  
data/new_data.py 测试用data.py的备份文件  
data/data.py 数据源自vtbs.moe + 爬虫追加  
data/data_medal.py 用于存储用户结果数据  
data/follows.json 爬取的个人关注数据，存储文件  

config/config.py 配置请求头，填入你的cookie  


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
