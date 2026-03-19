# utils_asr.py
# 录音模块

print('导入录音模块')

import pyaudio
import wave
from tqdm import tqdm


def record(RECORD_SECONDS=7, OUTPUT_FILENAME="temp/speech_record.wav"):
    '''
    录音功能
    
    参数:
        RECORD_SECONDS: 录音时长（秒）
        OUTPUT_FILENAME: 输出文件名
    
    返回:
        录音文件保存路径
    '''
    print('开始录音...')
    
    # 定义录音参数
    FORMAT = pyaudio.paInt16  # 16位深
    CHANNELS = 1              # 单声道
    RATE = 16000              # 采样率
    CHUNK = 1024              # 每个缓冲区的帧数

    # 初始化 PyAudio
    audio = pyaudio.PyAudio()

    # 打开流
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    input("准备好请按回车开始录音")
    print("开始录音...")

    frames = []

    # 录制音频数据
    for _ in tqdm(range(0, int(RATE / CHUNK * RECORD_SECONDS)), desc="录音进度"):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束")

    # 停止并关闭流
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 确保目录存在
    import os
    os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)

    # 保存录音文件
    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(f"音频已保存为 {OUTPUT_FILENAME}")
    return OUTPUT_FILENAME


if __name__ == "__main__":
    record()
