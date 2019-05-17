
# WxRobot/web微信机器人

- WxRobot 在 wxpy 的基础上，通过和Django进行结构，
- 打造出了web版的微信机器人，实现了丰富易用性，并可以自己进行扩展


### 演示站点
请自行注册账号体验
http://39.106.118.34

    | **强烈建议仅使用小号运行机器人！**

    | 使用机器人存在一定概率被限制登录的可能性。
    | 主要表现为无法登陆 Web 微信 (但不影响手机等其他平台)。



用来干啥
----------------

* 统计你的微信数据，并通过图形化界面展示出来
* 为你指定的好友定时发送消息 
* 程序自带四个插件：自动回复、图片搜索、天气预报、图片识别。
* 除了自带的几个插件外，还可以自己编写插件，然后上传到商店
* ...

总而言之，可用来实现各种微信个人号的自动化操作



目录说明
----------------
```
WxRobot 支持 Python 3.4-3.6 版本
databases 数据库目录 
helper  机器人核心代码 
homepage    后台交互 
initialize  初始化微信 
logintoRegister 登陆和注册 
Plugs   插件存放处
```

自定义插件
----------------
```
必须将程序写入到main函数里
:params msg 接收到的消息对象
:params plug_dir 插件所在的路径
:params fd2 用于将处理好的结果返回给用户
    - 由 类型 和 内容 两个部分组成，若 省略类型，将作为纯文本消息发送
    - 类型 部分可为: ‘@fil@’, ‘@img@’, ‘@msg@’, ‘@vid@’ (不含引号)
    - 分别表示: 文件，图片，纯文本，视频
    - 内容 部分可为: 文件、图片、视频的路径，或纯文本的内容
```
###### 例子
```
from wxpy import *
tuling = Tuling(api_key='91bfe84c2b2e437fac1cdb0c571cac91')
def main(msg,plug_dir,fd2):
    print('sdfsfsdfsdfsdf')
    print(plug_dir)
    # 图灵完成自动回复后使用管道将结果返回给父进程
    def reply_text(msg):
        text = tuling.reply_text(msg)
        fd2.send({'type':"@msg@",'content':text})
    reply_text(msg)
```

部分截图
----------------
登陆界面
![Image text](https://github.com/qiyuebuku/img-folder/blob/master/%E6%89%B9%E6%B3%A8%202019-05-17%20125000.png)
初始化微信
![Image text](https://github.com/qiyuebuku/img-folder/raw/master/%E6%89%B9%E6%B3%A8%202019-05-16%20202537.png)
数据统计
![Image text](https://github.com/qiyuebuku/img-folder/blob/master/%E6%89%B9%E6%B3%A8%202019-05-17%20125027.png)
插件中心
![Image text](https://github.com/qiyuebuku/img-folder/blob/master/%E6%89%B9%E6%B3%A8%202019-05-17%20125048.png)
定时发送
![Image text](https://github.com/qiyuebuku/img-folder/blob/master/%E6%89%B9%E6%B3%A8%202019-05-17%20125103.png)
好友管理 
![Image text](https://github.com/qiyuebuku/img-folder/blob/master/%E6%89%B9%E6%B3%A8%202019-05-17%20125305.png)

