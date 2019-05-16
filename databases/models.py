from django.db import models


# Create your models here.


class SelectedGroups(models.Model):
    # group_name = models.CharField(max_length=32)
    gid = models.CharField(max_length=16, primary_key=True)
    wechat_id = models.ForeignKey('WechatId', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.gid)


class SelectedFriends(models.Model):
    # friend_name = models.CharField(max_length=32)
    fid = models.CharField(max_length=16, primary_key=True)
    wechat_id = models.ForeignKey('WechatId', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.fid)


class WechatId(models.Model):
    puid = models.CharField(max_length=32, null=False, unique=True)
    user_info = models.ForeignKey(
        'UserInfo', on_delete=models.CASCADE, default=1)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.puid)


class Plugs(models.Model):
    ptitle = models.CharField(
        max_length=32, unique=True, verbose_name="插件名称", null=False)
    pdescribe = models.TextField(verbose_name="插件描述")
    plug = models.FileField(upload_to="static/upload/Plugs",
                            verbose_name="插件文件", null=False)
    msg_type_list = (
        ("Text","文本"),
        ("Map","位置"),
        ("Card","名片"),
        ("Note","提示"),
        ("Sharing","分享"),
        ("Picture","图片"),
        ("Recording","语音"),
        ("Attachment","文件"),
        ("Video","视频"),
        ("Friends","好友请求"),
        ("System","系统")
    )
    msg_type = models.CharField(max_length=36,choices=msg_type_list,default="Text")
    wake_word = models.CharField(max_length=128,unique=True,null=True,blank=True ,verbose_name="触发关键字")
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return str(self.ptitle)

    @property
    def to_dict(self):
        dic = {
            'ptitle': self.ptitle,
            'pdescribe': self.pdescribe,
            'id':self.id
        }
        return dic



class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    userpwd = models.CharField(max_length=32)
    uemail = models.EmailField()
    isActive = models.BooleanField(default=True)

    clues = models.TextField(max_length=550,null=True,blank=True)
    clues_status = models.BooleanField(default=True)

    timer = models.TimeField(null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    repetition = models.CharField(max_length = 32,choices=(("everyday","每天"),("once","单次")), blank=True,null=True)
    timer_send_isActive = models.BooleanField(null=True,blank=True)
    def __str__(self):
        return str(self.username)


class UserPlugs(models.Model):
    isActive = models.BooleanField(default=False)
    plug = models.ForeignKey(Plugs, on_delete=models.CASCADE)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.plug)

class Test(models.Model):
    name = models.CharField(max_length=32)



WechatId.objects.all().update(isActive=False)

   

