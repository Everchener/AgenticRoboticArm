# utils_vlm_move.py
# 视觉语言模型移动物体模块

print('导入VLM移动物体模块')

from utils_robot import *
from utils_vlm import *
import time


def vlm_move(PROMPT='帮我把绿色方块放在小猪佩奇上'):
    '''
    多模态大模型识别图像，吸泵吸取并移动物体
    
    参数:
        PROMPT: 给视觉大模型的指令，描述要移动的物体和目标位置
    
    工作流程:
        1. 机械臂归零
        2. 拍摄俯视图
        3. 调用视觉大模型识别物体位置
        4. 手眼标定转换为机械臂坐标
        5. 吸泵吸取并移动物体
    '''
    print('多模态大模型识别图像，吸泵吸取并移动物体')
    
    # 机械臂归零
    print('机械臂归零')
    mc.send_angles([0, 0, 0, 0, 0, 0], 50)
    time.sleep(3)
    
    # 发出指令
    print('给出的指令是:', PROMPT)
    
    # 拍摄俯视图
    print('拍摄俯视图')
    top_view_shot(check=False)
    
    # 将图片输入给多模态视觉大模型
    print('调用视觉大模型识别物体位置')
    img_path = 'temp/vl_now.jpg'
    
    n = 1
    while n < 5:
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            result = yi_vision_api(PROMPT, img_path=img_path)
            print('    多模态大模型调用成功！')
            print(result)
            break
        except Exception as e:
            print('    多模态大模型返回数据结构错误，再尝试一次', e)
            n += 1
    
    # 视觉大模型输出结果后处理和可视化
    print('视觉大模型输出结果后处理和可视化')
    START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz(result, img_path, check=True)
    
    # 手眼标定转换为机械臂坐标
    print('手眼标定，将像素坐标转换为机械臂坐标')
    START_X_MC, START_Y_MC = eye2hand(START_X_CENTER, START_Y_CENTER)
    END_X_MC, END_Y_MC = eye2hand(END_X_CENTER, END_Y_CENTER)
    print(f"起点机械臂坐标: X={START_X_MC}, Y={START_Y_MC}")
    print(f"终点机械臂坐标: X={END_X_MC}, Y={END_Y_MC}")
    
    # 吸泵吸取移动物体
    print('吸泵吸取移动物体')
    pump_move(mc, XY_START=[START_X_MC, START_Y_MC], XY_END=[END_X_MC, END_Y_MC])
    
    # 收尾
    print('任务完成')
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 测试代码
    vlm_move('帮我把红色方块放在小猪佩奇上')
