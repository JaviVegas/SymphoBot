import asyncio
from discord import Client, Message, User, FFmpegPCMAudio
from src.music_manager import get_song

async def join(user: User):
    voice_client = await user.voice.channel.connect()
    return voice_client    

def play(url: str):
    loop = asyncio.get_event_loop()

    ffmpeg_options = {"options": "-vn"}

    song = get_song(url)

    player = FFmpegPCMAudio(song, **ffmpeg_options)

    return player

def pause():
    pass

def stop():
    pass