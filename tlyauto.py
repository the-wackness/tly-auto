import time
import requests
import base64
import json
import os
from datetime import datetime

cookie = os.environ["COOKIE1"] #账号cookie  因为$前面是大写所以也是大写 COOKIE1是在yml里面env写的
token = os.environ["TOKEN"] #验证码token
#token在http://www.bhshare.cn/imgcode/ 自行申请


def imgcode_online(imgurl):
    _custom_url = "http://api.jfbym.com/api/YmServer/customApi"
    _token = token
    verify_type="10110"
    _headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "image": imgurl,
        "token": _token,
        "type": verify_type
    }
    # print(payload)
    resp = requests.post(_custom_url, headers=_headers, data=json.dumps(payload))
    print(resp.text)
    result = json.loads(resp.text)
    if result['code'] == 200:
        print('result return:')
        print(result['data'])
        return result['data']
    else:
        print('msg:')
        print(result['msg'])
        return result['data']
    # return resp.json()['data']['data']


# def imgcode_online(imgurl):
#     data = {
   
#         'token': token,
#         'type': 'online',
#         'uri': imgurl
#     }
#     response = requests.post('http://www.bhshare.cn/imgcode/', data=data)
#     print(response.text)
#     result = json.loads(response.text)
#     if result['code'] == 200:
#         print(result['data'])
#         return result['data']
#     else:
#         print(result['msg'])
#         return 'error'


def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()




def tly():
    signUrl="https://tly31.com/modules/index.php"
    hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','Cookie':cookie}

    res=requests.get(url=signUrl,headers=hearder).text
    signtime=getmidstring(res,'<p>上次签到时间：<code>','</code></p>')
    timeArray = time.strptime(signtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    t = int(time.time())
    #86400是一天
    if t-timeStamp>60000:
        print("距上次签到时间大于24小时啦,可签到")
        #获取验证码图片
        captchaUrl="https://tly31.com/other/captcha.php"
        signurl="https://tly31.com/modules/_checkin.php?captcha="
        hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Cookie':cookie}
        res1=requests.get(url=captchaUrl,headers=hearder)
        base64_data = base64.b64encode(res1.content).decode()
        oocr=imgcode_online(base64_data)
        print(oocr)
        # base64_data = base64.b64encode(res1.content)
        # oocr=imgcode_online('data:image/jpeg;base64,'+str(base64_data, 'utf-8'))
        res2=requests.get(url=signurl+oocr.upper(),headers=hearder).text
        print('res2')
        print(res2)
    else:
        print("还未到时间！",t-timeStamp)




    
 


def main_handler(event, context):
    tly()


if __name__ == '__main__':

    tly()





