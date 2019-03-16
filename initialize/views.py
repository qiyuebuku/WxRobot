from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from wxpy import *
from threading import Thread, Event
# Create your views here.
import os
import base64
import json
import time
from initialize import helper
# from initialize.helper import debug, initialize_channels as ic
from helper.channels_manager import initialize_channels as ic
from helper.debug import debug
# from homepage.helper import aom
from databases import models
from helper.bot_manager import robot_management as rm 

# 机器人线程


class BotThread(Thread):
    '''
        作用：用于生成一个机器人实例
        e_qrcode：二维码的标志位
        e_login：登录状态的标志位
    '''

    def __init__(self, e_qrcode, request):
        super().__init__()
        self.e_qrcode = e_qrcode
        self.qrcode = None
        self.bot_status = True
        self.bot = None  # 默认为True
        # self.username = username
        self.e_bot = Event()  # 获取标志位
        self.request = request
        # self.bot = None

    def run(self):
        # 构建机器人对象
        # self.bot = Bot(qr_callback=self.qr_callback,login_callback=self.login_callback)
        try:
            # 实例化一个机器人
            self.bot = Bot(qr_callback=self.qr_callback,
                           login_callback=self.login_callback, logout_callback=self.logout_callback)
            # 开启puid缓存
            self.bot.enable_puid('wxpy_puid.pkl')
            self.e_bot.set()
        except KeyError as e:
            channel = ic.get_channels(self.username)
            channel.reply_channel.send({
                'text': json.dumps({
                    'init_status': False,
                    'error': '该微信账号已被限制登录网页微信，请更换微信号后再试',
                })
            })
            print("error:", e)
            debug.print_l('该微信账号已被限制登录网页微信，请更换微信号后再试')
            # self.bot_status = False

    # 二维码获取成功后的回调函数
    def qr_callback(self, uuid, status, qrcode):
        debug.print_l('二维码刷新成功')
        # bytest格式的二维码数据流
        self.qrcode = qrcode
        self.uuid = uuid
        # set二维码标志位
        self.e_qrcode.set()
        try:
            channel = ic.get_channels(self.username)
            channel.reply_channel.send({
                'text': json.dumps({
                    'qrcode': base64.b64encode(qrcode).decode()
                })
            })
        except:
            pass

    # 微信在退出时调用

    def logout_callback(self):
        pass
        # puid = self.bot.puid
        # print(puid)
        # if puid:
        #     wechat_id = models.WechatId.objects.filter(puid=puid).all()
        #     if len(list(wechat_id)):
        #         print('将%s从数据清理成功' % puid)
        #         wechat_id.delete()
        #         return
        # print('将%s从数据清理失败' % puid)

    def bot_puid(self, bot):
        user_details = bot.user_details(bot.self)
        data = {
            # 微信名称
            'user_name': user_details.name,
            # 微信头像
            'avatar_bytes': base64.b64encode(
                user_details.get_avatar()).decode()
        }
        # 获取puid身份标识符
        puid = bot.user_details(bot.self).puid
        return data, puid

    #  登录成功后的回调函数
    def login_callback(self, **kwargs):
        self.e_bot.clear()
       
        def go_to_mainpage():
            # 等待bot被创建
            self.e_bot.wait()
            username = self.request.session['user'].get('username')
            print("用户名为：", username)

            # 获取初始化的微信头像和名称以及puid
            data, puid = self.bot_puid(self.bot)
            # 添加到登录成功字典里
            rm.add_bot(puid,self.bot)
            
            # 查找当前帐号下所绑定的微信号
            user = models.UserInfo.objects.filter(
                username = username
                ).first()
            # wechats = user.wechatid_set.all()

            wechat = user.wechatid_set.filter(puid = puid).first()
            # 帐号还没有绑定任何微信号，则绑定初始化成功的微信
            if not wechat:
                models.WechatId.objects.create(
                    puid = puid,
                    status = True,
                    user_info_id = user.id
                    )
                print('为%s添加微信：%s' %(username,puid))
            # 如果当前微信已经存在于数据库中，则检查其登录状态是否为在线
            else:
                # 设置为在线状态
                # models.WechatId.object.filter()
                wechat.status = True 
                wechat.save()
                print('%s的微信已经存在'%username)

           
            # 获取通信管道
            channel = ic.get_channels(username)
            # 设置登录成功到channel_seesion里面
            channel.channel_session['user']={
                'username':username,
                'prefsession': True,
                'puid': puid
            }
            print('puid:',puid)
            print('user:',self.request.session['user'])

            channel.reply_channel.send({
                'text': json.dumps({
                    # 'username': username,
                    'init_status': True,
                    'info': '登录成功，正在跳转......'
                })
            })
            # ic.del_channels(username)
        t = Thread(target=go_to_mainpage)
        t.start()


