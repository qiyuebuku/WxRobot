import json
import base64
import sys
import urllib.request
from urllib import parse
import ssl
import requests


def get_Access_token(ak,sk):

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ak+'&client_secret='+sk

    request = urllib.request.Request(host)

    request.add_header('Content-Type', 'application/x-www-form-urlencoded')

    response = urllib.request.urlopen(request).read().decode('UTF-8')
    return  json.loads(response)['access_token']


# if (result):
#     print(result)

def read_image(img):
    # f = open(r'C:\Users\11946\Desktop\plug\c381299a8c2a73516b92c4fec010e562f428f1fe065d5f8491948379f37c3757.jpg', 'rb')
    img = base64.b64encode(img)
    return img 


def get_info(access_token,img):
    params = {"image":img}
    params = parse.urlencode(params)
    host = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'
    headers={
    'Content-Type':'application/x-www-form-urlencoded'
    }
    request_url = host+'?access_token='+access_token

    data={'access_token':access_token,'image':img,'baike_num':1}
    res = requests.post(url=request_url,headers=headers,data=data)
    return res.json()

def parse_info(req):
    result = [{'type':"@msg@",'content':"百度百科："+req['result'][0]["baike_info"].get('baike_url','没有百科到信息')}]
    for index,row in enumerate(req['result'][1:]):
        # 百科的地址作为第一个元素
        item = []
        row['score'] = str(row['score'])
        # print(row.values())
        for r in row.values():
            item.append(str(r))
        result.append({'type':"@msg@",'content':'，'.join(item)})
    return result

def main(msg,plug_dir,fd2):
# def main():
    msg.reply("正在帮您进行图像识别")
    access_token = get_Access_token("0XlXeb0HUENBgGrd3xan0Gt2","bnIfKgdkmanPdhEswva58bL2metRGQEd")
    # print(msg.get_file())
    img = read_image(msg.get_file())
    info = get_info(access_token,img)
    result = parse_info(info)
    #将结果返回到主进程
    fd2.send(result)

# main()

