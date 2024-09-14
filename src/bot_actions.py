import asyncio
from discord import Client, Message, User, FFmpegPCMAudio
from src.music_manager import get_song

async def join(user: User):
    voice_client = await user.voice.channel.connect()
    return voice_client    

def play(url: str):
    #loop = asyncio.get_event_loop()
    
    #aca necesitamos el info
    player = None
    song = get_song(url)
    ffmpeg_options = {"options": "-vn"}
    if (song is not None):
        player = FFmpegPCMAudio(song['url'], **ffmpeg_options)

    return player

def pause():
    pass

def stop():
    pass