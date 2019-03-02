import base64
from threading import Thread
import time
from wxpy import *
# from wordcloud import WordCloud
# import jieba
# import matplotlib.pyplot as plt
# import numpy as np
# from PIL import Image


class Active_object_manager(Thread):
    def __init__(self,*,beat_timeout=60,inspection_interval=10):
        """
        :param beat_timeout 心跳的超时时间
        :param inspection_interval 检测间隔时间
        """

        super().__init__()
        self.has_logged = {}
        self.beat_timeout = beat_timeout
        self.inspection_interval = inspection_interval
    def run(self):
        """
            将心跳超时且没有开启任何功能的用户踢出去
        """
        while True:
            has_logged = self.has_logged
            current_time = time.time()
            cleaner_uuid = []
            for puid in has_logged:
                # 将当前时间退回到30秒前，依次和每个对象最近一次汇报心跳的时间作对比
                # 如果大于他，说明这个对象的汇报超时了，则将其踢出
                if self.has_logged[puid]['date']<(current_time-self.beat_timeout):
                    print('上次汇报时间：',time.ctime(self.has_logged[puid]['date']))
                    print('当前时间：',time.ctime(current_time))
                    print('puid:%s，心跳超时%s秒'%(puid,(current_time-self.beat_timeout-self.has_logged[puid]['date']) ))
                    cleaner_uuid.append(puid)

            for puid in cleaner_uuid:
                if self.cleaner(puid): 
                    print('将%s从字典清理完成'%puid)
            time.sleep(self.inspection_interval)
    
    def cleaner(self,bot_puid):
        try:
            # 从字典当中删除
            self.has_logged[bot_puid]['bot'].logout()
            del self.has_logged[bot_puid]
            return True
        except Exception as e:
            print('将%s从监控字典清理失败，失败原因：%s'%(bot_puid,e))
            return False
    
    def get_bot_dict(self,bot_puid):
        try:
            # 获取机器人对象
            bot_dict = self.has_logged[bot_puid]
            # print(bot_dict)
        except (KeyError,AttributeError,):
            return None
        return bot_dict
    
    # 获取登陆者的详细信息
    def bot_details(self,bot_puid):
        """
        :param bot_uuid 机器人的uuid标识符
        :return 名称、头像，微信ID
        """
        print(bot_puid)
        bot_dict = self.get_bot_dict(bot_puid)
        if  not bot_dict:
            return None 
        bot = bot_dict.get('bot')
        # 获取对象的详细信息
        user_details = bot.user_details(bot.self)
        # print(dir(user_details))
        # 微信名称
        USER_NAME =user_details.name
        # 微信头像
        AVATAR_BYTES = base64.b64encode(user_details.get_avatar()).decode() 
        # 微信ID号
        WXID = user_details.wxid
        # 性别
        SEX = user_details.sex
        # 省份
        PROVINCE = user_details.province 
        # 城市
        CITY = user_details.city
        # 个性签名
        SIGNATURE = user_details.signature
        # PUID = user_details.puid
        details={
            'user_name':USER_NAME,
            'avatar':AVATAR_BYTES,
            'wxid':WXID,
            'status':'正常',
            'sex' : SEX,
            'province' : PROVINCE,
            'city' : CITY,
            'signature' : SIGNATURE,
            # 'puid': PUID,
        }
        return details

    def add_logged(self,bot):
        puid = bot.user_details(bot.self).puid      
        self.has_logged[puid]={'bot':bot,'date':time.time()}
        print('开始数据分析')
        # 开始数据分析
        t = Data_analysis(bot)
        t.start()





aom = Active_object_manager(beat_timeout=60)
aom.setDaemon(True)
aom.start()




class Data_analysis(Thread):
    def __init__(self,Bot):
        super().__init__()
        self.Bot = Bot 
        self.puid = Bot.user_details(Bot.self).puid
        self.Bot.result = None
    def run(self):
        # 获取所有好友
        friends = self.Bot.friends(update=True)

        # 获取好友的数量
        friends_count = len(friends)
        # 获取群聊数量
        # 一些不活跃的群可能无法被获取到，可通过在群内发言，或修改群名称的方式来激活
        groups_count = len(self.Bot.groups(update=True))
        # 获取公众号数量
        msp_count = len(self.Bot.mps(update=True))
        # 获取所有人的性别
        gender_statistics = {'male':len(friends.search(sex=MALE)),'female':len(friends.search(sex=FEMALE)),'secrecy':len(friends.search(sex=None))}
         # 获取所有人的个性签名
        signatures = {i.name:i.signature for i in friends }
        # 创建词云
        # world_cloud = self.create_world_cloud(signatures,'/home/tarena/WxRobot/homepage/static/img/color_mask.jpg')
        # 获取所有人的所在城市
        region={f.name:f.province for f in friends}
        result_data = {
            'friends_count':friends_count,
            'groups_count':groups_count,
            'msp_count':msp_count,
            # 'world_cloud':world_cloud,
            'gender_statistics':gender_statistics,
            'region':region
        }
        # print(result_data)
        self.Bot.result = result_data

    def create_world_cloud(self,text,img_path):
        text = text 
        color_mask_path = img_path
        cut_text =" ".join(jieba.cut(" ".join(text)))
        color_mask = np.array(Image.open(color_mask_path))
        cloud = WordCloud(
            #设置字体，不指定就会出现乱码
            # font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
            #设置背景色
            background_color='white',
            #词云形状
            mask=color_mask,
            #允许最大词汇
            max_words=2000,
            #最大号字体
            max_font_size=40,
        )
        
        wCloud = cloud.generate(cut_text)
        
        # 返回生成好词云对象
        world_cloud = wCloud.to_image().tobytes()
        return world_cloud
        # return  base64.b64encode(world_cloud).decode()


class Create_world_cloud(Thread):
    def __init__(self,text,img_path):
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
        cut_text =" ".join(jieba.cut(" ".join(text)))
        color_mask = np.array(Image.open(color_mask_path))
        cloud = WordCloud(
            #设置字体，不指定就会出现乱码
            # font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
            #设置背景色
            background_color='white',
            #词云形状
            mask=color_mask,
            #允许最大词汇
            max_words=2000,
            #最大号字体
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
        

    def imageToStr(self,image):
        #先将图片转换位byte类型，然后再转换为str    
        image_str=base64.b64encode(image).decode('ascii') 
        return image_str