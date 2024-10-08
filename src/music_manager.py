import yt_dlp
import asyncio
from src.path_converter import *
from src.json_controller import *

       
async def get_video(url):
    '''
    Gets the requested video as an audio file.

    Parameters
    ----------
    url : str
        The video's URL
    key: String
        The video's identifier, obtained from the URL.
    dicci: dict
        A dictionary that represents all previously downloaded files.
    TEMP_PATH: str
        Absolute path to the 'temp' directory, where the file will be saved.

    Returns
    -------
    dict
        An updated version of the dictionary that represents all downloaded files, including the latest file.
    '''    
    #ffmpeg\fmpeg.exe
    ffmpeg_abs_path= convert_to_absolute("./ffmpeg") # -> modificado
    print ("ABSOLUTE EXE PATH " + ffmpeg_abs_path)

    ydl_opts = {
        'format': 'bestaudio/best',  
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', 
            'preferredquality': '192',
            }
        ]
    }
    

    def extract_info(url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download= False)
    

    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, lambda: extract_info(url))

    print("Retornando INFO.......")
    return info


def cut_url(url, endchar): 
    '''
    Obtains an identifer for the video from its URL.

    Parameters
    ----------
    url: str
        The video's URL.
    inichar: char
        Identifier's initial delimiter.
    endchar: char 
        Identifier's end delimiter.

    Returns
    -------
    str
         The video's identifier, obtained from the URL.
    '''    
    endpos= url.find(endchar)

    if endpos != -1: 
        key= url[0 : (endpos)]
    else: 
        key= url[0 : (len(url))]

    return key
            

# video_web_url = "https://www.youtube.com/watch?v=efS8lO4nCtQ&ab_channel=juanjannon4001"
# video_app_url = "https://youtu.be/efS8lO4nCtQ?si=kBotFy7AOteH1A49"
def process_url(url):
    '''
    Processes the video's URL, based on its format, in order to obtain an identifier from it.

    Parameters
    ----------
    url: str
        The video's URL.
        
    Returns
    -------
    str
        The video's identifier, obtained from the URL.
    or
    None
        Represents the video was not found.
    '''
    
    print ("TYPE DE URL:              ____________________")
    print (type (url ))
    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://m.youtube.com/watch?v=") : #error ortografico
        key=cut_url(url, '&')
        return key
    elif url.startswith("https://youtu.be/"):
        key=cut_url(url, '?')
        return key
    else: 
        return None
    

async def get_song(url):
    '''
    Checks if the video file was already downloaded. 
    If it wasn't, then it gets downloaded and its information saved in a json file.

    Parameters
    ----------
    url : str
        The video's URL.
        
    Returns
    -------
    str
        The video's identifier, obtained from the URL.
    or
    None
        Represents the video was not found.
    '''
    key= process_url(url)
    info= None
    
    if (key is not None): 
        info= await get_video(key)
    else: 
        print ("Che no tengo URL >:(")
    
    return info