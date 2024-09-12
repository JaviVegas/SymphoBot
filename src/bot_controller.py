import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
from discord import Intents, Client, Message, Status, Game, Object, User, ClientUser

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
    return Client(bot_intents)


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
        print(f"{client.user} is now running!")
        
        game = Game("some tunes!")
        await Client.change_presence(status= Status.online,
                                     activity= game)

    @client.event
    async def on_message(message: Message) -> None:
        if is_bot_message(message.author, client.user):
            return

        print(f"I can read you {message.author} :)")

        channel: str = str(message.channel)
        username: str = str(message.author)
        user_message: str = message.content        

        print(f"[{channel}] {username}: '{user_message}'")
        
        # CALL RESPONSE MANAGER HERE.