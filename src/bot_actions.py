import asyncio
from discord import Client, Message, User, FFmpegPCMAudio
from src.music_manager import get_song

#async def join(user: User):
  #  voice_client = await user.voice.channel.connect() <- anterior
  #  return voice_client    
async def join(message: Message): 
    if message.author.voice and message.author.voice.channel:
        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()
        return voice_client
    else:
        print ( "UUSUARIO NO ESTA EN EL CANAL DE VOZ")
        raise Exception("El usuario no está en un canal de voz")

async def play(url: str):
    #loop = asyncio.get_event_loop()
    
    #aca necesitamos el info
    player = None
    song =  await get_song(url)
    ffmpeg_options = {"options": "-vn"}
    if (song is not None):
        player = FFmpegPCMAudio(song['url'], **ffmpeg_options)

    return player

def pause():
    pass

def stop():
    pass