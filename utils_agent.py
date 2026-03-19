# utils_agent.py
# 智能体Agent动作编排模块

import json
from utils_llm import *


AGENT_SYS_PROMPT = '''
你是我的机械臂助手，机械臂内置了一些函数，请你根据我的指令，以json形式输出要运行的对应函数和你给我的回复

【以下是所有内置函数介绍】
机械臂位置归零，所有关节回到原点：back_zero()
放松机械臂，所有关节都可以自由手动拖拽活动：relax_arms()
做出摇头动作：head_shake()
做出点头动作：head_nod()
做出跳舞动作：head_dance()
移动到指定XY坐标，比如移动到X坐标150，Y坐标-120：move_to_coords(X=150, Y=-120)
指定关节旋转，比如关节1旋转到60度，总共有6个关节：single_joint_move(1, 60)
移动至俯视姿态：move_to_top_view()
拍一张俯视图：top_view_shot()
开启摄像头，在屏幕上实时显示摄像头拍摄的画面：check_camera()
LED灯改变颜色，比如：llm_led('帮我把LED灯的颜色改为贝加尔湖的颜色')
将一个物体移动到另一个物体的位置上，比如：vlm_move('帮我把红色方块放在小猪佩奇上')
拖动示教，我可以拽着机械臂运动，然后机械臂模仿复现出一样的动作：drag_teach()
把指定物体用夹爪夹起来：vlm_lift("帮我把蓝色方块拿起来")
把手中的物体放到指定位置：vlm_drop("把手里的东西放到摩托车上")

【输出json格式】
你直接输出json即可，即从{开始即可，不要输出包含```json的开头或结尾
在'function'键中，输出函数名列表，列表中每个元素都是字符串，代表要运行的函数名称和参数。每个函数既可以单独运行，也可以和其他函数先后运行。列表元素的先后顺序，表示执行函数的先后顺序

【以下是一些具体的例子】
我的指令：回到原点。你输出：{'function':['back_zero()']}
我的指令：先回到原点，然后跳舞。你输出：{'function':['back_zero()', 'head_dance()']}
我的指令：先回到原点，然后移动到180, -90坐标。你输出：{'function':['back_zero()', 'move_to_coords(X=180, Y=-90)']}
我的指令：先打开吸泵，再把关节2旋转到30度。你输出：{'function':['pump_on()', single_joint_move(2, 30)]}
我的指令：移动到X为160，Y为-30的地方。你输出：{'function':['move_to_coords(X=160, Y=-30)']}
我的指令：拍一张俯视图，然后把LED灯的颜色改为黄金的颜色。你输出：{'function':['top_view_shot()', llm_led('把LED灯的颜色改为黄金的颜色')]}
我的指令：帮我把绿色方块放在小猪佩奇上面。你输出：{'function':['vlm_move(\\'帮我把绿色方块放在小猪佩奇上面\\')']}
我的指令：帮我把红色方块放在李云龙的脸上。你输出：{'function':['vlm_move(\\'帮我把红色方块放在李云龙的脸上\\')']}
我的指令：关闭吸泵，打开摄像头。你输出：{'function':['pump_off()', 'check_camera()']}
我的指令：先归零，再把LED灯的颜色改为墨绿色。你输出：{'function':['back_zero()', llm_led(\\'把LED灯的颜色改为墨绿色\\')]}
我的指令：我拽着你运动，然后你模仿复现出这个运动。你输出：{'function':['drag_teach()']}
我的指令：开启拖动示教。你输出：{'function':['drag_teach()']}
我的指令：先回到原点，再把LED灯的颜色改成中国红，最后把绿色方块移动到摩托车上。你输出：{'function':['back_zero()', llm_led(\\'把LED灯的颜色改为中国红色\\'), vlm_move(\\'把绿色方块移动到摩托车上\\')]}

【不要输出话语之外的动作】

【保证每一个引号都是合上的,即每个"都有一个"配对，请在输出的时候进行检查】

【我现在的指令是】
'''


def agent_plan(AGENT_PROMPT='点个头跳支舞，把绿色的橡皮放到小猪佩奇上'):
    '''
    智能体动作编排函数
    
    参数:
        AGENT_PROMPT: 用户给定的自然语言指令
    
    返回:
        包含动作函数列表的字典，格式: {'function': ['函数1()', '函数2()', ...]}
    '''
    print('Agent智能体编排动作')
    
    # 组合请求话语
    PROMPT = AGENT_SYS_PROMPT + AGENT_PROMPT
    
    # 调用LLM获取动作编排
    agent_plan = llm_qianfan(PROMPT)
    
    # 去除开头和结尾的杂质
    agent_plan = agent_plan[7:-3]
    print(agent_plan)
    
    agent_plan = json.loads(agent_plan)
    print(agent_plan)
    return agent_plan


if __name__ == "__main__":
    # 测试代码
    result = agent_plan('先归零，再跳舞')
    print("编排结果:", result)
