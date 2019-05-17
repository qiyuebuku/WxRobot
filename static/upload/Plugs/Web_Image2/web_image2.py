"""
必须将程序写入到main函数里
:params msg 接收到的消息对象
:params plug_dir 插件所在的路径
:params fd2 用于将处理好的结果返回给用户
    - 由 类型 和 内容 两个部分组成，若 省略类型，将作为纯文本消息发送
    - 类型 部分可为: ‘@fil@’, ‘@img@’, ‘@msg@’, ‘@vid@’ (不含引号)
    - 分别表示: 文件，图片，纯文本，视频
    - 内容 部分可为: 文件、图片、视频的路径，或纯文本的内容
"""
# <function main at 0x7fb5406ca488>
# <function main at 0x7fb5406ca488>
# <function main at 0x7fb5406ca488>

# <function main at 0x7fb5406a80d0>
from xpinyin import Pinyin
import requests
import json
import urllib
import re

pin = Pinyin()



def getSogouImag(category,plug_dir):
    cate = category
    try :
        # 初次请求图片时,json文件未被创建
        data = json.load(fp=open(plug_dir+"/test_info.json"))
        # 请求不同主题的图片
        assert pin.get_pinyin(cate,"") in data,'not_exist'
    except:
        m = 0
        data = {}
        #　爬取图片的url 
        imgs = requests.get('https://pic.sogou.com/pics?query='+cate+'start=0&reqType=ajax')
        # 将json格式的字符串转换成python数据类型
        jd = json.loads(imgs.text)
        # 数据处理
        jd = jd['items']
        imgs_url = []
        for j in jd:
            # 存储图片下载地址的url
            print(imgs_url)
            imgs_url.append(j['thumbUrl'])
    # 请求相同主题的图片
    else:
            with open(plug_dir+'/image_info') as f:
                m = int(f.read())
            imgs_url = data[pin.get_pinyin(cate,"")]
        
    # 存储请求次数
    m = m+1
    with open(plug_dir+'/image_info','w') as f:
        f.write(str(m))
    # 获取图片url
    img_url=imgs_url.pop(0)
    # 更新json文本
    data[pin.get_pinyin(cate,"")] = imgs_url
    json.dump(obj=data,fp=open(plug_dir+"/test_info.json",'w'))
    # 获取图片流
    img = requests.get(img_url).content
    filname = plug_dir+"/"+pin.get_pinyin(cate,"")+str(m)+'.jpg'
    with open(filname,'wb') as f:
        f.write(img)
    return filname
def main(msg,plug_dir,fd2):
    pattern = ":图片(\w+)"
    s = str(msg.text)
    if len(s)<=3:
       s +="美女"
    cata=re.findall(pattern,s)[0]
    filename = getSogouImag(cata,plug_dir)
    fd2.send({'type':"@img@",'content':filename})
