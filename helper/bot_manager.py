import json
import base64
from threading import Thread
import time
from wxpy import *
from helper import bot_manager as bm
from helper.channels_manager import logged_channels as lc
from databases import models
# from wordcloud import WordCloud
# import jieba
# import matplotlib.pyplot as plt
# import numpy as np
# from PIL import Image




class Plugs_management():
    pass 







class Data_analysis(Thread):
    def __init__(self, Bot ,callback_analysis_result,username):
        super().__init__()
        self.Bot = Bot 
        self.puid = Bot.user_details(Bot.self).puid
        self.Bot.result = None
        self.callback_analysis_result = callback_analysis_result
        self.username = username

    def run(self):
        # 获取所有好友
        friends = self.Bot.friends(update=True)

        # 获取好友的数量
        friends_count = len(friends[1:])
        # 获取群聊数量
        # 一些不活跃的群可能无法被获取到，可通过在群内发言，或修改群名称的方式来激活
        groups_count = len(self.Bot.groups(update=True))
        # 获取公众号数量
        msp_count = len(self.Bot.mps(update=True))
        # 获取所有人的性别
        gender_statistics = {'male': len(friends.search(sex=MALE)), 'female': len(
            friends.search(sex=FEMALE)), 'secrecy': len(friends.search(sex=None))}
         # 获取所有人的个性签名
        signatures = {i.name: i.signature for i in friends}
        # 创建词云
        # world_cloud = self.create_world_cloud(signatures,'/home/tarena/WxRobot/homepage/static/img/color_mask.jpg')
        # 获取所有人的所在城市
        region = {f.name: f.province for f in friends}
        result_data = {
            'friends_count': friends_count,
            'groups_count': groups_count,
            'msp_count': msp_count,
            # 'world_cloud':world_cloud,
            'gender_statistics': gender_statistics,
            'region': region
        }
        # print(result_data)
        self.callback_analysis_result(result_data,self.username)

    def create_world_cloud(self, text, img_path):
        text = text
        color_mask_path = img_path
        cut_text = " ".join(jieba.cut(" ".join(text)))
        color_mask = np.array(Image.open(color_mask_path))
        cloud = WordCloud(
            # 设置字体，不指定就会出现乱码
            # font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
            # 设置背景色
            background_color='white',
            # 词云形状
            mask=color_mask,
            # 允许最大词汇
            max_words=2000,
            # 最大号字体
            max_font_size=40,
        )

        wCloud = cloud.generate(cut_text)

        # 返回生成好词云对象
        world_cloud = wCloud.to_image().tobytes()
        return world_cloud
        # return  base64.b64encode(world_cloud).decode()


class Create_world_cloud(Thread):
    def __init__(self, text, img_path):
        """
        功能：将text按照img的形状做呈现出词云
        :param text 需要呈现的文字，词组
        :param color_mask_path 参照图路径地址
        :return 制作完成的bytes格式图片
        """
        super().__init__()
        self.text = text
        self.img_path = img_path
        self.world_cloud = None

    def run():
        text = self.text
        color_mask_path = self.img_path
        cut_text = " ".join(jieba.cut(" ".join(text)))
        color_mask = np.array(Image.open(color_mask_path))
        cloud = WordCloud(
            # 设置字体，不指定就会出现乱码
            # font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
            # 设置背景色
            background_color='white',
            # 词云形状
            mask=color_mask,
            # 允许最大词汇
            max_words=2000,
            # 最大号字体
            max_font_size=40,
        )

        wCloud = cloud.generate(cut_text)
        # 返回生成好词云对象
        self.world_cloud = wCloud.to_image()

    def get_bytes_cloud(self):
        '''
        :return　bytest格式的词云图片
        '''
        if self.world_cloud:
            return self.world_cloud.tobytes()
        else:
            return None

    def get_str_cloud(self):
        '''
        :return str格式的词云图片
        '''
        if self.world_cloud:
            image = self.world_cloud.tobytes()
            return self.imageToStr(image)
        else:
            return None

    def imageToStr(self, image):
        # 先将图片转换位byte类型，然后再转换为str
        image_str = base64.b64encode(image).decode('ascii')
        return image_str


