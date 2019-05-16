<<<<<<< HEAD
# coding=utf-8
import json
import os
import base64
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from multiprocessing import Pipe
from threading import Thread

fd1, fd2 = Pipe(duplex=True)


# def reply_channel_send():

@channel_session_user_from_http
def ws_connect(message):
    print("os.getpid()", os.getpid())
    path = message['path'].strip('/').split('/')
    username = path[2]
    # if path[1] == "initialize":
    #     print("添加到登录管道里")
    #     # # 添加到登录管道里
    #     initialize_channels[username] = message
    #     print("initialize_channels", initialize_channels)
    #
    # elif path[1] == "homepage":
    #     print("添加到主页管道里")
    #     # 添加到主页管道里
    #     logged_channels[username] = message
    #     print("logged_channels", logged_channels)

    # 添加到广播群组
    Group(username).add(message.reply_channel)
    # 广播消息
    Group(username).send({
        'text': json.dumps({
            'is_logged_in': True
        })
    })



@channel_session_user
# 将发来的信息原样返回
def ws_message(message):
    message.reply_channel.send({
        "text": message.content['text'],
    })


@channel_session_user
def ws_disconnect(message):
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('users').discard(message.reply_channel)
=======
#coding=utf-8
import json
from channels import Group
from channels.auth import channel_session_user,channel_session_user_from_http
from helper.channels_manager import initialize_channels as ic,logged_channels as lc 

@channel_session_user_from_http
def ws_connect(message):
    path = message['path'].strip('/').split('/')
    username = path[1]
    print("path",path)
    if path[0] == "initialize":
        print("添加到登录管道里")
        # 添加到登录管道里
        ic.add_channels(username,message)
    elif path[0] == "homepage":
        print("添加到主页管道里")
        # 添加到主页管道里
        lc.add_channels(username,message)
       

    # 添加到广播群组
    Group('users').add(message.reply_channel)
    # 广播消息
    Group('users').send({
        'text':json.dumps({
            'is_logged_in':True 
        })
    })

@channel_session_user
#将发来的信息原样返回
def ws_message(message):
    message.reply_channel.send({
        "text": message.content['text'],
    })


@channel_session_user
def ws_disconnect(message):
    Group('users').send({
        'text':json.dumps({
            'username':message.user.username,
            'is_logged_in':False
        })
    })
    Group('users').discard(message.reply_channel)




>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
