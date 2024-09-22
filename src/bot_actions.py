from discord import Message, VoiceClient, FFmpegOpusAudio
from src.music_manager import get_song
from src.path_converter import convert_to_absolute

  
async def join(message: Message) -> VoiceClient:
    '''
    Connects the bot to the same voice channel the user is in at that moment.

    Parameters
    ----------
    message: Message
        A message sent in any of the server's text channel.
    
    Returns
    -------
    VoiceClient
        Represents a connection with a voice channel.
    '''
    if message.author.voice and message.author.voice.channel:
        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()
        return voice_client
    else:
        raise Exception("The user is not in a voice channel!")

async def play(url: str) -> FFmpegOpusAudio:
    '''
    Gets audio from a video's URL.

    Parameters
    ----------
    url: str
        A video's URL.
    
    Returns
    -------
    FFmpegOpusAudio
        An audio source from FFmpeg.
    '''
    player = None
    song =  await get_song(url)
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    if (song is not None):
        player = FFmpegOpusAudio(song['url'], **ffmpeg_options)

    return player
