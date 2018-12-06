import re
import json
import requests
from time import sleep
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SPVOICE")

print('机器人:您好，我是聊天机器人菲菲。')
print('机器人:您好，我是聊天机器人小鱼。')
replys = input("请主人输入开始话题：")
while 1:
    info = replys
    replysa = replys
    resp = requests.get("http://api.qingyunke.com/api.php", {'key': 'free', 'appid': 0, 'msg': info})
    resp.encoding = 'utf-8'
    resp = resp.json()
    resp = re.sub("{br}", "", resp['content'])
    print('菲菲:', resp)
    speaker.Speak(resp)
    sleep(1)

    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = '4fede3c4384846b9a7d0456a5e1e2943'
    req = requests.post(api_url, data={'key': apikey, 'info': resp}).text
    replys = json.loads(req)['text']
    if replys != replysa:
        print('小鱼:', replys)
        speaker.Speak(replys)
        sleep(1)
    else:
        replys = "我们换个话题吧！"