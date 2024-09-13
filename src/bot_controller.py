import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
from discord import Intents, Client, Message, Status, Game
import src.message_manager as message_manager
from src.json_controller import read_json
from src.path_converter import *
import src.bot_actions as bot_actions


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
    bot_intents.message_content = True
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


    @client.event
    async def on_ready() -> None:
        '''
        Runs only once when bot awakes.
        '''
        print(f"{client.user} is now running!")
        
        game = Game("some tunes!")
        await Client.change_presence(status= Status.online,
                                     activity= game)


    @client.event
    async def on_message(message: Message) -> None:
        '''
        Runs when a message is sent on any of the server channels.
        '''
        if is_bot_message(message.author, client.user):
            return

        print(f"I can read you {message.author} :)\n")

        message_data = {"Channel": str(message.channel),
                        "Username": str(message.author),
                        "Message-Body": message.content}

        print(f"[{message_data["Channel"]}] {message_data["Username"]}: '{message_data['Message-Body']}'")
        
        # CALL RESPONSE MANAGER HERE.
        command = message_manager.get_command(message_data["Message-Body"])

        command_list = read_json(convert_to_absolute("data/responses.json"))
        if command[0].lower() in command_list:
            
            # Bot Main Actions.

            if command[0] == "join":
                try:
                    vc = bot_actions.join(message_data["Username"])
                    voice_clients[vc.guild.id] = vc

                except Exception as e:
                    print(e)

            
            elif command[0] == "play":
                try:
                    player = bot_actions.play(command[1])
                    voice_clients[message.guild.id].play(player)

                except Exception as e:
                    print(e)


            elif command[0] == "pause":
                bot_actions.pause()


            elif command[0] == "stop":
                bot_actions.stop()


            await message_data["Channel"].send(command_list[command[0].lower()])

        elif command == "help":
            await message_data["Channel"].send(message_manager.get_help_message())
