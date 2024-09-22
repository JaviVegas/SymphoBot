from discord import Message, VoiceClient, FFmpegOpusAudio
from src.music_manager import get_song
from src.path_converter import convert_to_absolute
from src.playlist_manager import DICCI, add_to_playlist
import asyncio

  
async def join(message: Message) -> VoiceClient: 
    if message.author.voice and message.author.voice.channel:
        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()
        print (" EL USUARIO ESTA EN UN CANAL DE VOZ ")
        print (voice_channel.name)
        return voice_client
    else:
        print ( "UUSUARIO NO ESTA EN EL CANAL DE VOZ")
        raise Exception("El usuario no está en un canal de voz")

async def play(url: str):
    player = None
    song =  await get_song(url)
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    print("Guau-")
    if (song is not None):
        print("Miau-")
        duration = song.get('duration')  # 'duration' ya viene en segundos desde yt-dlp
        player = FFmpegOpusAudio(song['url'], **ffmpeg_options)

    print("Cuak-")
    return player, duration

def pause():
    pass

def stop():
    pass

def add(url: str):
    pass




##FUNCIONES PARA MANEJAR LA PLAYLIST 

async def playlist_play(message, voice_clients, server, voice_channel, client):
    '''
    Reproduce la playlist desde la primera canción.
    '''
    queue = DICCI[server][voice_channel]["Queue"]
    if not queue:
        return await message.channel.send("The playlist is empty")

    
    if message.guild.id not in voice_clients or not voice_clients[message.guild.id].is_connected():
        try:
            vc = await message.author.voice.channel.connect()
            voice_clients[message.guild.id] = vc
        except Exception as e:
            return await message.channel.send("Could not connect to the voice channel.")

    if not voice_clients[message.guild.id].is_playing(): 
        url = queue.popleft()
        player, duration = await play(url)
        if player: 
            
            voice_clients[message.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(
                play_next_in_queue(voice_clients[message.guild.id], server, voice_channel, client), client.loop))

            DICCI[server][voice_channel]['Last-Played'] = url
            await message.channel.send(f"Now playing: {url}")
    else: 
        await message.channel.send("Se está reproduciendo otra cosa flaco.")

async def play_next_in_queue(voice_client, server, voice_channel, client):
    '''
    Reproduce la siguiente canción en la cola, si hay más.
    '''
    queue = DICCI[server][voice_channel]["Queue"]
    
    # si no esta vacia
    if queue:
        next_url = queue.popleft()
        player, duration = await play(next_url)

        
        if player:
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(
                play_next_in_queue(voice_client, server, voice_channel, client), client.loop))
            await message.channel.send(f"Now playing: {url}")# MODIFICAR ESTA LINEA Y PONERLA EN EL BOT CONTROLLER !!!!
            DICCI[server][voice_channel]["Last-Played"] = next_url
    else:
        print("La cola está vacía, no hay más canciones para reproducir.")


    # Reproducir la primera canción
    #url = queue[0]
    #player, duration = await play(url)
    #voice_clients[message.guild.id].play(player)

    # Guardar la última reproducida
    #DICCI[server][voice_channel]["Last-Played"] = url
    #await message.channel.send(f"Now playing : {url}")

    # 30 segundos antes de que termine la canción, enviar mensaje de la siguiente canción

   # await send_next_song_message(voice_clients[message.guild.id], queue, message, server, voice_channel, duration)
async def playlist_resume(message, voice_clients, server, voice_channel):
    '''
    '''
    if voice_clients[message.guild.id].is_paused():
        voice_clients[message.guild.id].resume()
        await message.channel.send("Resuming the song...")
    else:
        await message.channel.send("There are no songs paused at the moment :thinking_face:")


async def playlist_pause(message, voice_clients):
    '''
    '''
    if voice_clients[message.guild.id].is_playing():
        voice_clients[message.guild.id].pause()
        await message.channel.send("Song paused")
    else:
        await message.channel.send("No song is playing!")

async def playlist_clear(message, server, voice_channel):
    '''limpio toda la playlist
    '''
    
    if server not in DICCI or voice_channel not in DICCI[server]:
        return await message.channel.send("Sorry, there is no playlist available for this channel :frowning_face:")
    
    DICCI[server][voice_channel]["Queue"].clear()
    await message.channel.send("The playlist has been deleted")

async def playlist_list(message, server, voice_channel):
    '''lista todas las canciones de la playlist
    '''
    if server not in DICCI or voice_channel not in DICCI[server]:
        return await message.channel.send("Sorry, there is no playlist available for this channel :frowning_face:")
    
    queue = DICCI[server][voice_channel]["Queue"]
    if not queue:
        return await message.channel.send("The playlist is empty")

    song_list = "\n".join(queue)
    await message.channel.send(f"Song list:\n{song_list}")


async def send_next_song_message(voice_client, queue, message, server, voice_channel, current_song_duration):
    next_song = queue[1] if len(queue) > 1 else None
    
    if next_song:
        await asyncio.sleep(current_song_duration - 30)
        await message.channel.send(f"LNext song: {next_song}")
    else:
        await message.channel.send("no songs left .")
