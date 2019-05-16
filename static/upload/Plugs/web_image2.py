import requests
import json
import urllib
import re



def getSogouImag(category):
    cate = category
    try :
        # 初次请求图片时,json文件未被创建
        data = json.load(fp=open("test_info.json"))
        # 请求不同主题的图片
        assert cate in data,'not_exist'
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
            imgs_url.append(j['thumbUrl'])
    # 请求相同主题的图片
    else:
            with open('image_info') as f:
                m = int(f.read())
            imgs_url = data[cate]
        
    # 存储请求次数
    m = m+1
    with open('image_info','w') as f:
        f.write(str(m))
    # 获取图片url
    img_url=imgs_url.pop(0)
    # 更新json文本
    data[cate] = imgs_url
    json.dump(obj=data,fp=open("./test_info.json",'w'))
    # 获取图片流
    img = requests.get(img_url).content
    filname = cate+str(m)+'.jpg'
    with open(filname,'wb') as f:
        f.write(img)
    return filname

def main(msg,fd2):
    pattern = "(\w+)图片"
    s = "壁纸图片"
    cata=re.findall(pattern,s)[0]
    filename = getSogouImag(cata)
    print(filename)
    fd2.send(filename)
