from wxpy import *
tuling = Tuling(api_key='91bfe84c2b2e437fac1cdb0c571cac91')


def main(msg,fd2):
    # 图灵完成自动回复后使用管道将结果返回给父进程
    def reply_text(msg):
        text = tuling.reply_text(msg)
        fd2.send(text)
    reply_text(msg)