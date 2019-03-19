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
    status =  models.NullBooleanField(default=True)  # 可以为空的布尔值
    user_info = models.ForeignKey('UserInfo',on_delete=models.CASCADE,default=1)

class UserInfo(models.Model):
    username = models.CharField(max_length=32,unique=True)
    userpwd = models.CharField(max_length=32)

