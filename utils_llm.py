# utils_llm.py
# 大语言模型API模块

print('导入大模型API模块')

import os
import qianfan


def llm_qianfan(PROMPT='你好，你是谁？', 
                QIANFAN_ACCESS_KEY='YOUR_ACCESS_KEY', 
                QIANFAN_SECRET_KEY='YOUR_SECRET_KEY'):
    '''
    百度智能云千帆大模型平台API
    
    使用方法：
    1. 访问 https://cloud.baidu.com/
    2. 注册/登录百度智能云
    3. 进入千帆大模型平台，创建应用获取API Key和Secret Key
    4. 修改本文件中的 QIANFAN_ACCESS_KEY 和 QIANFAN_SECRET_KEY
    
    参数:
        PROMPT: 输入给大模型的提示词
        QIANFAN_ACCESS_KEY: 百度千帆平台的Access Key
        QIANFAN_SECRET_KEY: 百度千帆平台的Secret Key
    
    返回:
        大模型的回复文本
    '''
    
    # 传入 ACCESS_KEY 和 SECRET_KEY
    os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_ACCESS_KEY
    os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_SECRET_KEY
    
    # 选择大语言模型
    # MODEL = "ERNIE-Speed-128K"
    # MODEL = "ERNIE-Speed-8K"
    MODEL = "ERNIE-Lite-8K-0922"
    # MODEL = "ERNIE Speed"
    # MODEL = "ERNIE-Lite-8K"
    # MODEL = 'ERNIE-Tiny-8K'

    chat_comp = qianfan.ChatCompletion()
    
    # 输入给大模型
    resp = chat_comp.do(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}], 
    )
    
    response = resp["result"]
    return response


if __name__ == "__main__":
    # 测试代码
    response = llm_qianfan("你好，请介绍一下你自己")
    print("大模型回复:", response)
