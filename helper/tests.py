<<<<<<< HEAD
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

        return "[小晓]  " + result["text"] + result["url"]
    else:
        return "[小晓]  " + result["text"]


def get_analysis_result(Bot):
        # 获取所有好友
        friends_count = len(Bot.friends(update=True))
        # 一些不活跃的群可能无法被获取到，可通过在群内发言，或修改群名称的方式来激活
        groups_count = len(Bot.groups(update=True))
        msp_count = len(Bot.mps(update=True))
        gender_statistics = {'male':len(friends.search(sex=MALE)),'female':len(friends.search(sex=FEMALE)),'secrecy':len(friends.search(sex=None))}
        print(gender_statistics)
        signatures = {i.name:i.signature for i in friends}
        region={}
        for f in friends:
            region[f.name] = f.city if f.city else f.province

def groups_and_friends_info(bot):
    # # 获取puid
    # puid = request.session.get('puid')
    # # 获取用户的bot对象
    # bot = aom.get_bot_dict(puid).get('bot')
    groups = bot.groups(update = True)
    friends = bot.friends(update=True)
    ug_info = []

    for group in groups:
        group.update_group(True)

        gname = group.name
        # print("群名称：",gname)

        gowner = group.owner.name  #群主
        # print("群主：",gowner)

        #所有群成员
        members = group.members 
        # print("群内成员：",group.members) 

        # 统计性别
        mtfratio = {'male':len(members.search(sex=MALE)),'female':len(members.search(sex=FEMALE)),'secrecy':len(members.search(sex=None))}
        # print(mtfratio)

        pcount = len(members)  #群成员数量
        ug_info.append({'gname':gname,'gowner':gowner,'pcount':pcount,'mtfratio':mtfratio})
    print(ug_info)



# bot = Bot(cache_path=True)  # 登录缓存
# bot.file_helper.send('[奸笑][奸笑]')
bot = Bot(cache_path = True)   #定义一个微信机器人
bot.enable_puid('wxpy_puid.pkl')

print(bot.alive)
# groups_and_friends_info(bot)
friends = bot.friends()   #获取更新好友列表
print(friends.__len__())
for i in friends:
    print(i.puid)

groups = bot.groups()
for i in groups:
    print(i.puid)

print(friends.search(puid = "c48a6698"))
print(groups.search(puid = "11d1c2d7"))

# print('机器人已经启动')
# print("我的所有好友",friends)
# get_analysis_result(bot)

 
# chats = bot.chats(update=False) # 获取所有聊天对象
# print("我的所有聊天对象",chats)
# boring_group1 = bot.friends().search('逝语')[0]  #只对某个特定的角色回复
boring_group1 = bot.friends()  #对所有人回复

from multiprocessing import Process
@bot.register(boring_group1)
def group_message(msg):
    print('[接收]' + str(msg))

    if (msg.type != 'Text'):
        ret = '[奸笑][奸笑]'
    else:
        def return_msg():
            print('sdfsdf')
            msg.reply_image("/home/tarena/WxRobot/壁纸2.jpg")
            msg.reply("/home/tarena/WxRobot/壁纸2.jpg")
            return r"@img@/home/tarena/WxRobot/壁纸2.jpg"
        p = Process(target=return_msg)
        p.start()
# tuling = Tuling(api_key='91bfe84c2b2e437fac1cdb0c571cac91')

# @bot.register(friends)
# def friends_message(msg):
#     print('[接收来自好友：]' + str(msg))
#     if (msg.type != 'Text'):
#         ret = '[奸笑][奸笑]'
#     else:
#         print('准备调用图灵')
#         print("msg",msg)
#         print(type(msg))
#         ret = tuling.reply_text(msg)
#         print("ret",ret)
#     print('[发送]' + str(ret))
#     return ret



embed()




# start_plug('liaotian',bot)


# def start_plug(plug_name,bot):
#     function_list = ['liaotian':listotian]
#     if(plug_name in function_list):
#         boring_group1 = bot.friends()  #对所有人回复
#         func = function_list[plug_name]
#         func()


# def listotian(bot):
#     @bot.register(boring_group1)
#     def group_message(msg):
#         print('[接收]' + str(msg))

#         if (msg.type != 'Text'):
#             ret = '[奸笑][奸笑]'
#         else:
#             ret = auto_ai(msg.text)
#         print('[发送]' + str(ret))
#         return ret
=======
from django.test import TestCase

# Create your tests here.
>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
