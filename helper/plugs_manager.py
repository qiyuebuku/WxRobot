from databases import models
from django.db.models.signals import post_save ,post_delete
import os 
import zipfile 
from django.db.models import F
import shutil
from imp import reload 
# from static.upload.Plugs import helloworld_7ds3mNe
class Plugs_management():
    def __init__(self):
        self.register_plugs = {}
        for plug in models.Plugs.objects.filter(isActive=True):
            self.add_plug(plug,mode=False)
               
    def add_plug(self,plug,mode=True):

        if plug.ptitle == "delete_success":
            print('插件重复，清理完成')
            return 
        try:
            # 获取文件路径
            file_path = plug.plug.path 
            # 查看新添加的插件路径是否已经存在与数据库当中
            flag = False
            repetition = False
            for i in models.Plugs.objects.all():
                if plug.plug.name == i.plug.name:
                    if repetition == True:
                        flag = True
                        os.remove(file_path)
                        break 
                    repetition = True

                    
                    
            # 判断文件是否是zip格式
            # 如果不是,则将其从数据库和plug中删除
            if file_path[-3:] != "zip" or flag :
                # 将名称改为delete表示已经删除
                plug.ptitle = "delete_success"
                plug.save()
                plug.delete()
            else:
                # 将上传的包，解压缩成文件夹
                if mode:
                    self.__unpack_plugin(file_path)
                attr_name = plug.plug.path.split('/')[-1:][0][:-4]
                print('正在加载插件:',attr_name)
                plug_path = "from static.upload.Plugs."+attr_name.title()+" import "+attr_name
                exec(plug_path)
                func = eval(attr_name)
                reload(func)
                # 将导入成功的插件添加到当前的对象中
                self.register_plugs[attr_name]=func
                # setattr(self,attr_name,func)
        # 如果导入文件时出现意外        
        except Exception as e:
            print('加载插件到内存失败，自动从数据库中取消激活',e)
            # 取消激活状态
            r = models.Plugs.objects.filter(plug = plug.plug).update(isActive=False)

    def __unpack_plugin(self,file_path):
        # 获取解压的路径
        l = file_path.split("/")
        # 将包名的首字母转换为大写，然后作为文件夹名称
        dir_name = l[-1][:-4].title()
        # 将路径和文件名成拼接，组成新的路径
        un_path = "/".join( l[:-1] )+"/"+dir_name
        # 创建一个用于读取zip包的对象
        z = zipfile.ZipFile(file_path,'r')
        # 解压缩
        z.extractall(path = un_path)
        # 删除解压缩完成后的包        
        os.remove(file_path)
        print('删除文件：',file_path)
        # 返回解压缩完成后的文件夹
        # return dir_name
    

    def del_plug(self,plug):
        try:
            print(plug)
            if not plug.ptitle == "delete_success":
                attr_name = plug.plug.path.split('/')[-1:][0][:-4]
                print("attr_name",attr_name)
                file_path = plug.plug.path 
                # 获取解压的路径
                l = file_path.split("/")
                # 将包名的首字母转换为大写，然后作为文件夹名称
                dir_name = l[-1][:-4].title()
                print(dir_name)
                # 将路径和文件名成拼接，组成新的路径
                unpath = "/".join( l[:-1] )+"/"+dir_name
                shutil.rmtree(unpath)
                del self.register_plugs[attr_name]
                print('从内存中删除插件成功')
                return True 
            return False
        except Exception as e:
            print('从内存中删除失败',e)
            return False

# 创建插件管理对象
plugs_management = Plugs_management()
# 执行测试插件
# plugs_management.helloworld.main()
# 打印已注册插件列表
# print(plugs_management.register_plugs)



def post_save_func(sender,**kwargs):
    print("post_save_msg:",sender)
    if sender == models.Plugs:
        instance = kwargs['instance']
        plugs_management.add_plug(instance)
        print("添加后的注册插件为：",plugs_management.register_plugs)



def post_delete_func(sender,**kwargs):
    print("post_delete_msg:",sender)
    if sender == models.Plugs:
        instance = kwargs['instance']
        plugs_management.del_plug(instance)
        print("删除后的注册插件为：",plugs_management.register_plugs)



# 指定数据库触发保存操作时的回调函数
post_save.connect(post_save_func)
# 指定数据库触发删除操作是的回调函数
post_delete.connect(post_delete_func)
