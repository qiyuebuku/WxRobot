from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from wxpy import *
from threading import Thread,Event 
# Create your views here.
import os 
import base64
import inspect
import ctypes
import json 
import time
import shutil
import sys 
import pickle 






class Debug(object):
    def __init__(self,flag):
        self.debug=flag 

    def print_l(self,*args,**kwargs):
        if self.debug:
            print(*args,**kwargs)

debug = Debug(True)

# 机器人线程
class BotThread(Thread):
    '''
        作用：用于生成一个机器人实例
        e_qrcode：二维码的标志位
        e_login：登录状态的标志位
    '''
    def __init__(self,e_qrcode):
        super().__init__()
        self.e_qrcode=e_qrcode
        self.qrcode=None
        self.bot_status=True
        # self.bot = None
    def run(self):
        # 构建机器人对象
        # self.bot = Bot(qr_callback=self.qr_callback,login_callback=self.login_callback)
        try:
            self.bot = Bot(qr_callback=self.qr_callback)
            self.bot.enable_puid('wxpy_puid.pkl')
            # self.bot = Bot(qr_callback=self.qr_callback,login_callback=self.login_callback)
            # old_file = os.path.join(os.path.dirname(__file__),'cache',self.uuid+'.pkl')
            # puid_map1 = self.bot.enable_puid(old_file)
            # puid1 = puid_map1.get_puid(self.bot.self)
            # new_file = os.path.join(os.path.dirname(__file__),'cache',puid1+'.pkl')
            # puid_map2 = self.bot.enable_puid(new_file)
            # os.remove(old_file)
            # print(puid_map2.get_puid(self.bot.self))
            # time.sleep(2)
            # new_file = os.path.join(os.path.dirname(__file__),'cache',self.bot.user_details(self.bot.self).puid+'.pkl')
            # print(new_file)
            # if not os.path.exists(new_file):
            #     shutil.copyfile(old_file,new_file)
        except KeyError:
            debug.print_l('该微信账号已被限制登录网页微信，请更换微信号后再试')
            self.bot_status=False

    
    # 二维码获取成功后的回调函数
    def qr_callback(self,uuid, status, qrcode):
        debug.print_l('二维码刷新成功')
        # bytest格式的二维码数据流
        self.qrcode=qrcode
        self.uuid=uuid
        # set二维码标志位
        self.e_qrcode.set()

    
    # #  登录成功后的回调函数
    # def login_callback(self):
    #     self.bot.enable_puid(self.uuid+'.pkl')
    #     # self.bot.enable_puid('wxpy_puid.pkl')
    #     puid = self.bot.user_details(self.bot.self).puid
    #     shutil.copyfile(self.uuid+'.pkl','cache/'+puid+'.pkl')

    

class Robot_management(Thread):
    """
    机器人管理者，管理活动的机器人，当机器人对象超出预先设定好的走向时，杀死他::
        * 如果一个机器人的存活时间超过了预设的值，程序将会检测他是否被用户登录。
        * 如果不是，这个机器人线程将会被清理掉。
    """
    def __init__(self,*,timeout=10,inspection_interval=5):
        super().__init__()
        self.bot_thread = {}
        self.timeout=timeout
        self.inspection_interval=inspection_interval 
        self.debug = debug

    def run(self):
        """ 
        :param timeout:
            * 设定未被扫码的持续时间
            * 单位为秒
        :param inspecition_interval
            * 检测间隔
            * 多少秒进行一次检测

        """
        while True:
            bot_thread = self.bot_thread
            Current_timestamp = int(time.time()) 
            # 待清理的机器人id
            cleaner_uuid = [] 
            if not len(bot_thread.values()):
                continue
            for uuid in bot_thread:
                # 如果实例没有被登录，并且存在时间超过了设定的超时时间
                # 将其加入到待清理列表，准备销毁
                if bot_thread[uuid]['time']+self.timeout<Current_timestamp:
                    try:
                        if bot_thread[uuid]['object'].bot.alive:
                            # 如果机器人为登录状态，则跳过
                            continue
                    except AttributeError:
                        debug.print_l('%s机器人被创建时间',bot_thread[uuid]['time'])
                        debug.print_l('当前时间：',Current_timestamp)
                        cleaner_uuid.append(uuid)  
            # 将待处理列表里的机器人销毁
            for uuid in cleaner_uuid: 
                if self.cleaner(uuid)<0:
                   debug.print_l('机器人id：%s存在抵抗行为，自动清理失败！！！'%uuid)
                   continue
                debug.print_l('机器人ID：%s,清理完成'%uuid)
            debug.print_l('---------------------------------------')
            debug.print_l('当前活动机器人：',self.bot_thread)
            debug.print_l('---------------------------------------')
            time.sleep(self.inspection_interval)
    
    # 机器人清理器
    def cleaner(self,bot_uuid): 
        '''
            功能：用于强制结束一个线程的执行
            bot_uuid：需要被清理的机器人uuid
        '''
        try:
            thread = self.bot_thread[bot_uuid]['object']   # 获取线程对象
            # 如果机器人在登录时出现了问题，就直接删除！！！
            if not thread.bot_status:
                del self.bot_thread[bot_uuid] # 从监控列表中移除
                return True
            # 要删除的线程必须是活动线程，否则直接从字典里面移除
            try:
                self._async_raise(thread.ident,SystemExit)  #终止机器人线程
            except:
                pass 
            del self.bot_thread[bot_uuid] # 从监控列表中移除
            return True
        except Exception as e:
            print(e)
            return False

    # 用于强制终止线程的运行
    def _async_raise(self,tid,exctype):
        '''
            tid : 线程的识别符
            exctype : 类型，如：SystemExit，表示终止这个线程
        '''

        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    # 增加需要被管理的机器人
    def append(self,bot_uuid,bot_object):
        """
            用于将需要被管理的机器人线程加入进来
            :param bot_uuid 
                * 机器人的uuid号
            :param bot_object
                * 机器人对应的线程对象
        """
        # 获取当前的时间戳
        Current_timestamp = int(time.time()) 
        self.bot_thread[bot_uuid]={'object':bot_object,'time':Current_timestamp}


