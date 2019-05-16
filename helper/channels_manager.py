from threading import Thread,Event 
# Create your views here.
import os 
import inspect
import ctypes
import time
import shutil
import sys 
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