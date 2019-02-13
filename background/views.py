from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect


from background.helper import aom
from login.helper import debug,rmt
import time
# Create your views here.


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
    # 用于刷新用户提交心跳的时间
    # puid = request.POST.get('puid')
    puid = request.session['puid']
    bot_dict = aom.get_bot_dict(puid)
    if not bot_dict:
        return HttpResponse('no')
    bot_dict['date']=time.time()
    return HttpResponse('ok')
    


@check_user
def home(request):
    puid = request.session.get('puid')
    user_details = aom.bot_details(puid)
    # 如果获取到了用户的详细信息，则进入后台页面
    if user_details:
        debug.print_l('%s的签名为：%s'%(user_details['user_name'],user_details['signature']))
        return render(request,'background_frame/data_analysis.html',user_details)
    else:
        return HttpResponseRedirect('/index/')

@check_user
def custom_plug(request):
    puid = request.session.get('puid')
    user_details = aom.bot_details(puid)
    # 如果获取到了用户的详细信息，则进入后台页面
    if user_details:
        debug.print_l('%s的签名为：%s'%(user_details['user_name'],user_details['signature']))
        return render(request,'background_frame/custom_plug.html',user_details)
    else:
        return HttpResponseRedirect('/index/')

@check_user
def data_analysis(request):
    puid = request.session.get('puid')
    user_details = aom.bot_details(puid)
    # 如果获取到了用户的详细信息，则进入后台页面
    if user_details:
        debug.print_l('%s的签名为：%s'%(user_details['user_name'],user_details['signature']))
        return render(request,'background_frame/data_analysis.html',user_details)
    else:
        return HttpResponseRedirect('/index/')

@check_user
def intelligent_chat(request):
    puid = request.session.get('puid')
    user_details = aom.bot_details(puid)
    # 如果获取到了用户的详细信息，则进入后台页面
    if user_details:
        debug.print_l('%s的签名为：%s'%(user_details['user_name'],user_details['signature']))
        return render(request,'background_frame/intelligent_chat.html',user_details)
    else:
        return HttpResponseRedirect('/index/')


@check_user
def timed_transmission(request):
    puid = request.session.get('puid')
    user_details = aom.bot_details(puid)
    # 如果获取到了用户的详细信息，则进入后台页面
    if user_details:
        debug.print_l('%s的签名为：%s'%(user_details['user_name'],user_details['signature']))
        return render(request,'background_frame/timed_transmission.html',user_details)
    else:
        return HttpResponseRedirect('/index/')


           


    