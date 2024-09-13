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
def download_song(url,key, TEMP_PATH):
    '''
    downloads the requested song

    Parameters
    ----------
    url : String
        The video/playlist url
    key: String
        The song identifier
    TEMP_PATH: String
        Absolute path to the 'temp' directory
    Returns
    -------
    string
        
    '''    
    #ffmpeg\fmpeg.exe
    absolute_exe_path= convert_to_absolute("ffmpeg/ffmpeg.exe")
    name='%(title)s.%(ext)s'; 
    path_name=convert_to_absolute(TEMP_PATH+"/"+name)
    
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
   
    dicci={}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Desconocido')
        uploader = info.get('uploader', 'Desconocido')
        
      
        dicci[key]={'Title':title,
                    'Artist': uploader,
                    'Relative-Path':convert_to_relative(path_name)}
    return dicci
#[{url:{titulo: blala, 
#     artista: blabla
#     ruta: blabla}, 
#{}
#]

def cut_url(url,inichar,endchar): 
    '''
    obtains the url identifier

    Parameters
    ----------
    url : String
        The video/playlist url
    inichar: char
        initial identifier delimiter
    endchar: char 
        end delimiter of the identifier
    Returns
    -------
    string
        
    '''    
    initialpos = url.find(inichar)
    print(initialpos)
    endpos=url.find(endchar)
    print(initialpos)
    if endpos != -1: 
        key= url[(initialpos+1): (endpos -1)]
    else: 
        key= url[(initialpos+1): (len(url))]  
    return key
            
            
            
def process_url(url):
    '''
    process url

    Parameters
    ----------
    url : String
        The video/playlist url
        
    Returns
    -------
    string/None
        
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
    tries to open the json file and checks for the existence of the song. 
    If it does not exist, it downloads it and saves its data. 

    Parameters
    ----------
    url : String
        The video/playlist url
        
    Returns
    -------
    string
        
    '''
    TEMP_PATH= convert_to_absolute('temp')
    key= process_url
    json_path=convert_to_absolute('data/history.json')
    try: 
        read_json(json_path)
        if (key is not None) and (key not in dicci): 
  
            dicci=download_song(url, key,TEMP_PATH)
            write_json(json_path, dicci)
        elif key is not None:
            #busco la cancion en dicci y la reproduczo PARA IMPLEMENTAR
            pass
    except FileNotFoundError: 
        if key is not None: 
            dicci=download_song(url, key,TEMP_PATH)
            write_json(json_path, dicci)
    return key
         
        
        
        

video_web_url = "https://www.youtube.com/watch?v=efS8lO4nCtQ&ab_channel=juanjannon4001"
video_app_url="https://youtu.be/efS8lO4nCtQ?si=kBotFy7AOteH1A49"

get_song(video_web_url)
print ("todo ok")
