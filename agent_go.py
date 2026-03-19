# agent_go.py
# 语音控制智能体 - 主入口程序

# 导入常用函数
from utils_asr import *             # 录音+语音识别
from utils_robot import *           # 连接机械臂
from utils_llm import *             # 大语言模型API
from utils_led import *             # 控制LED灯颜色
from utils_camera import *          # 摄像头
from utils_robot import *           # 机械臂运动
from utils_vlm_move import *        # 多模态大模型识别图像，吸泵吸取并移动物体
from utils_drag_teaching import *   # 拖动示教
from utils_agent import *           # 智能体Agent编排
from utils_xf_asr import *          # 讯飞语音识别

import socket

def agent_play():
    '''
    主函数，语音控制机械臂智能体编排动作
    '''
    # 归零
    # back_zero()
    
    # 输入指令方式选择
    start_record_ok = input('是否开启录音，按r开始从主机接收录音，按k打字输入，按c输入默认指令: ')
    
    if start_record_ok == 'r':
        # 创建socket对象（用于接收树莓派客户端的语音指令）
        socket_server = socket.socket()
        # 绑定ip和端口
        socket_server.bind(("10.42.0.1", 8888))
        socket_server.listen(1)
        print("服务端已开始监听，正在等待客户端连接...")
        conn, address = socket_server.accept()
        print(f"接收到了客户端的连接，客户端的信息：{address}")
        conn.send("已接收".encode("UTF-8"))
        order = conn.recv(1024).decode("UTF-8")
        conn.close()
        socket_server.close()
    elif start_record_ok == 'k':
        order = input('请输入指令: ')
    elif start_record_ok == 'c':
        order = '先归零，再摇头，然后把绿色方块放在篮球上'
    else:
        print("无效输入，程序退出")
        return
    
    # 智能体Agent编排动作
    agent_plan_output = agent_plan(order)
    
    print('智能体编排动作如下\n', agent_plan_output)
    plan_ok = input('是否继续？按c继续，按q退出: ')
    
    if plan_ok == 'c':
        for each in agent_plan_output['function']:
            print('开始执行动作:', each)
            eval(each)
    elif plan_ok == 'q':
        exit()

if __name__ == '__main__':
    agent_play()
