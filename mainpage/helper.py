import base64
from threading import Thread
import time
from wordcloud import WordCloud
import cv2
import jieba
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

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





aom = Active_object_manager(beat_timeout=60)
aom.setDaemon(True)
aom.start()




class Data_analysis(object):
    def __init__(self,Bot):
        self.Bot = Bot 
        self.puid = Bot.user_details(Bot.self).puid
    def get_analysis_result(self):
        # 获取所有好友
        friends = self.Bot.friends(update=True)

        # 获取所有好友的数量
        friends_count = len(friends)
        # 获取所有群聊数量
        # 一些不活跃的群可能无法被获取到，可通过在群内发言，或修改群名称的方式来激活
        groups_count = len(self.Bot.groups(update=True))
        # 获取所有公众号数量
        msp_count = len(self.Bot.mps(update=True))
        # 获取所有人的性别字典
        gender_statistics = {'male':len(friends.search(sex='MALE')),'female':len(friends.search(sex='FEMALE')),'secrecy':len(friends.search(sex='None'))}
        # 获取所有人的个性签名
        signatures = {i.name:i.signature for i in friends}
        # 获取所有人的所在地区
        # 优先获取市，如果没有则返回省
        region={}
        for f in friends:
            region[f.name] = f.city if f.city else f.province


        result_data = {
            'friends_count':friends_count,
            'groups_count':groups_count,
            'msp_count':msp_count,
            'gender_statistics':gender_statistics,
            'signatures':self.word_cloud(signatures.values(),r'mainpage\static\img\color_mask.jpg'),
            'region':region
        }

        return result_data

    def word_cloud(self,text,color_mask_path):
        """
        功能：将text按照img的形状做呈现出词云
        :param text 需要呈现的文字，词组
        :param color_mask_path 参照图路径地址
        :return 制作完成的bytes格式图片
        """
        print(text)
        cut_text =" ".join(jieba.cut(" ".join(text)))
        color_mask = np.array(Image.open(color_mask_path))
        cloud = WordCloud(
            #设置字体，不指定就会出现乱码
            font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
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
        img = wCloud.to_image()

        return img.tobytes()
        # # print()
        # # wCloud.to_file('cloud.jpg')
        # print(wCloud.to_image)
        
        # import matplotlib.pyplot as plt
        # plt.imshow(wCloud, interpolation='bilinear')
        # plt.axis('off')
        # plt.show()
