import yt_dlp
# import re
import asyncio
from src.path_converter import *
from src.json_controller import *


# def extract_info_from_description(description):
#     ##REVISAR SI DEJAMOS ESTA FUNCION O NO 
#     match = re.search(r'(?P<artist>.+?)\s*-\s*(?P<title>.+)', description)
#     if match:
#         return match.group('title').strip(), match.group('artist').strip()
#     return 'Desconocido', 'Desconocido'

       
async def get_audio(url):
    '''
    Gets the requested video's audio.

    Parameters
    ----------
    url : str
        The video's URL
    
    Returns
    -------
    dict
        An updated version of the dictionary that represents all downloaded files, including the latest file.
    '''    
    #ffmpeg\fmpeg.exe
    ffmpeg_abs_path= convert_to_absolute("./ffmpeg") # -> modificado
    print ("ABSOLUTE EXE PATH " + ffmpeg_abs_path)
    name='%(title)s.%(ext)s'; 

    print ('im here in get video')
    ydl_opts = {
        'format': 'bestaudio/best',  
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', 
            'preferredquality': '192',
            }
        ],
       # 'ffmpeg_location': ffmpeg_abs_path # -> modificado
       # 'ffmpeg_location': convert_to_absolute('ffmpeg') # AGREGE LA VARIABLE AL PATH 
    }
    
    loop = asyncio.get_event_loop()
    def extract_info(url):
        print("aasddddddd")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download= False)
    
    info = await loop.run_in_executor(None, lambda: extract_info(url))
    #with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #loop = asyncio.get_event_loop()
        #info = loop.run_in_excecutor(None, lambda: ydl.extract_info(url, download=False))-> error ortografico
        #info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
        #info = ydl.extract_info(url, download=False)

    print("Retornando INFO.......")
    return info


def write_history(info, dicci, key) -> dict:
    '''
    Updates the song history.

    Parameters
    ----------
    info: dict
        An updated version of the dictionary that represents all downloaded files, including the latest file.
    dicci: dict
        The current content of the song history.
    key: str
        The video's identifier, obtained from the URL.

    Returns
    -------
    dict
        The updated song history.
    '''
    title = info.get('title', 'Desconocido')
    uploader = info.get('uploader', 'Desconocido')
    dicci[key]={'Title': title,
                'Artist': uploader, 
                'Listens': 1
                }
    return dicci


def cut_url(url, inichar, endchar) -> str: 
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
    
    print ("TYPE DE URL:              ____________________")
    print (type (url ))
    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://m.youtube.com/watch?v=") : #error ortografico
        key=cut_url(url, '=', '&')
        return key
    
    elif url.startswith("https://youtu.be/"):
        key=cut_url(url, '/', '?')
        return key
    
    else: 
        return None
    

async def get_song(url):
    '''
    Obtains the audio of a video from its URL.

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
    json_path=convert_to_absolute('data/history.json')
    new_dicci={}
    info= None

    try: 
        dicci = read_json(json_path)
        
        if (key is not None): 
            info=await get_audio(url)
            if  (key not in dicci):  
                new_dicci=write_history(info, dicci, key)
            else: 
                new_dicci= dicci
                new_dicci[key]['Listens'] =+ 1
            write_json(json_path, new_dicci)
        else: 
            print ("Che no tengo URL >:(")

    except FileNotFoundError: 
        if key is not None: 
            info= await get_audio(url)
            new_dicci=write_history(info, new_dicci, key)
            write_json(json_path, new_dicci)
    
    return info