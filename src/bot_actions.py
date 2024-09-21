from discord import Client, Message, User, VoiceClient, FFmpegOpusAudio
from src.music_manager import get_song
from src.path_converter import convert_to_absolute

#async def join(user: User):
  #  voice_client = await user.voice.channel.connect() <- anterior
  #  return voice_client    
async def join(message: Message) -> VoiceClient: 
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
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    print("Guau-")
    if (song is not None):
        print("Miau-")
        player = FFmpegOpusAudio(song['url'], **ffmpeg_options)

    print("Cuak-")
    return player

def pause():
    pass

def stop():
    pass