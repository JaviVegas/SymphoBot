import asyncio
from discord.ext import commands


def get_help_message():
    return '''-- SymphoBot Help --

Use "?" to comunicate with SymphoBot, followed by one of the next messages:

-> join:
    If you are in a voice channel, use this command to get SymphoBot in the same voice channel as you.

-> play <URL>:
    If SymphoBot is in a voice channel, use this command to start playing the audio from a YouTube URL of your choice (Non Private videos only).

-> pause:
    If SymphoBot is playing, use this command to pause the current audio.

-> stop:
    If SymphoBot is playing or pausing, use this command to stop the current audio.

Enjoy!
'''

def get_command(message_body: str) -> list[str]:
    '''
    Interprets a command message recived from a user.

    Parameters
    ----------
    message_data: dict
        A dictionary containing the message's basic information.
    
    Returns
    -------
    str
        A string representing a potential command sent by a user.
    '''
    if message_body[0] == "?":
        potential_command = message_body[1:]
        
        #Space is intentional here!
        if potential_command.startswith("play "):
            potential_command = potential_command.split(" ")
        
        else:
            potential_command = list(potential_command)

        return potential_command