def get_bot(bot_uuid):
    try:
        # 获取机器人对象
        bot = rmt.bot_thread[bot_uuid]['object'].bot
    except (KeyError,AttributeError):
        return False
    return bot
    
# 获取单个或多个用户的详细信息
def bot_details(bot_uuid):
    """
    :param bot_uuid 机器人的uuid标识符
    :return 名称、头像，微信ID
    """
    bot = get_bot(bot_uuid)
    if not bot :
        return False
    # 获取对象的详细信息
    user_details = bot.user_details(bot.self)
    # 微信名称
    USER_NAME =user_details.name
    # 微信头像
    AVATAR_BYTES = base64.b64encode(user_details.get_avatar()).decode() 
    # 微信ID号
    WXID = user_details.wxid
    # 性别
    SEX = user_details.sex
    # 省份
    PROVINCE = user_details.province 
    # 城市
    CITY = user_details.city
    # 个性签名
    SIGNATURE = user_details.signature
    PUID = user_details.puid
    details={
        'user_name':USER_NAME,
        'avatar':AVATAR_BYTES,
        'wxid':WXID,
        'status':'正常',
        'sex' : SEX,
        'province' : PROVINCE,
        'city' : CITY,
        'signature' : SIGNATURE,
        'uuid':bot_uuid,
        'puid': PUID,
    }
    return details


#======================================= 视图 ====================================================

global rmt
# 创建管理线程
rmt = Robot_management(timeout=10)
# 主进程退出，线程也跟着陪葬
rmt.setDaemon(True)
rmt.start()

def home(request):
    # 用户提交的uuid
    bot_uuid = request.GET['uuid']
    user_details = bot_details(bot_uuid)
    if user_details:
        return render(request,'home.html',user_details)
    else:
        # 让用户重新登录
        return HttpResponseRedirect('/index/')

def is_login(request):
    # 获取登录状态的机器人标识符
    bot_uuid = request.POST['uuid']
    # debug.print_l('查询机器人：',bot_uuid)
    data={'inventory':False,'alive':False}

    bot = rmt.bot_thread.get(bot_uuid)
    if bot:
        bot_object = bot['object']
        data['inventory'] = True
        data['alive'] = hasattr(bot_object,'bot')
    return HttpResponse(json.dumps(data))

# 用户输入的url为空时，则将其跳转到主页
def main_index(request):
    return HttpResponseRedirect('/index/')



def index(request):
    # global e_qrcode,e_login
    e_qrcode = Event() # 二维码标志位
    # 清除维码标志位
    e_qrcode.clear()
    # 创建机器人对象
    robot = BotThread(e_qrcode)
    robot.start()
    
    #等待二维码标志位被set
    e_qrcode.wait()
    # 对图片数据进行base64编码，然后在转换为普通字符串格式
    qrcode = base64.b64encode(robot.qrcode).decode()
    # 用户的唯一标识符
    uuid = robot.uuid
    # 将新创建的线程按照，键：uui，值：robot的方式加入到字典里面
    rmt.append(uuid,robot)
    debug.print_l(rmt.bot_thread)

    # 获取二维码请求
    if request.method == "GET": 
        return render(request,'index.html',{'qrcode':qrcode,'uuid':uuid})    
    # 刷新二维码请求
    elif request.method == "POST":
        # 获取未被扫描的机器人标识符
        last_bot_uuid = request.POST['uuid']
        # kill掉刷新前的机器人
        debug.print_l("正在结束线程：",last_bot_uuid)
        rmt.cleaner(last_bot_uuid)
        # 构建一个json格式的数据包，包含新建机器人的uuid和qrcode
        data = json.dumps({'uuid':robot.uuid,'qrcode':qrcode})
        # 返回请求
        return HttpResponse(data)


def logout(request):
    uuid = request.GET['uuid']
    bot = get_bot(uuid)
    debug.print_l("机器人ID：%s请求退出"%uuid)
    rmt.cleaner(uuid)
    if not bot :
        return HttpResponse("退出失败！！！")    
    if bot.logout():
        return HttpResponseRedirect('/index/')
    return HttpResponse("退出失败！！！")    
    