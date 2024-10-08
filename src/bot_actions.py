from discord import Message, VoiceClient, FFmpegOpusAudio
from src.music_manager import get_song
from src.path_converter import convert_to_absolute

  
async def join(message: Message) -> VoiceClient: 
    if message.author.voice and message.author.voice.channel:
        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()
        return voice_client
    else:
        print ( "USUARIO NO ESTA EN EL CANAL DE VOZ")
        raise Exception("El usuario no está en un canal de voz")

async def play(url: str):
    player = None
    song =  await get_song(url)
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    print("Guau-")
    if (song is not None):
        print("Miau-")
        player = FFmpegOpusAudio(song['url'], **ffmpeg_options)

    print("Cuak-")
    return player