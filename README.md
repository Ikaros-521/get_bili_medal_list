# 前言
用于实现通过牌子逆向查主播信息这个功能。  
插件基于Nonebot2开发，链接：[https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo](https://github.com/Ikaros-521/nonebot_plugin_searchBiliInfo)  

## 目录结构
data.py数据源自vtbs.moe  
1.py用于爬取数据  
2.py用于中断时候的下标检索  
data_medal.py用于存储用户结果数据  

## API
`https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByUser?from=0&not_mock_enter_effect=1&room_id=` 传入主播的房间号，解析`json["data"]["medal"]["up_medal"]["medal_name"]`，即可。  


## 使用
安装相应的第三方库（aiohttp）后，`python 1.py` 即可。  