class Robot_management():

    def __init__(self):
        self.robots = {}

    def get_basic_data(self, puid , username):
        """
        初始化登陆者的详细信息
        :param bot_uuid 机器人的uuid标识符
        :return 名称、头像，微信ID
        """
        # bot_dict = self.get_bot_dict(bot_puid)
        bot = self.get_bot(puid)
        if not bot:
            return None 
        print("get_bot:-----------------------------",bot)
        # 获取登陆者的详细信息
        user_details = bot.user_details(bot.self)

        # 获取插件用户所拥有插件信息                                               
        plug_querys = models.UserInfo.objects.filter(username = username).first().userplugs_set.all()
        user_plugs = [plug_query for plug_query in plug_querys if plug_query.plug.isActive]
        print("plugs",user_plugs)
        details={
        # 微信名称
            'user_name':user_details.name,
        # 微信头像
            'avatar':base64.b64encode(user_details.get_avatar()).decode() ,
        # 微信ID号
            'status':'正常',
        # 性别
            'sex' : user_details.sex,
        # 省份
            'province' : user_details.province,
        # 城市
            'city' : user_details.city,
        # 个性签名
            'signature' : user_details.signature,
        # 用户的插件
            'user_plugs':user_plugs,
        # 当前登录的用户名
            'username':username,
        }
        return details

    def start_data_analysis(self,puid,username):
        """
            数据分析入口函数
        """
        print("开始进行数据分析")
        bot = self.get_bot(puid)
        data_analysis = Data_analysis(bot,self.callback_analysis_result,username = username)
        data_analysis.start()


    def callback_analysis_result(self,data,username):
        """
            数据分析完成后的回调函数
        """
        channel = lc.get_channels(username=username)
        print('callback_analysis_result')
        channel.reply_channel.send({
            'text': json.dumps({
                'analysis_result':data
            })
        })


    def get_data_intelligent(self,puid,username,data_intelligent=None):
        """
            同步的方式获取好友和群组信息
        """

        #已被选中的好友
        select_friends =[f.fid for f in models.SelectedFriends.objects.all()]  

        #已被选中的群组
        select_groups = [g.gid for g in models.SelectedGroups.objects.all()] 

        # print(dir(select_friends),select_groups,sep="\n")

        


        print("正在：同步的方式获取好友和群组信息")
        bot = self.get_bot(puid)
        # 获取登陆者的好友和群组的详细信息
        groups = bot.groups(update = True)
        group_infos = []
        for group in groups:
            group.update_group(True)
        
            gname = group.name
            # print("群名称：",gname)
        
            gowner = group.owner.name  #群主
            # print("群主：",gowner)
        
            #所有群成员
            members = group.members
            # print("群内成员：",group.members)
        
            # 统计性别
            mtfratio = {'male':len(members.search(sex=MALE)),'female':len(members.search(sex=FEMALE)),'secrecy':len(members.search(sex=None))}
            # print(mtfratio)

            selected = True if group.puid in select_groups else False
            # print("group_selected:",selected)
            pcount = len(members)  #群成员数量
            group_infos.append({'gname':gname,'gowner':gowner,'pcount':pcount,'mtfratio':mtfratio,'puid':group.puid,'selected':selected})
            
            # group_infos.append({'gname':gname,'gowner':gowner,'pcount':pcount,'puid':group.puid})
        
        friends = bot.friends(update=True)[1:]
        user_infos = []
        sex_dict = {0:'保密',1:'男',2:'女'}
        for friend in friends:
            uname = friend.name
            usex = sex_dict[friend.sex]
            puid = friend.puid
            selected = True if friend.puid in select_friends else False
            # print("friend_selected",selected)
            user_infos.append({'uname':uname,'usex':usex,'puid':friend.puid,'selected':selected})


        ug_detail_info={'user_info':user_infos,'group_info':group_infos}
        # 如果回调函数不为空，则调用回调函数
        if data_intelligent:
            print("调用回调函数返回：data_intelligent")
            data_intelligent(ug_detail_info,username)
        #直接返回
        else:
            print("直接返回：data_intelligent")
            return ug_detail_info

    def start_data_intelligent(self,puid,username):
        """
            异步的方式获取好友和群组数据
            return : 通过回调函数＂callback_data_intelligent＂反馈结果，参数为：data,username
        """
        # 创建线程
        data_intelligent = Thread(
            target=self.get_data_intelligent,
            args=(
                puid,username,
                self.callback_data_intelligent
        ))
        data_intelligent.start()
        print('启动：start_data_intelligent')

    def callback_data_intelligent(self,data,username):
        """
            数据分析完成后的回调函数
        """
        # print(data,username)
        channel = lc.get_channels(username=username)

        channel.reply_channel.send({
            'text': json.dumps({
                'intelligent_result':data
            })
        })
    


        

    # 增加需要被管理的机器人
    def add_bot(self, puid, bot ,username):
        """
            用于将需要被管理的机器人线程加入进来
            :param bot_uuid 
                * 机器人的uuid号
            :param bot
        """
        fs = Functional_scheduler(bot,username)
        fs.setDaemon(True)
        fs.start()
        self.robots[puid] =[bot,fs]




    def get_bot(self, puid):
        try:
            print("get_bot------------------------",self.robots[puid][0])
            return self.robots[puid][0]
        except:
            return None

    def get_fs(self,puid):
        try:
            return self.robots[puid][1] 
        except:
            return None 

    def del_bot(self,puid):
        del self.robots[puid]

    


