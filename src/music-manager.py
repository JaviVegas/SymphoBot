import yt_dlp
import re
from src.paths import *
from src.json_controller import *

def extract_info_from_description(description):
    ##REVISAR SI DEJAMOS ESTA FUNCION O NO 
    match = re.search(r'(?P<artist>.+?)\s*-\s*(?P<title>.+)', description)
    if match:
        return match.group('title').strip(), match.group('artist').strip()
    return 'Desconocido', 'Desconocido'

       
    
#solo descargo el audio
def download_video(url, key, dicci, temp_path):
    '''
    Downloads the requested video as an audio file.

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
    path_name=convert_to_absolute(temp_path + "/" + name)
    
    ydl_opts = {
        'format': 'bestaudio/best',  
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', 
            'preferredquality': '192',
        }],

        'ffmpeg_location': rf'{absolute_exe_path}',  
        'outtmpl': path_name,   
    }
   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Desconocido')
        uploader = info.get('uploader', 'Desconocido')
        
      
        dicci[key]={'Title': title,
                    'Artist': uploader,
                    'Relative-Path': convert_to_relative(path_name)
                    }
    
    return dicci
#[{url:{titulo: blala, 
#     artista: blabla
#     ruta: blabla}, 
#{}
#]

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
    temp_path= convert_to_absolute('temp')
    key= process_url
    json_path=convert_to_absolute('data/history.json')
    try: 
        dicci = read_json(json_path)
        if (key is not None) and (key not in dicci):  
            new_dicci=download_video(url, key, dicci, temp_path)
            write_json(json_path, new_dicci)

        elif key is not None:
            # busco la cancion en dicci y la reproduczo
            # PARA IMPLEMENTAR
            pass

    except FileNotFoundError: 
        if key is not None: 
            dicci=download_video(url, key, temp_path)
            write_json(json_path, dicci)
    
    return key
         
        
        
        

# video_web_url = "https://www.youtube.com/watch?v=efS8lO4nCtQ&ab_channel=juanjannon4001"
# video_app_url="https://youtu.be/efS8lO4nCtQ?si=kBotFy7AOteH1A49"

# get_song(video_web_url)
# print ("todo ok")
