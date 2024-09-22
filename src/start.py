import os
import tkinter
from tkinter import messagebox
import tkinter.messagebox
from src.path_converter import ROOT_PATH
from src.bot_controller import run_bot


def show_popup(title, message) -> None:
    '''
    Shows a popup window with a message.

    Parameters
    ----------
    title: str
        The title of the popup window.
    message: str
        The message of the popup window.
    '''
    tkinter.messagebox.showinfo(title, message)


def start_bot() -> None:
    '''
    Does an integrity of files verification before running the bot.
    '''
    responses_path = os.path.join(ROOT_PATH, 'data', 'responses.json')
    env_path = os.path.join(ROOT_PATH, '.env')
    ffmpeg_path = os.path.join(ROOT_PATH, "ffmpeg.exe")
    bot_controller_path = os.path.join(ROOT_PATH, 'src', 'bot_controller.py')

    if (os.path.isfile(responses_path)
        and os.path.isfile(env_path)
        and os.path.isfile(ffmpeg_path)
        and os.path.isfile(bot_controller_path)):
        run_bot()
    
    else:
        show_popup("Warning", "Important files are missing. Cannot start the program.")
        print(" [!] >> Important files are missing. Cannot start the program. << ")            

    