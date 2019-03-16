# from django.db import models
#
# # Create your models here.
#
# # class intelligent_chat(models.Model):
# #     uid = models.IntegerField(primary_key=True)
# #     puid = models.CharField(max_length=20)
# #     name = models.CharField(max_length=20)
#
#
#
#
# class SelectedGroups(models.Model):
#     group_name = models.CharField(max_length=32)
#     wechat_id = models.ForeignKey('WechatId',on_delete=models.CASCADE)
#
#
# class SelectedFriends(models.Model):
#     friend_name = models.CharField(max_length=32)
#     wechat_id = models.ForeignKey('WechatId',on_delete=models.CASCADE)
#
# class WechatId(models.Model):
#     puid = models.CharField(max_length=32)
#     status = models.CharField(max_length=16)
#     # user_info = models.ForeignKey('UserInfo',on_delete=models.CASCADE)
#
# class UserInfo(models.Model):
#     username = models.CharField(max_length=32)
#     userpwd = models.CharField(max_length=32)
#     # we_chat_id = models.ForeignKey('WechatId',on_delete=models.CASCADE)
