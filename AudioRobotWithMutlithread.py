from pyaudio import PyAudio, paInt16
import wave
from aip import AipSpeech
import win32com.client
import re
import requests
import pythoncom, pyHook
import threading

#-----------------------------------------------------------------------------------------------------------
#线程函数
#-----------------------------------------------------------------------------------------------------------
global KeyPressFlag
KeyPressFlag = False
def thread_job():
    global KeyPressFlag

    # -----------------------------------------------------------------------------------------------------------
    # 监测键盘进程
    # -----------------------------------------------------------------------------------------------------------
    def OnKeyboardEvent(event):
        # print('Key:', event.Key)
        # print('KeyID:', event.KeyID)
        # print('---')
        global KeyPressFlag
        if(event.KeyID == 80):   #  p
            KeyPressFlag = not KeyPressFlag
        # 同鼠标事件监听函数的返回值
        return True

    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()

    # wait forever
    pythoncom.PumpMessages()

#添加一个线程
added_thread = threading.Thread(target=thread_job)
added_thread.start()

#-----------------------------------------------------------------------------------------------------------
#百度语音识别接口
#-----------------------------------------------------------------------------------------------------------
"""说话配置"""
speaker = win32com.client.Dispatch("SAPI.SPVOICE")

""" APPID AK SK """
APP_ID = '15074162'
API_KEY = 'D8WvOtEiT6QlbN2X0aKxd3q2'
SECRET_KEY = 'sT4H7uywGyiK1uW0vvGW9sMfZthNiThq'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
def BAIDU_ASR(_path):
    result = client.asr(get_file_content(_path), 'wav', 16000, {
        'dev_pid': 1536,
    })

    return result.get('result')[0]

#-----------------------------------------------------------------------------------------------------------
#本地录音  为wav文件
#-----------------------------------------------------------------------------------------------------------
channels = 1
sampwidth = 2
framerate = 16000
NUM_SAMPLES=32000
TIME = 1
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)#声道
    wf.setsampwidth(sampwidth)#采样字节 1 or 2
    wf.setframerate(framerate)#采样频率 8000 or 16000
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    global KeyPressFlag
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]

    print('输入p开始说话')

    while(KeyPressFlag==False):
        pass

    print('开始说话.')

    while KeyPressFlag:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)#一次性录音采样字节大小
        my_buf.append(string_audio_data)

    print('说话结束')
    save_wave_file('01.wav',my_buf)
    stream.close()

#-----------------------------------------------------------------------------------------------------------
#图灵机器人接口调用
#-----------------------------------------------------------------------------------------------------------
def chat_robot(msg):
    resp = requests.get("http://api.qingyunke.com/api.php", {'key': 'free', 'appid': 0, 'msg': msg})
    resp.encoding = 'utf-8'
    resp = resp.json()
    resp = re.sub("{br}", "", resp['content'])
    return resp


while True:
    my_record()
    audio = BAIDU_ASR('01.wav')
    print("你说的话：",audio)

    resp = chat_robot(audio)
    print("ta说的话：",resp)
    speaker.Speak(resp)
