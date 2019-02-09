from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from wxpy import *
from threading import Thread,Event 
# Create your views here.
import os 
import base64
import json 
import time
from login import helper
# from login.helper.Robot_manage import *
from login.helper import debug,rmt
from background_frame.helper import aom






# 机器人线程
class BotThread(Thread):
    '''
        作用：用于生成一个机器人实例
        e_qrcode：二维码的标志位
        e_login：登录状态的标志位
    '''
    def __init__(self,e_qrcode,rmt):
        super().__init__()
        self.e_qrcode=e_qrcode
        self.qrcode=None
        self.bot_status=True
        # self.bot = None
    def run(self):
        # 构建机器人对象
        # self.bot = Bot(qr_callback=self.qr_callback,login_callback=self.login_callback)
        try:
            # 实例化一个机器人
            self.bot = Bot(qr_callback=self.qr_callback)
            # 开启puid缓存
            puid_map = self.bot.enable_puid('wxpy_puid.pkl')
            # # 获取Puid
            # puid = puid_map.get_puid(self.bot.self)   
            # # 加入已登录字典         
            # rmt.has_logged[puid]={'bot':self.bot,'beat':30}
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

    




#======================================= 视图 ====================================================



def is_login(request):
    # 获取登录状态的机器人标识符
    bot_uuid = request.POST['uuid']
    # debug.print_l('查询机器人：',bot_uuid)
    data={'inventory':False,'alive':False}
    bot_thread = rmt.bot_thread.get(bot_uuid)
    # 如果二维码存在
    if bot_thread:
        bot_object = bot_thread['object']
        data['inventory'] = True
        data['alive'] = hasattr(bot_object,'bot')
        if data['alive']:
            # 根据uuid获取机器人对象
            bot = bot_object.bot
            # 获取puid身份标识符
            puid = bot.user_details(bot.self).puid
            # 将登陆成功的对象添加到活跃对象管理器
            # aom.has_logged[puid]={'bot':bot,'time':time.time()}
            aom.add_logged(bot)
            data['puid']=puid
            # 登录成功，则将其从监控列表移除            
            if rmt.cleaner(bot_uuid):
                debug.print_l('将%s移除成功'%bot_uuid)
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
    robot = BotThread(e_qrcode,rmt)
    robot.start()
    
    #等待二维码标志位被set
    e_qrcode.wait()
    # 对图片数据进行base64编码，然后在转换为普通字符串格式
    qrcode = base64.b64encode(robot.qrcode).decode()
    # 用户的唯一标识符
    uuid = robot.uuid
    # 将新创建的线程按照，键：uui，值：robot的方式加入到监控字典里字典里面
    rmt.add(uuid,robot)
    debug.print_l(rmt.bot_thread)

    # 获取二维码请求
    if request.method == "GET": 
        return render(request,'login/index.html',{'qrcode':qrcode,'uuid':uuid})    
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

