

def get_help_message() -> str:
    '''
    Returns a help message.

    Return
    ------
    str
        A help message.
    '''
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

def get_command(message_body: str) -> list:
    '''
    Interprets a command message recived from a user.

    Parameters
    ----------
    message_data: dict
        A dictionary containing the message's basic information.
    
    Returns
    -------
    list
        A list representing a potential command sent by a user.
    '''
    list = []
    if message_body.startswith("?"):
        potential_command = message_body[1:]
        print(potential_command)
        
        #Space is intentional here!
        if potential_command.startswith("play "):
            list = potential_command.split(" ")
        
        else:
            list.append(potential_command)
        
    return list

        


