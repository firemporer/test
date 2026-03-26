from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

from playsound import playsound
import os

@register("test", "fire_empire", "一个简单的test插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("test")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    # 音频播放
    @filter.command("playaudio")
    async def play_audio(self, event: AstrMessageEvent):
        """播放本地音频文件"""
        audio_file = os.path.join(os.path.dirname(__file__), "music//audio.mp3")  # 确保音频文件放在插件目录下
        if os.path.exists(audio_file):
            try:
                playsound(audio_file)
                yield event.plain_result("音频播放完成！")
            except Exception as e:
                logger.error(f"播放音频时出错: {e}")
                yield event.plain_result("播放音频时出错，请检查日志！")
        else:
            yield event.plain_result("音频文件不存在，请检查路径！")




    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
