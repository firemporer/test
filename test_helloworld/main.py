from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp


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
        """发送本地音频文件到 QQ 聊天"""
        audio_file = os.path.join(os.path.dirname(__file__), "music", "audio.mp3")
        if os.path.exists(audio_file):
            try:
                await event.send_audio(audio_file)
                yield event.plain_result("音频已发送！")
            except Exception as e:
                logger.error(f"发送音频时出错: {e}")
                yield event.plain_result("发送音频时出错，请检查日志！")
        else:
            yield event.plain_result("音频文件不存在，请检查路径！")

    # 发送 WAV 音频到 QQ 聊天
    @filter.command("sendwav")
    async def send_wav_audio(self, event: AstrMessageEvent):
        """发送本地 WAV 音频文件到 QQ 聊天"""
        # 动态获取插件目录下的 WAV 音频文件路径
        path = "data/plugins/test_helloworld/music/test.wav"  # 替换为你的 WAV 音频文件路径
        try:
            # 使用 Comp.Record 函数发送音频

            chain = [
                Comp.Record(file = path),
                Comp.Plain("wav发送成功"),
            ]
            yield event.chain_result(chain)
        except Exception as e:
            logger.error(f"发送 WAV 音频时出错: {e}")
            yield event.plain_result("发送 WAV 音频时出错，请检查日志！")
        


    @filter.command("vedio")
    async def vedio(self, event: AstrMessageEvent):
        """发送视频到 QQ 聊天"""
        from astrbot.api.message_components import Video

        # 视频 URL 示例
        video_url = "data/plugins/test_helloworld/vedio/madoka.mp4"  

        try:
            # 使用 Video.fromURL 发送视频
            video = Video.fromFileSystem(path=video_url)
            yield event.chain_result([video])
            yield event.plain_result("视频已成功发送！")
        except Exception as e:
            logger.error(f"发送视频时出错: {e}")
            yield event.plain_result("发送视频时出错，请检查日志！")

    @filter.command("picture")
    async def picture(self, event: AstrMessageEvent):
        chain = [
            #Comp.At(qq=event.get_sender_id()), # At 消息发送者
            Comp.Plain("快看快看："),
            #Comp.Image.fromURL("https://example.com/image.jpg"), # 从 URL 发送图片
            Comp.Image.fromFileSystem("data/plugins/test_helloworld/picture/test.jpg"), # 从本地文件目录发送图片
        ]
        yield event.chain_result(chain)


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
