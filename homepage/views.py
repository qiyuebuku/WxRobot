<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from homepage import helper
from helper.debug import debug
import time
import json
from wxpy import *
from databases import models
from helper.bot_manager import robot_management as rm
import os
from django.views.decorators.csrf import csrf_exempt
import threading
from helper.channels_manager import cm

# from .forms import *
# Create your views here.

# 用户管理对象
# aom = helper.aom


def check_user(fun):
    """
        用于检测是否登陆成功
    """
    def function(request, *args, **kwargs):
        username = request.session.get('username')
        puid = request.session.get('puid')
        print("request.GET",request.GET)
        #用户已登录
        if request.GET.get('puid'):
            print('二维码扫描登录成功',request.GET.get('puid'))
            request.session['puid']=request.GET.get('puid')
            time.sleep(0.5)
            return fun(request, *args, **kwargs)
        elif puid:
            # 微信已经初始化
            print('session缓存登录成功')
            return fun(request, *args, **kwargs)
        elif username:
            print('用户未初始化微信')
            return redirect('/wx_init/')
        else:
            #用户未登录
            print('用户未登录')
            return redirect('/login/')
    return function


@check_user
def mainpage(request):
    print('这里是manpage....')
    if request.method == "GET":
        puid = request.session.get('puid')
        username = request.session.get('username')
        print(puid)
        basic_data = rm.get_basic_data(puid, username)
        # 如果获取到了用户的详细信息，则进入后台页面
        if basic_data:
            debug.print_l('%s的签名为：%s' % (
                basic_data['user_name'], basic_data['signature']))
            # 初始化数据分析页面
            rm.start_data_analysis(puid, username)
            # 初始化智能聊天页面
            rm.start_data_intelligent(puid, username)
            # 将数据库数据匹配到内存中
            fs = rm.get_fs(puid)
            fs.refresh_listening_obj(puid)
            fs.refresh_function()
            #启动
            return render(request, 'homepage/mainpage.html', basic_data)
        # else:
        #     print('登陆失败')
        def change_status():
            request.session['puid'] = None
            user = models.UserInfo.objects.filter(
                username=username
            ).first()
            if user:
                wechat = user.wechatid_set.filter(puid=puid).first()
                wechat.isActive = False
                wechat.save()
        t = threading.Thread(target=change_status)
        t.start()
        return HttpResponseRedirect('/wx_init/')

    elif request.method == "POST":
        # 获取puid
        puid = request.session.get('puid')
        # # 获取用户信息
        # bot_dict = aom.get_bot_dict(puid)
        # # 获取用户的bot对象
        # bot = bot_dict.get('bot')
        bot = rm.get_bot(puid)
        # 获取是哪个nav-item
        content_page = request.POST.get('content_page')[1:]
        if content_page == "custom_plug":
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
    # 获取id
    puid = request.session.get('puid')
    wechat_id = models.WechatId.objects.filter(puid=puid).first()

    # 获取被用户选中的好友和群组信息
    friends = json.loads(request.POST.get('friends'))
    groups = json.loads(request.POST.get('groups'))

    # 获取Functional_scheduler对象
    fs = rm.get_fs(puid)

    # 获取所有的好友和群组信息
    friends_all = fs.friends_all
    groups_all = fs.groups_all

    # 获取消息提醒和状态
    user_name = request.session['username']
    clues_status = models.UserInfo.objects.get(username=user_name).clues_status
    clues = models.UserInfo.objects.get(username=user_name).clues
    # print(clues_status)
    # 根据模式执行相应操作
    model = request.POST.get('model')
    # 创建模式
    if model == "true":
        # 好友
        for fid in friends:
            # 如果存在则替换，否则创建
            models.SelectedFriends.objects.update_or_create(
                fid=fid, wechat_id=wechat_id)
            if clues_status:
                friends = friends_all.search(puid=fid)
                # print('clues:', clues)
                # print("friends", friends)
        # 群组
        for gid in groups:
            # 如果存在则替换，否则创建
            models.SelectedGroups.objects.update_or_create(
                gid=gid, wechat_id=wechat_id)
            if clues_status:
                groups = groups_all.search(puid=gid)
                # print('clues:', clues)
                # print("groups", groups)
    # 删除模式
    else:
        print('删除好友%s' % friends)
        print('删除群组%s' % groups)
        models.SelectedFriends.objects.filter(fid__in=friends).delete()
        models.SelectedGroups.objects.filter(gid__in=groups).delete()
    # 更新调度器
    fs.refresh_listening_obj(puid)
    return HttpResponse('ok')


