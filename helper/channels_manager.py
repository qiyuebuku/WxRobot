from threading import Thread,Event 
# Create your views here.
import os 
import inspect
import ctypes
import time
import shutil
import sys 
<<<<<<< HEAD
import pickle
import time
from multiprocessing import Queue
import json
from channels import Group

class channel_management(object):
    def __init__(self):
        super().__init__()
        self.channels = {}
        # self.q = Queue()
        # 添加到广播群组

    def reply_channel_send(self,username,info):
        Group(username).send({
            'text': json.dumps(info)
        })


cm = channel_management()
=======
import pickle 


class Initialize_channels(object):
    def __init__(self):
        self.channels = {}         
    def add_channels(self,username,channels):
        self.channels[username]=channels
    def del_channels(self,username):
        del self.channels[username]
    def get_channels(self,username):
        try:
            return self.channels[username]
        except:
            print('当前已加入的管道：',self.channels)
            return None


class Logged_channels(object):
    def __init__(self):
        self.channels = {}         
    def add_channels(self,username,channels):
        self.channels[username]=channels

    def del_channels(self,username):
        del self.channels[username]

    def get_channels(self,username):
        try:
            return self.channels[username]
        except:
            print('当前已加入的管道：',self.channels)
            return None


initialize_channels = Initialize_channels()
logged_channels = Logged_channels()
>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
