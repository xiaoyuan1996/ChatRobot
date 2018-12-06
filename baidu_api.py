from aip import AipSpeech
import win32com.client

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

ans = BAIDU_ASR('16k.wav')
print(ans)
speaker.Speak(ans)