@csrf_exempt
def set_plugin_state(request):
    # print('这里是set_plugin_state')
    puid = request.session.get('puid')
    id = request.POST.get('id')
    ret_dict = {'status':True}
    try:
        plug = models.UserPlugs.objects.filter(id=id).first()

        # 获取所有已被选中的好友和群组
        select_obj = rm.select_obj(puid)
        # 如果要打开某个插件
        if request.POST.get('state') == "true":
            state = True
            text = "开启插件："
        # 如果要关闭某个插件
        else:
            state = False
            text = "关闭插件："
        # 更改插件状态，并且应社会数据库
        plug.isActive = state
        plug.save()

        # 给所有被关注的好友或者群聊发送提示信息
        for item in select_obj:
            for friend in select_obj[item]:
                plug_name = plug.plug.ptitle
                text += plug_name
                try:
                    friend.send(text+" 功能："+plug.plug.pdescribe)
                except:
                    pass
                # 为了防止发送消息频率过快导致意想不到的后果
                # 这里每发送一条消息，休息0.5秒
                time.sleep(0.5)

        # 更新调度器
        fs = rm.get_fs(puid)
        fs.refresh_function()
    except Exception as e:
        ret_dict['status'] = False
        print('获取插件失败：',e)
    return HttpResponse(json.dumps(ret_dict))


@csrf_exempt
def save_clues(request):
    text = request.POST.get('text')

    username = request.session.get('username')
    user = models.UserInfo.objects.filter(username=username).first()
    if user:
        user.clues = text
        user.save()
        print("保存成功：", text)
    return HttpResponse('ok')

    

def save_timer_send(request):
    timer = request.POST.get('timer')
    repetition = request.POST.get('repetition')
    text = request.POST.get('text') 
    timer_send_isActive = int(request.POST.get('timer_send_isActive'))
    print(timer,repetition,text,timer_send_isActive)
    if timer and repetition and text:
        username = request.session.get('username')
        user = models.UserInfo.objects.filter(username=username).first()
        user.timer = timer 
        user.repetition = repetition 
        user.text = text 
        user.timer_send_isActive = timer_send_isActive
        user.save() 

        puid = request.session.get('puid')
        fs = rm.get_fs(puid)
        if timer_send_isActive:
            # 将时间字符串转换为时间戳
            h,m = timer.strip().split(':')
            seconds = int(h)*3600+int(m)*60
            print("{0}被转换成时间戳后为：{1}".format(timer,seconds))
            
            print('正子重启定时发送')
            fs.stop_regularly_send()
            fs.start_regularly_send(seconds,text,repetition)
        else:
            print('正在关闭定时发送')
            fs.stop_regularly_send()
    return HttpResponse('ok')

def del_plug(request):
    plug_id = request.POST.get('id')
    print(plug_id)
    plug = models.UserPlugs.objects.filter(id = plug_id)
    if plug:
        plug.delete()
        return HttpResponse('ok')
    return HttpResponse('no')
    
def add_user_plug(request):
    plug_id = request.POST.get('id')
    res_dic = {"user_plug":{},'status':False}
    print("plug_id",plug_id)
    if plug_id:
        try:
            username = request.session.get('username')
            user = models.UserInfo.objects.filter(username=username).first()
            user_plug = models.UserPlugs.objects.create(plug_id=plug_id,user_info=user)
            print(user_plug)
            res_dic = {"user_plug":{'id':user_plug.id,'isActive':user_plug.isActive,'plug':user_plug.plug.to_dict},'status':True}
        except Exception as e:
            print('增加用户插件失败：',e)
    print(res_dic)
    return HttpResponse(json.dumps(res_dic))

     
def get_plug_shops(request):
    res_dic = {"already_have":[],'status':False}
    try:
        #  找出用户
        username = request.session.get('username')
        user = models.UserInfo.objects.filter(username=username).first()
        #　查询出数据库中用户所拥有的所有插件
        user_plugs = user.userplugs_set.all()
        print("user_plugs",user_plugs)
        # 还有商店中的所有插件
        shop_plugs = models.Plugs.objects.all() 
        print('商店插件：',shop_plugs)
        # 将两者进行对比，再标记出已被用户拥有的插件
        for user_plug in user_plugs:
            print('用户插件：',user_plug)
            if user_plug.plug in shop_plugs:
                res_dic['already_have'].append(user_plug.plug.to_dict)
        res_dic['status'] = True 
        print(res_dic)
    except Exception as e:
        print('获取商店插件失败：',e)
    print("商店插件",res_dic)
    return HttpResponse(json.dumps(res_dic))

