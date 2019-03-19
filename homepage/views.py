from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from homepage import helper
from helper.debug import debug
import time
import json
from wxpy import *
from databases import models
from helper.bot_manager import robot_management as rm 
from helper.channels_manager import initialize_channels as ic
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# 用户管理对象
# aom = helper.aom

def check_user(fun):
    """
        用于检测是否登陆成功
    """
    def function(request,*args,**kwargs):
        v = request.session.get('prefsession')
        if not v:
            print('用户未登录')
            return redirect('/index/')
        return fun(request,*args,**kwargs)
    return function

# # 用户的退出操作
# def logout(request):
#     puid = request.GET['puid']
#     bot = aom.get_bot_dict(puid)['bot']
#     debug.print_l("用户ID：%s请求退出"%puid)
#     # 如果提交的puid可以获取到对象，并且注销成功和从列表里面也删除成功，则跳转到登录页面
#     if  bot and bot.logout() and aom.cleaner(puid):
#         return HttpResponseRedirect('/index/')
#     return HttpResponse("退出失败！！！")    

# def Heart_rate_response(request):
#     print('这里是heart_rate_response')
#     # 用于刷新用户提交心跳的时间
#     # puid = request.POST.get('puid')
#     puid = request.session['puid']
#     bot_dict = aom.get_bot_dict(puid)
#     if not bot_dict:
#         return HttpResponse('no')
#     bot_dict['date']=time.time()
#     return HttpResponse('ok')


# def analysis_result(request):
#     puid = request.session['puid']
#     bot = aom.get_bot_dict(puid)['bot']
#     if not bot.result:
#         return HttpResponse('没有分析好')
#     else:
#         # 以json格式将处理好的数据返回给前端
#         data = json.dumps(bot.result)
#         print(data)
#         return HttpResponse(data)


# @check_user
def mainpage(request):
    print('这里是manpage....')
    if request.method ==  "GET":
        user = request.session.get('user')
        if user:
            username = user.get('username')
            if username:
                # 如果获取到了管道,则使用管道里面的内容替换session
                channels = ic.get_channels(username)
                if channels and channels.channel_session.get('user'):
                    user = channels.channel_session['user']
                    ic.del_channels(username)
                    request.session['user'] = user 
                print("user",user)
                puid = user['puid']
                print("robots",rm.robots)
                basic_data = rm.get_basic_data(puid)
                # 如果获取到了用户的详细信息，则进入后台页面
                if basic_data:
                    debug.print_l('%s的签名为：%s'%(basic_data['user_name'],basic_data['signature']))
                    # 初始化数据分析页面
                    rm.start_data_analysis(puid,username)
                    rm.start_data_intelligent(puid,username)
                    basic_data['username'] = username
                    return render(request,'homepage/mainpage.html',basic_data)
        return HttpResponseRedirect('/wx_init/')  

    elif request.method == "POST":
        # 获取puid
        puid = request.session["user"].get('puid')
        # # 获取用户信息
        # bot_dict = aom.get_bot_dict(puid)
        # # 获取用户的bot对象
        # bot = bot_dict.get('bot')  
        bot = bm.get_bot(puid)
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
#
# def get_world_cloud(request):
#     if request.method =="GET":
#         # 获取puid
#         puid = request.session.get('puid')
#         # 获取用户信息
#         bot_dict = aom.get_bot_dict(puid)
#         # 获取用户的所有的对象
#         friends = bot_dict.get('bot').friends(update=True)
#         # 获取所有人的个性签名
#         signatures = {i.name:i.signature for i in friends }
#         # 创建词云分析线程
#         cloud_thread = helper.Create_world_cloud(signatures,'/home/tarena/WxRobot/homepage/static/img/color_mask.jpg')
#         return HttpResponse('ok')
#     elif request.method == "POST":
#         world_cloud = cloud_thread.get_bytes
#         if world_cloud:
#             return HttpResponse(world_cloud)
#         else:
#             return HttpResponse('no')
@csrf_exempt
def save_chat_config(request):
    friends = request.POST.get('friends')
    groups = request.POST.get('groups')
    wechat_id = models.WechatId.objects.filter(puid = request.session['user'].get('puid')).first()
    friends = json.loads(friends)
    groups = json.loads(groups)


    models.SelectedFriends.objects.filter(wechat_id = wechat_id).delete()
    models.SelectedGroups.objects.filter(wechat_id = wechat_id).delete()

    #好友
    for f in friends:
        fid = f['fid']
        models.SelectedFriends.objects.update_or_create(fid=fid,wechat_id = wechat_id)
        # models.SelectedFriends.objects.create(fid=fid,friend_name=friend_name,wechat_id = wechat_id)

    #群组
    for g in groups:
        gid = g['gid']
        models.SelectedGroups.objects.update_or_create(gid=gid,wechat_id = wechat_id)




    # print(friends,groups)
    #
    # # 获取puid
    # puid = request.session.get('puid')
    #
    # wfriends = request.POST.getlist('wfriend')
    # wgroups = request.POST.getlist('wgroup')
    #
    # wechat_id = models.WechatId.objects.filter(puid=puid).first()
    # # 清空以前的数据
    # wechat_id.selectedfriends_set.all().delete()
    # wechat_id.selectedgroups_set.all().delete()
    #
    # # 增加提交的数据到数据库
    # fcount = gcount = 0
    # # 增加好友到数据库
    # for name in wfriends:
    #     models.SelectedFriends.objects.create(friend_name=name, wechat_id=wechat_id)
    #     fcount += 1
    # # 增加群聊到数据库
    # for group in wgroups:
    #     models.SelectedGroups.objects.create(group_name=group, wechat_id=wechat_id)
    #     gcount += 1
    # # print(len(wfriends),len(wgroups))
    # # print(fcount,gcount)
    # if (fcount == len(wfriends)) & (gcount == len(wgroups)):
    #     return HttpResponse('ok')
    # else:
    #     return HttpResponse('no')

    return HttpResponse('ok')

# def groups_and_friends_info(request):
#     # 获取puid
#     puid = request.session.get('puid')
#     # 获取用户的bot对象
#     bot = aom.get_bot_dict(puid).get('bot')
#     groups = bot.groups(update = True)
#     group_infos = []
#     for group in groups:
#         group.update_group(True)

#         gname = group.name
#         # print("群名称：",gname)

#         gowner = group.owner.name  #群主
#         # print("群主：",gowner)

#         #所有群成员
#         members = group.members 
#         # print("群内成员：",group.members) 

#         # 统计性别
#         mtfratio = {'male':len(members.search(sex=MALE)),'female':len(members.search(sex=FEMALE)),'secrecy':len(members.search(sex=None))}
#         # print(mtfratio)

#         pcount = len(members)  #群成员数量
#         group_infos.append({'gname':gname,'gowner':gowner,'pcount':pcount,'mtfratio':mtfratio,'puid':group.puid})

#     friends = bot.friends(update=True)
#     user_infos = []
#     for friend in friends:
#         uname = friend.name 
#         usex = friend.sex 
#         user_infos.append({'uname':uname,'usex':usex})
#     print('user_infos',user_infos)
#     print('group_infos',group_infos)
#     ug_info = json.dumps({'user_info':user_infos,'group_info':group_infos})
#     return HttpResponse(ug_info)
        

    

def test(request):
    return render(request,'homepage/test05.html')

    