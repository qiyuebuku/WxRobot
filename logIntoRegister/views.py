<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from databases import models


# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'logIntoRegister/index.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user_info = models.UserInfo.objects.filter(username=username, userpwd=password).first()
        # 如果找到了用户的信息
        if user_info:
            # 关闭浏览器后session失效
            request.session['username']=username
            request.session['puid']=None
            request.session.set_expiry(0)
            return HttpResponseRedirect('/wx_init/')
        # 重新登陆
        else:
            return HttpResponseRedirect('/login/')


def register(request):
    if request.method == "POST":
        uname = request.POST.get('Name')
        uemail = request.POST.get('Email')
        upassword = request.POST.get('Password')

        print(uname, uemail, upassword)
        user_info = models.UserInfo.objects.filter(username=uname)
        if user_info:
            return HttpResponseRedirect('/register/')
        else:
            models.UserInfo.objects.create(username=uname, userpwd=upassword)
            return HttpResponseRedirect('/login/')
=======
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from databases import models


# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'logIntoRegister/index.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user_info = models.UserInfo.objects.filter(username=username, userpwd=password).first()
        # 如果找到了用户的信息
        if user_info:
            # 关闭浏览器后session失效
            request.session['user'] = {'username':username,'prefsession':False,'puid':None}
            request.session.set_expiry(0)
            # 如果没有登陆登陆了微信号
            wechats= user_info.wechatid_set.all()  # 获取所有的用户
            if wechats:
                for wechat in wechats:
                    if wechat.isActive:
                        request.session['user']={
                            'username':username,
                            'prefsession':True,
                            'puid': wechat.puid
                        }
                        print("＂%s＂ 已经初始化了微信，他的信息：%s"%(username,request.session['user']))
                        return HttpResponseRedirect('/mainpage/')
            # 如果没有绑定任何帐号，或者绑定的帐号都是离线状态则条状到初始化微信页面
            return HttpResponseRedirect('/wx_init/')
        # 重新登陆
        else:
            return HttpResponseRedirect('/login/')


def register(request):
    if request.method == "POST":
        uname = request.POST.get('Name')
        uemail = request.POST.get('Email')
        upassword = request.POST.get('Password')

        print(uname, uemail, upassword)
        user_info = models.UserInfo.objects.filter(username=uname)
        if user_info:
            return HttpResponseRedirect('/register/')
        else:
            models.UserInfo.objects.create(username=uname, userpwd=upassword)
            return HttpResponseRedirect('/login/')
>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
