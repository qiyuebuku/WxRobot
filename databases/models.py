from django.db import models


# Create your models here.




class SelectedGroups(models.Model):
    # group_name = models.CharField(max_length=32)
    gid = models.CharField(max_length=16,primary_key=True)
    wechat_id = models.ForeignKey('WechatId',on_delete=models.CASCADE)


class SelectedFriends(models.Model):
    # friend_name = models.CharField(max_length=32)
    fid = models.CharField(max_length=16,primary_key=True)
    wechat_id = models.ForeignKey('WechatId',on_delete=models.CASCADE)

class WechatId(models.Model):
    puid = models.CharField(max_length=32,null=False,unique=True)
    user_info = models.ForeignKey('UserInfo',on_delete=models.CASCADE,default=1)
    isActive = models.BooleanField(default=True)

class Plugs(models.Model):
    ptitle = models.CharField(max_length=32,unique=True,verbose_name = "插件名称",null=False)
    pdescribe = models.TextField(verbose_name="插件描述")
    plug_path = models.FileField(upload_to="static/upload/Plugs",verbose_name="插件文件",null=False)
    wake_word = models.CharField(max_length = 128, null=False)
    isActive = models.BooleanField(default=True)


class UserInfo(models.Model):
    username = models.CharField(max_length=32,unique=True)
    userpwd = models.CharField(max_length=32)
    uemail = models.EmailField()
    # user_plugs = models.ManyToManyField(UserPlugs)
    isActive = models.BooleanField(default=True)

class UserPlugs(models.Model):
    isActive = models.BooleanField(default=True)
    plug = models.ForeignKey(Plugs,on_delete=models.CASCADE)
    user_info = models.ForeignKey(UserInfo,on_delete=models.CASCADE)

