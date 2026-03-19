# **多模态AI Agent驱动的语音控制智能机械臂系统**

一个基于**多模态AI Agent驱动的语音控制智能机械臂系统**项目，可以听懂人类指令并编排执行相应的机械臂动作。

视频演示：百度网盘
链接: https://pan.baidu.com/s/1Z3BkQe7FZhw8c4kjpri6yQ?pwd=es2b 提取码: es2b

## 功能特性

- 🤖 **机械臂控制**: 归零、移动、跳舞、点头、摇头等动作
- 👁️ **视觉识别**: 利用视觉大模型识别物体位置
- 🗣️ **语音控制**: 支持语音输入指令
- 💡 **智能编排**: LLM智能体理解自然语言并编排动作
- 💻 **拖动示教**: 支持拖动机械臂示教并复现动作

## 硬件要求

- 机械臂
- USB摄像头
- 麦克风（电脑自带的就可以）

## 软件依赖

### Python包

```
pip install -r requirements.txt
```

### API密钥配置

使用前需要配置以下API服务：

1. **百度千帆LLM** (用于智能体动作编排)
   - 访问 https://cloud.baidu.com/
   - 创建应用获取 Access Key 和 Secret Key
   - 修改 `utils_llm.py` 中的配置

2. **零一万物 Yi-Vision** (用于视觉识别)
   - 访问 https://platform.lingyiwanwu.com/
   - 获取 API Key
   - 修改 `utils_vlm.py` 中的配置

3. **讯飞语音识别** (可选，用于语音输入)
   - 访问 https://www.xfyun.cn/
   - 创建应用获取 APPID、APIKey、APISecret
   - 修改 `utils_xf_asr.py` 中的配置

## 使用方法

### 运行主程序

```bash
python agent_go.py
```

程序会提示选择输入方式：
- `r`: 从网络接收语音指令
- `k`: 键盘输入指令
- `c`: 使用默认指令

### 机械臂内置函数

| 函数名 | 功能说明 |
|--------|----------|
| `back_zero()` | 机械臂归零 |
| `relax_arms()` | 放松机械臂 |
| `head_shake()` | 摇头动作 |
| `head_nod()` | 点头动作 |
| `head_dance()` | 跳舞动作 |
| `move_to_coords(X, Y)` | 移动到指定坐标 |
| `single_joint_move(joint, angle)` | 单关节旋转 |
| `move_to_top_view()` | 移动至俯视姿态 |
| `top_view_shot()` | 拍摄俯视图 |
| `check_camera()` | 开启摄像头 |
| `llm_led(color)` | 控制LED灯颜色 |
| `vlm_move(prompt)` | 视觉识别并移动物体 |
| `drag_teach()` | 拖动示教 |

## 项目结构

```
mycobot_agent/
├── agent_go.py              # 主入口程序
├── utils_agent.py           # 智能体动作编排
├── utils_robot.py           # 机械臂控制
├── utils_vlm.py             # 视觉大模型API
├── utils_vlm_move.py        # 视觉移动物体
├── utils_camera.py          # 摄像头
├── utils_led.py             # LED灯控制
├── utils_llm.py             # LLM大模型API
├── utils_asr.py             # 录音模块
├── utils_xf_asr.py          # 讯飞语音识别
├── utils_drag_teaching.py   # 拖动示教
└── README.md                # 说明文档
```

## 注意事项

1. **手眼标定**: 使用前需要进行手眼标定，修改 `utils_robot.py` 中的标定参数
2. **API配额**: 大模型API有调用配额限制，请注意使用
3. **安全操作**: 运行前确保机械臂周围无障碍物

## 常见问题

### Q: 运行报错 "No module named 'pymycobot'"
A: 需要安装机械臂控制库，请确保在树莓派上运行：
```bash
pip install pymycobot
```

### Q: 视觉识别失败
A: 检查API Key是否正确配置，以及网络连接是否正常

## License

MIT License
