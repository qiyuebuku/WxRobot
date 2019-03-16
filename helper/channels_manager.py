from threading import Thread,Event 
# Create your views here.
import os 
import inspect
import ctypes
import time
import shutil
import sys 
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