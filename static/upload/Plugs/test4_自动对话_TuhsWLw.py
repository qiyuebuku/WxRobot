# coding:utf-8
import json
import requests
from wxpy import *


# bot = Bot()
# bot.file_helper.send_image('ParticleSmoke.png')

# 回复 my_friend 发送的消息
# @bot.register(my_friend)
# def reply_my_friend(msg):
#    return 'received: {} ({})'.format(msg.text, msg.type)

# 回复发送给自己的消息，可以使用这个方法来进行测试机器人而不影响到他人
# @bot.register(bot.self, except_self=False)
# def reply_self(msg):
#   return 'received: {} ({})'.format(msg.text, msg.type)

# 打印出所有群聊中@自己的文本消息，并自动回复相同内容
# 这条注册消息是我们构建群聊机器人的基础
# @bot.register(Group, TEXT)
# def print_group_msg(msg):
#    if msg.is_at:
#        print(msg)
#        msg.reply(meg.text)
import os 

import pickle

# fp = open()
print()

def auto_ai(text):
    url = "http://www.tuling123.com/openapi/api"
    api_key = "91bfe84c2b2e437fac1cdb0c571cac91"
    payload = {
        "key": api_key,
        "info": text,
        "userid": "666"
    }
    r = requests.post(url, data=json.dumps(payload))
    result = json.loads(r.content)
    if ('url' in result.keys()):

        return result["text"] + result["url"]
        # return "[丽丽机器人]  " + result["text"] + result["url"]
        
    else:
        return  result["text"]
        # return "[雨阳]  " + result["text"]
        

# bot = Bot(cache_path=True)  # 登录缓存
# bot.file_helper.send('[奸笑][奸笑]')
bot = Bot()   #定义一个微信机器人
bot.enable_puid('wxpy_puid.pkl')
friends = bot.friends(update=False)   #获取更新好友列表
print('机器人已经启动')
# boring_group1 = bot.friends().search('逝语')[0]  #只对某个特定的角色回复
boring_group1 = bot.friends()  #对所有人回复
dir(bot)
print(bot.user_details(bot.self))


@bot.register(boring_group1)
def group_message(msg):
    print('[接收]' + str(msg))

    if (msg.type != 'Text'):
        ret = '[奸笑][奸笑]'
    else:
        ret = auto_ai(msg.text)
    print('[发送]' + str(ret))
    return ret



@bot.register(chats=[Friend])
def forward_message(msg):
    print('[接收]' + str(msg))

    if (msg.type != 'Text'):
        ret = '[奸笑][奸笑]'
    else:
        ret = auto_ai(msg.text)
    print('[发送]' + str(ret))
    return ret

embed()


