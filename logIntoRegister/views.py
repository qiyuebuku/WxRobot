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
