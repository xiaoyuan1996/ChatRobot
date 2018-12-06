import re
import json
import requests
from time import sleep
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SPVOICE")

print('常国庆:您好，我是聊天机器人黑菲菲。')
print('袁志强:你好，我是主人。')
replys = input("黑猩猩：请主人输入开始话题：")
while 1:
    info = replys
    replysa = replys
    resp = requests.get("http://api.qingyunke.com/api.php", {'key': 'free', 'appid': 0, 'msg': info})
    resp.encoding = 'utf-8'
    resp = resp.json()
    resp = re.sub("{br}", "", resp['content'])
    print('黑猩猩:', resp)
    speaker.Speak(resp)
    sleep(1)

    replysa = resp
    req =requests.get("http://api.qingyunke.com/api.php", {'key': 'free', 'appid': 0, 'msg': resp})
    req.encoding = 'utf-8'
    req = req.json()
    replys = re.sub("{br}", "", req['content'])

    if replys != replysa:
        print('主人:', replys)
        speaker.Speak(replys)
        sleep(1)
    else:
        replys = "我们换个话题吧！"

