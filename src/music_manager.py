import yt_dlp
import re
import asyncio
from path_converter import *
from src.json_controller import *

def extract_info_from_description(description):
    ##REVISAR SI DEJAMOS ESTA FUNCION O NO 
    match = re.search(r'(?P<artist>.+?)\s*-\s*(?P<title>.+)', description)
    if match:
        return match.group('title').strip(), match.group('artist').strip()
    return 'Desconocido', 'Desconocido'

       
    
#solo descargo el audio
async def get_video(url, key, dicci):
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
    absolute_exe_path= convert_to_absolute("ffmpeg/ffmpeg.exe")
    name='%(title)s.%(ext)s'; 

    
    ydl_opts = {
        'format': 'bestaudio/best',  
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', 
            'preferredquality': '192',
        }],

        'ffmpeg_location': rf'{absolute_exe_path}'
    }
   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        loop = asyncio.get_event_loop()
        info = loop.run_in_excecutor(None, lambda: ydl.extract_info(url, download=False))
        #info = ydl.extract_info(url, download=False)

    
    return info
#[{url:{titulo: blala, 
#     artista: blabla
#     ruta: blabla}, 
#{}
#]

def write_history(info, dicci, key):
    title = info.get('title', 'Desconocido')
    uploader = info.get('uploader', 'Desconocido')
    dicci[key]={'Title': title,
                'Artist': uploader, 
                'Listens': 1
                }
    return dicci


def cut_url(url, inichar, endchar): 
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
    initialpos = url.find(inichar)
    print(initialpos)
    endpos=url.find(endchar)
    print(initialpos)
    if endpos != -1: 
        key= url[(initialpos+1) : (endpos -1)]
    else: 
        key= url[(initialpos+1) : (len(url))]  
    return key
            
            
            
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
    if url.starswith("https://www.youtube.com/watch?v=") or url.startswith("https://m.youtube.com/watch?v=") : 
        key=cut_url(url, '=', '&')
        return key
    elif url.starswith("https://youtu.be/"):
        key=cut_url(url, '/', '?')
        return key
    else: 
        return None
    

def get_song(url):
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
    #temp_path= convert_to_absolute('temp')
    key= process_url(url)
    json_path=convert_to_absolute('data/history.json')
    new_dicci={}
    info= None
    try: 
        dicci = read_json(json_path)
        
        if (key is not None): 
            info=get_video(url, key, dicci)
            if  (key not in dicci):  
                new_dicci=write_history(info, dicci, key)
            else: 
                new_dicci= dicci
                new_dicci[key]['Listens']+=1
            write_json(json_path, new_dicci)
        else: 
            print (" che no tengo url")
    except FileNotFoundError: 
        if key is not None: 
            info=get_video(url, key)
            new_dicci=write_history(info, dicci, key)
            write_json(json_path, new_dicci)
    
    return info
         
        
        
        

# video_web_url = "https://www.youtube.com/watch?v=efS8lO4nCtQ&ab_channel=juanjannon4001"
# video_app_url="https://youtu.be/efS8lO4nCtQ?si=kBotFy7AOteH1A49"

# get_song(video_web_url)
# print ("todo ok")