robot_management = Robot_management()



class Functional_scheduler(Thread):
    def __init__(self,bot,username):
        super().__init__()
        self.bot = bot 
        self.username = username
        self.friends = []
        self.groups = []
        self.select_function = {}
        tuling = Tuling(api_key='91bfe84c2b2e437fac1cdb0c571cac91')

    def run(self):
        self.functional_scheduler()

    def functional_scheduler(self):
        bot = self.bot  
        friends = self.friends 
        groups = self.groups 

   

        @bot.register(self.friends)
        def friends_message(msg):
            print('[接收来自好友：]' + str(msg))
            if (msg.type != 'Text'):
                ret = '[奸笑][奸笑]'
            else:
                print('准备调用图灵')
                ret = self.tuling.do_reply(msg)
                print("ret",ret)
            print('[发送]' + str(ret))
            return ret

        @bot.register(self.groups)
        def group_message(msg):
            print('[接收来自群聊：]' + str(msg))
            if msg.is_at:
                if (msg.type != 'Text'):
                    ret = '[奸笑][奸笑]'
                else:
                    ret = self.tuling.reply_text(msg)
                    print("ret",ret)

                print('[发送]' + str(ret))
                return ret


    def refresh_listening_obj(self,puid):
        print('================----------------================')
        bot = robot_management.get_bot(puid)
        print(puid,bot,sep='\n')

        # 获取所有的好友和群组对象
        friends = bot.friends()   #获取更新好友列表
        groups = bot.groups()

        # 从数据库中获取所有已经被选中的好友和群组puid
        m_friends = models.SelectedFriends.objects.all()
        m_groups = models.SelectedGroups.objects.all()

        # 用从数据库中查找出已被选中的好友或者群组Puid获取对应的对象
        select_friends = []
        select_groups = []

        # 清空上一次的选中的内容
        self.friends.clear() 
        self.groups.clear()
        # 两种方法，列表生成式和普通遍历
        # self.friends = [friends.search(puid == f.puid) for f in m_friends if friends.search(puid == f.puid)]
        for f in m_friends:
            friend = friends.search(puid =f.fid)
            if friend and friend[0] not in self.friends:
                print("添加好友：",friend[0])
                self.friends.append(friend[0])
        # self.groups = [groups.search(puid == g.puid) for g in m_groups if groups.search(puid == g.puid)]
        for g in m_groups:
            group = groups.search(puid =g.gid)
            if group and groups[0] not in self.groups:
                print("添加群聊：",group[0])
                self.groups.append(group[0])
        # print(self.friends,self.groups,sep="\n")

        

    def refresh_function(self):
        # 获取插件用户所拥有插件信息                                               
        plug_querys = models.UserInfo.objects.filter(username = self.username).first().userplugs_set.filter(isActive=True)
        # 清空所有原先功能状态
        self.select_function.clear()
        for plug_query in plug_querys:
            if not plug_query.plug.isActive:
                continue
            plug = plug_query.plug
            self.select_function[plug.wake_word] = {'name':plug.ptitle,'plug_path':plug.plug_path}

        print("select_function",self.select_function)







    