def logout(request):
    username = request.session.get('username')
    puid = request.session.get('puid')
    print(puid)
    models.WechatId.objects.filter(puid=puid).update(isActive=False)
    del request.session['puid']

    # lc.del_channels(username)

    rm.del_bot(puid)

    return HttpResponseRedirect('/wx_init/')


def test(request):
    return render(request, 'homepage/test05.html')
=======
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
                basic_data = rm.get_basic_data(puid,username)
                # 如果获取到了用户的详细信息，则进入后台页面
                if basic_data:
                    debug.print_l('%s的签名为：%s'%(basic_data['user_name'],basic_data['signature']))
                    # 初始化数据分析页面
                    rm.start_data_analysis(puid,username)
                    # 初始化智能聊天页面
                    rm.start_data_intelligent(puid,username)
                    # 将数据库数据匹配到内存中
                    fs = rm.get_fs(puid)
                    fs.refresh_listening_obj(puid)
                    fs.refresh_function()
                    return render(request,'homepage/mainpage.html',basic_data)
        return HttpResponseRedirect('/wx_init/')  

    elif request.method == "POST":
        # 获取puid
        puid = request.session["user"].get('puid')
        # # 获取用户信息
        # bot_dict = aom.get_bot_dict(puid)
        # # 获取用户的bot对象
        # bot = bot_dict.get('bot')  
        bot = rm.get_bot(puid)
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
    model = request.POST.get('model')
    puid = request.session['user'].get('puid')
    wechat_id = models.WechatId.objects.filter(puid = puid).first()
    friends = json.loads(friends)
    groups = json.loads(groups)

    print(friends,groups,model)


    # 创建模式
    if model =="true":
        #好友
        for fid in friends:
            # 如果存在则替换，否则创建
            models.SelectedFriends.objects.update_or_create(fid=fid,wechat_id = wechat_id)
            # models.SelectedFriends.objects.create(fid=fid,friend_name=friend_name,wechat_id = wechat_id)
        #群组
        for gid in groups:
            # 如果存在则替换，否则创建
            models.SelectedGroups.objects.update_or_create(gid=gid,wechat_id = wechat_id)
            
    # 删除模式
    else:
        print('删除好友%s'%friends)
        print('删除群组%s'%groups)
        models.SelectedFriends.objects.filter(fid__in=friends).delete()
        models.SelectedGroups.objects.filter(gid__in=groups).delete()
    # 更新调度器
    fs = rm.get_fs(puid)
    fs.refresh_listening_obj(puid)
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
        
# def intelligent_switch(request):
#     status = request.GET.get('switch_status')
#     user = request.session.get('user')
#     if user:
#         puid = user.get('puid')
#         bot = rm.get_bot(puid)
#         print(status,puid,bot,sep='\n')
#         if bot :
#             # 如果为打开状态
#             if status == "true":
#                 # 获取所有的好友和群组对象
#                 friends = bot.friends()   #获取更新好友列表
#                 groups = bot.groups()

#                 # 从数据库中获取所有已经被选中的好友和群组puid
#                 m_friends = models.SelectedFriends.objects.all()
#                 m_groups = models.SelectedGroups.objects.all()

#                 # 用从数据库中查找出已被选中的好友或者群组Puid获取对应的对象
#                 select_friends = []
#                 select_groups = []
#                 # 两种方法，列表生成式和普通遍历
#                 # self.friends = [friends.search(puid == f.puid) for f in m_friends if friends.search(puid == f.puid)]
#                 for f in m_friends:
#                     friend = friends.search(puid =f.fid)
#                     if friend:
#                         select_friends.append(friend[0])
#                 # self.groups = [groups.search(puid == g.puid) for g in m_groups if groups.search(puid == g.puid)]
#                 for g in m_groups:
#                     group = groups.search(puid =g.gid)
#                     if group:
#                         select_groups.append(group[0])

#                 # 创建智能聊天对象
#                 # select_friends = friends.search("好好生活")
#                 # print(friends,select_friends,sep="\n-************************************************\n")

#                 it = intelligent_chat(bot,select_friends,groups=select_groups)
#                 return HttpResponse('开启成功')
#             else:
#                 return HttpResponse('关闭成功')
#         return HttpResponse('error')



@csrf_exempt
def set_plugin_state(request):
    print('这里是set_plugin_state')
    puid = request.session['user'].get('puid')
    id = request.POST.get('id')
    state =True if request.POST.get('state') == "true" else False
    # print(id,state)
    models.UserPlugs.objects.filter(id = id).update(isActive=state)

    # 更新调度器
    fs = rm.get_fs(puid)
    fs.refresh_function()
    
    return HttpResponse('ok')



    

def test(request):
    return render(request,'homepage/test05.html')

    
>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
