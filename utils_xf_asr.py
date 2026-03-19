# utils_xf_asr.py
# 讯飞语音识别模块
# 基于讯飞开放平台WebAPI的语音识别功能

print('导入讯飞语音识别模块')

import _thread as thread
import time
from time import mktime
import websocket
import base64
import datetime
import hashlib
import json
import ssl
from datetime import datetime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

# 状态标识
STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    '''
    讯飞WebAPI连接参数类
    '''
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile
        self.iat_params = {
            "domain": "slm", 
            "language": "zh_cn", 
            "accent": "mandarin",
            "dwa": "wpgs", 
            "result": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain"
            }
        }

    def create_url(self):
        '''生成鉴权的WebSocket URL'''
        url = 'ws://iat.xf-yun.com/v1'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + "iat.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v1 " + "HTTP/1.1"
        
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'), 
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat.xf-yun.com"
        }
        url = url + '?' + urlencode(v)
        return url


# 默认配置（需要用户修改）
DEFAULT_APPID = 'YOUR_APPID'
DEFAULT_APIKEY = 'YOUR_APIKEY'
DEFAULT_APISECRET = 'YOUR_APISECRET'


# 收到websocket消息的处理
def on_message(ws, message):
    message = json.loads(message)
    code = message["header"]["code"]
    status = message["header"]["status"]
    re_sentence = ''
    
    if code != 0:
        print(f"请求错误：{code}")
        ws.close()
    else:
        payload = message.get("payload")
        if payload:
            text = payload["result"]["text"]
            text = json.loads(str(base64.b64decode(text), "utf8"))
            text_ws = text['ws']
            result = ''
            for i in text_ws:
                for j in i["cw"]:
                    w = j["w"]
                    result += w
            re_sentence = result
        if status == 2:
            ws.close()
    
    if re_sentence != '。':
        with open('temp/text_xf.txt', "w", encoding='utf-8') as f:
            f.write(re_sentence)


def on_error(ws, error):
    print("### error:", error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        frameSize = 1280  # 每一帧的音频大小
        intervel = 0.04  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME
        
        try:
            with open(wsParam.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    audio = str(base64.b64encode(buf), 'utf-8')

                    if not buf:
                        status = STATUS_LAST_FRAME
                    
                    if status == STATUS_FIRST_FRAME:
                        d = {
                            "header": {"status": 0, "app_id": wsParam.APPID},
                            "parameter": {"iat": wsParam.iat_params},
                            "payload": {"audio": {"audio": audio, "sample_rate": 16000, "encoding": "raw"}}
                        }
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {
                            "header": {"status": 1, "app_id": wsParam.APPID},
                            "parameter": {"iat": wsParam.iat_params},
                            "payload": {"audio": {"audio": audio, "sample_rate": 16000, "encoding": "raw"}}
                        }
                        ws.send(json.dumps(d))
                    elif status == STATUS_LAST_FRAME:
                        d = {
                            "header": {"status": 2, "app_id": wsParam.APPID},
                            "parameter": {"iat": wsParam.iat_params},
                            "payload": {"audio": {"audio": audio, "sample_rate": 16000, "encoding": "raw"}}
                        }
                        ws.send(json.dumps(d))
                        break

                    time.sleep(intervel)
        except:
            print("识别已完成，链接已关闭")

    thread.start_new_thread(run, ())


# 全局变量
wsParam = None


def init_xf_asr(APPID=None, APIKey=None, APISecret=None, AudioFile="temp/speech_record.wav"):
    '''
    初始化讯飞语音识别配置
    
    参数:
        APPID: 讯飞应用ID
        APIKey: 讯飞API Key
        APISecret: 讯飞API Secret
        AudioFile: 录音文件路径
    
    获取方式:
        1. 访问 https://www.xfyun.cn/
        2. 注册/登录讯飞开放平台
        3. 创建应用获取APPID、APIKey、APISecret
    '''
    global wsParam
    wsParam = Ws_Param(
        APPID=APPID or DEFAULT_APPID,
        APIKey=APIKey or DEFAULT_APIKEY,
        APISecret=APISecret or DEFAULT_APISECRET,
        AudioFile=AudioFile
    )


def speech_recognition_xf(AudioFile="temp/speech_record.wav"):
    '''
    讯飞语音识别函数
    
    参数:
        AudioFile: 要识别的音频文件路径
    
    返回:
        识别结果文本
    '''
    global wsParam
    
    if wsParam is None:
        init_xf_asr(AudioFile=AudioFile)
    else:
        wsParam.AudioFile = AudioFile
    
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(
        wsUrl, 
        on_message=on_message, 
        on_error=on_error, 
        on_close=on_close, 
        on_open=on_open
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    
    re_sentence = ''
    with open('temp/text_xf.txt', 'r', encoding='utf-8') as f:
        re_sentence = f.readline()
    
    print("识别结果:", re_sentence)
    return re_sentence


if __name__ == "__main__":
    # 测试代码
    print("请确保录音文件 temp/speech_record.wav 存在")
    result = speech_recognition_xf()
    print("识别结果:", result)
