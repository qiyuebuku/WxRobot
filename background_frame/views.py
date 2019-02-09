from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404


from background_frame.helper import aom
from login.helper import debug,rmt
import time
# Create your views here.


def home(request,puid):
    try:
        debug.print_l('用户的puid为：',puid)
        user_details = aom.bot_details(puid)
    except Exception as e :
        print('出现错误：',e)
        # 让用户重新登录
        return HttpResponseRedirect('/index/')
    # 如果获取到了用户的详细信息，则进入后台页面
    if user_details:
        debug.print_l('%s的签名为：%s'%(user_details['user_name'],user_details['signature']))
        return render(request,'background_frame/home.html',user_details)
    else:
        return HttpResponseRedirect('/index/')
           

# 用户的退出操作
def logout(request):
    puid = request.GET['puid']
    bot = aom.get_bot_dict(puid)['bot']
    debug.print_l("用户ID：%s请求退出"%puid)
    # 如果提交的puid可以获取到对象，并且注销成功和从列表里面也删除成功，则跳转到登录页面
    if  bot and bot.logout() and aom.cleaner(puid):
        return HttpResponseRedirect('/index/')
    return HttpResponse("退出失败！！！")    


def Heart_rate_response(request):
    puid = request.POST.get('puid')
    bot_dict = aom.get_bot_dict(puid)
    if not bot_dict:
        return HttpResponse('no')
    bot_dict['time']=time.time()
    return HttpResponse('ok')
    
    