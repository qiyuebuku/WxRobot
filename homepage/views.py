from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from homepage import helper
from login.helper import debug,rmt
import time
import json
# Create your views here.

# 用户管理对象
aom = helper.aom

def check_user(fun):
    """
        用于检测是否登陆成功
    """
    def function(request,*args,**kwargs):
        v = request.session.get('prefsession')
        if not v:
            return redirect('/index/')
        return fun(request,*args,**kwargs)
    return function

# 用户的退出操作
def logout(request):
    # puid = request.GET['puid']
    puid = request.session['puid']
    bot = aom.get_bot_dict(puid)['bot']
    debug.print_l("用户ID：%s请求退出"%puid)
    # 如果提交的puid可以获取到对象，并且注销成功和从列表里面也删除成功，则跳转到登录页面
    if  bot and bot.logout() and aom.cleaner(puid):
        return HttpResponseRedirect('/index/')
    return HttpResponse("退出失败！！！")    

def Heart_rate_response(request):
    print('这里是heart_rate_response')
    # 用于刷新用户提交心跳的时间
    # puid = request.POST.get('puid')
    puid = request.session['puid']
    bot_dict = aom.get_bot_dict(puid)
    if not bot_dict:
        return HttpResponse('no')
    bot_dict['date']=time.time()
    return HttpResponse('ok')

def analysis_result(request):
    puid = request.session['puid']
    bot = aom.get_bot_dict(puid)['bot']
    if not bot.result:
        return HttpResponse('没有分析好')
    else:
        # print('数据分析成功')
        # print(bot.result)
        # 以json格式将处理好的数据返回给前端
        data = json.dumps(bot.result)
        print(data)
        # data = "hello"
        # print(data)
        return HttpResponse(data)

    


@check_user
def mainpage(request):
    print('这里是manpage....')
    if request.method ==  "GET":
        puid = request.session.get('puid')
        user_details = aom.bot_details(puid)
        # 如果获取到了用户的详细信息，则进入后台页面
        if user_details:
            debug.print_l('%s的签名为：%s'%(user_details['user_name'],user_details['signature']))
            return render(request,'homepage/mainpage.html',user_details)
        else:
            return HttpResponseRedirect('/index/')  
    elif request.method == "POST":
        # 获取puid
        puid = request.session.get('puid')
        # 获取用户信息
        bot_dict = aom.get_bot_dict(puid)
        # 获取用户的bot对象
        bot = bot_dict.get('bot')  
        # 获取是哪个nav-item
        content_page = request.POST.get('content_page')[1:]
        if content_page=="custom_plug":
            # 调用自定义插件函数
            pass 
        elif content_page == "data_analysis":
            # 调用数据分析函数
            data = helper.Data_analysis(bot)
            analysis_result = data.get_analysis_result()
            # print(analysis_result)
            return HttpResponse(analysis_result)
        elif content_page == "intelligent_chat":
            # 调用只能聊天函数
            pass 
        elif content_page == "timed_transmission":
            # 调用定时发送函数
            pass

def get_world_cloud(request):
    if request.method =="GET":
        # 获取puid
        puid = request.session.get('puid')
        # 获取用户信息
        bot_dict = aom.get_bot_dict(puid)
        # 获取用户的所有的对象
        friends = bot_dict.get('bot').friends(update=True)
        # 获取所有人的个性签名
        signatures = {i.name:i.signature for i in friends }
        # 创建词云分析线程
        cloud_thread = helper.Create_world_cloud(signatures,'/home/tarena/WxRobot/homepage/static/img/color_mask.jpg')
        return HttpResponse('ok')
    elif request.method == "POST":
        world_cloud = cloud_thread.get_bytes
        if world_cloud:
            return HttpResponse(world_cloud)
        else:
            return HttpResponse('no')
def test(request):
    return render(request,'homepage/test05.html')

    