def check_landing(fun):
    """
        用于检测是否登陆成功
    """
    def function(request, *args, **kwargs):

        print(request.path)
        v = request.session.get('user')
        print("用户名：", v)
        if not v:
            print('用户未登录')
            return redirect('/login/')
        return fun(request, *args, **kwargs)
    return function


# @check_landing
# def wx_status(request):
#     # 获取登录状态的机器人标识符
#     bot_uuid = request.POST['uuid']
#     # debug.print_l('查询机器人：',bot_uuid)
#     data = {'inventory': False, 'alive': False}
#     bot_thread = rmt.bot_thread.get(bot_uuid)
#     # 如果二维码存在
#     if bot_thread:
#         bot_object = bot_thread['object']
#         data['inventory'] = True
#         data['alive'] = hasattr(bot_object, 'bot')
#         if data['alive']:
#             # 根据uuid获取机器人对象
#             bot = bot_object.bot
#             user_details = bot.user_details(bot.self)
#             # 微信名称
#             data['user_name'] = user_details.name
#             # 微信头像
#             data['avatar_bytes'] = base64.b64encode(user_details.get_avatar()).decode()
#             # 获取puid身份标识符
#             puid = bot.user_details(bot.self).puid
#             # 将puid标识符赋给bot对象
#             bot.puid = puid
#             # 将登陆成功的对象添加到aom里面
#             aom.add_logged(bot)
#             # 将登陆状态设置为登陆成功
#             request.session['prefsession'] = True
#             # 设置puid到缓存
#             request.session['puid'] = puid
#             request.session.set_expiry(0)
#             # 登录成功，获取对象，并将其从监控列表移除
#             if rmt.cleaner(bot_uuid):
#                 # 登陆成功尝试创建档案，如果已经存在则放弃
#                 # status = True if request.POST.get('status') == "1" else False
#                 # print(status)
#                 # print(request.POST.get('status'))
#                 if not models.WechatId.objects.filter(puid=puid).first():
#                     # result = list(models.WechatId.objects.all().values("puid"))  # 取所有puid
#                     # print(list(result))
#                     # for dict in result:
#                     #     if puid in dict["puid"]:
#                     #         print("已经存在：", puid)
#                     #         break
#                     # else:
#                     models.WechatId.objects.create(puid=str(puid))
#                     print('为%s建立档案成功' % puid)
#                 else:
#                     print('已经存在')
#                 debug.print_l('将%s移除成功' % data['user_name'])
#     return HttpResponse(json.dumps(data))


# 用户输入的url为空时，则将其跳转到主页
def main_index(request):
    return HttpResponseRedirect('/wx_init/')


@check_landing
def wx_init(request):
    try:
        # global e_qrcode,e_login
        e_qrcode = Event()  # 二维码标志位
        # 清除维码标志位
        e_qrcode.clear()
        # 创建机器人对象
        # --------------------------------------------------
        robot = BotThread(e_qrcode, request)
        # --------------------------------------------------

        robot.start()
        # 等待二维码标志位被set
        e_qrcode.wait()

       
        # 对图片数据进行base64编码，然后在转换为普通字符串格式
        qrcode = base64.b64encode(robot.qrcode).decode()

        # # 用户的唯一标识符
        uuid = robot.uuid
        # # 将新创建的线程按照，键：uui，值：robot的方式加入到监控字典里字典里面
        # rmt.add(uuid, robot)
        # debug.print_l(rmt.bot_thread)
        print(request.session['user'])    
        # 获取用户名
        username = request.session['user'].get('username')
        # 获取二维码请求
        print('初始化微信')
        return render(request, 'initialize/InitializeWeChat.html', {'qrcode': qrcode, 'uuid': uuid, 'username':username})
    except Exception as e:
        print('未获去到用户名',e)
        return HttpResponseRedirect('／login/')
    # # 刷新二维码请求
    # elif request.method == "POST":
    #     # 获取未被扫描的机器人标识符
    #     last_bot_uuid = request.POST['uuid']
    #     # kill掉刷新前的机器人
    #     # debug.print_l("正在结束线程：", last_bot_uuid)
    #     # rmt.cleaner(last_bot_uuid)
    #     # 构建一个json格式的数据包，包含新建机器人的uuid和qrcode
    #     data = json.dumps({'uuid': robot.uuid, 'qrcode': qrcode})
    #     # 返回请求
    #     return HttpResponse(data)
