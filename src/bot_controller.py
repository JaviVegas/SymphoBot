import os
import yt_dlp
from dotenv import load_dotenv
from discord import Intents, Client, Message, Status, Game, errors
import src.message_manager as message_manager
from src.json_controller import read_json
from src.path_converter import *
import src.bot_actions as bot_actions
import src.playlist_manager as playlist_manager
from src.Playlist import Playlist
import asyncio

def is_bot_message(message_author, this_bot):
    '''
    Checks whether the sender of the message is this bot or not.

    Parameters
    ----------
    message_author : User
        The sender of the message.

    this_bot : ClientUser
        The discord user that represents this bot.
    
    Returns
    -------
    bool
        The result of comparing the sender of the message with this bot's discord user.
    '''
    
    if message_author == this_bot:
        return True

def obtain_token():
    '''
    Gets this bot's authentication token from an existing enviromental variable (".env" file) from this program's enviroment.
    
    Returns
    -------
    str
        This bot's authentication token.
    '''
    load_dotenv()
    return os.getenv("DISCORD_TOKEN")

def get_client():
    '''
    Sets up the bot's client, allowing it to connect to the server and detect events that occur in it.

    Returns
    -------
    Client
        A client connection that connects to Discord.
    '''
    bot_intents = Intents.default()
    bot_intents.messages= True
    bot_intents.message_content = True
    bot_intents.guild_typing = True
    return Client(intents= bot_intents)


def run_bot():
    '''
    Runs this bot.
    '''
    TOKEN = obtain_token()
    client = get_client()
        
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg = {"options": "-vn"}

    playlist= Playlist()


    def get_playlist():
        return playlist


    @client.event
    async def on_ready() -> None:
        '''
        Runs only once when bot awakes.
        '''
        print(f"{client.user} is now running!")
        
        game = Game("some tunes!")
        await client.change_presence(status= Status.online,
                                     activity= game)


    @client.event
    async def on_message(message: Message) -> None:
        '''
        Runs when a message is sent on any of the server channels.
        '''
        if is_bot_message(message.author, client.user):
            return

        print(f"I can read you {message.author} :)\n")

        user_message: str = message.content
        message_data = {"Channel": str(message.channel),
                        "Username": str(message.author),
                        "Message-Body": user_message}
        
        print(f"[{message_data['Channel']}] {message_data['Username']}: '{message_data['Message-Body']}'")
        
        # CALL RESPONSE MANAGER HERE.
        command = message_manager.get_command(message_data["Message-Body"])
        print(message_data)
        print("el channel es: "+ message_data['Channel'])
        print("--------")
        print(type(command))
        print(command)
        print ("COMMAND ->"+ command[0].lower()) 
        command_list = read_json(convert_to_absolute("data/responses.json"))
        
        plist = get_playlist()

        async def join_voice_channel():
            if (voice_clients == {}) or (not voice_clients[message.guild.id].is_connected()):
                try:
                        vc = await bot_actions.join(message)
                        voice_clients[vc.guild.id] = vc

                except errors.ClientException as e:
                        print(e + "No se puede unir al canal de voz...")
            else:
                print("YA ESTAS EN UN CANAL DE VOZ LOCOOOO")

            return voice_clients
        
        
        async def play_song(url, title, uploader):
            if (voice_clients != {}):
                print("EL DICT NO ES VACIO-- HAY UN CLIENTE GUARDADO")
                
                if (voice_clients[message.guild.id].is_playing()):
                    print("STOPPING---")
                    voice_clients[message.guild.id].pause()

            try:
                player, duration= await bot_actions.play(url)
                await asyncio.sleep(duration + 5)
                if (player is not None):
                    voice_clients[message.guild.id].play(player)
                    await message.channel.send(f'{command_list[command[0].lower()]} "{title}" by {uploader}')
                
                else: 
                    await message.channel.send("Video not found!")
            
            except errors.ClientException as e:
                print(e, " - No se puede reproducir la cancion...")



        if (command != []) and (command[0].lower() in command_list):

            # Bot Main Actions.                
            
            #FUNCIONALIDAD PARA AGREGAR A LA LISTA
          
            if command[0].lower() == "add": 
           
                url = command[1]
                plist, added= playlist_manager.add_to_playlist(url, plist)
                
                if added:
                    await message.channel.send(command_list[command[0].lower()])
                else:
                    await message.channel.send(f"[!] Error. Could not add the video to the playlist...")


            elif command[0].lower() == "playnext":
                voice_clients= join_voice_channel()
                next_song = playlist_manager.get_next_song(plist)
                
                if next_song is not None:
                    play_song(next_song['URL'], next_song['Title'], next_song['Uploader'])
                else:
                    await message.channel.send("The playlist is empty! Please add at least one song before playing.")
             

            elif command[0].lower() == "pause":
                try:                    
                    voice_clients[message.guild.id].pause()
                    await message.channel.send(command_list[command[0].lower()])
                
                except Exception as e:
                    print(e)


            elif command[0].lower() == "resume":
                try:
                    voice_clients[message.guild.id].resume()
                    await message.channel.send(command_list[command[0].lower()])
                
                except Exception as e:
                    print(e)


            elif command[0].lower() == "stop":
                try:
                    voice_clients[message.guild.id].stop()
                    await voice_clients[message.guild.id].disconnect()
                    await message.channel.send(command_list[command[0].lower()])
                    
                except Exception as e:
                    print(e + " AIUDAAA NO SE PUDO PARAAAAAAAAR")
            

            elif command[0].lower() == "clear":
                plist.clear_list()
                await message.channel.send(command_list[command[0].lower()])


            elif command[0].lower() == "playlist":
                song_list = playlist_manager.show_song_list(plist)
                await message.channel.send(song_list)

        
        elif (command != []) and (command[0].lower() == "help"):
            await message.channel.send(message_manager.get_help_message())
        

    client.run(TOKEN)