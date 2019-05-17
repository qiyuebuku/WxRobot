"""
必须将程序写入到main函数里
:params msg 接收到的消息对象
:params plug_dir 插件所在的路径
:params fd2 用于将处理好的结果返回给用户
    - 由 类型 和 内容 两个部分组成，若 省略类型，将作为纯文本消息发送
    - 类型 部分可为: ‘@fil@’, ‘@img@’, ‘@msg@’, ‘@vid@’ (不含引号)
    - 分别表示: 文件，图片，纯文本，视频
    - 内容 部分可为: 文件、图片、视频的路径，或纯文本的内容
"""

from wxpy import *
tuling = Tuling(api_key='91bfe84c2b2e437fac1cdb0c571cac91')

def main(msg,plug_dir,fd2):
    print(plug_dir)
    # 图灵完成自动回复后使用管道将结果返回给父进程
    def reply_text(msg):
        text = tuling.reply_text(msg)
        fd2.send({'type':"@msg@",'content':text})
    reply_text(msg)