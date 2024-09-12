import yt_dlp
import re

#podriamos hacer un json y dps borrar el json
#el usuario podria acceder al historial de reproduccion antes de salir de la sesion y borrarlo
dicci={}


def extract_info_from_description(description):
  
    match = re.search(r'(?P<artist>.+?)\s*-\s*(?P<title>.+)', description)
    if match:
        return match.group('title').strip(), match.group('artist').strip()
    return 'Desconocido', 'Desconocido'

def get_song_info(url):
    ydl_opts = {
        'format': 'bestaudio/best',  
        'noplaylist': True,  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'Desconocido')
        uploader = info.get('uploader', 'Desconocido')
        description = info.get('description', '')

        # intenro buscar el artista y el titulo por la descripcion del video
        extracted_title, extracted_artist = extract_info_from_description(description)
        if extracted_title != 'Deconocido' or extracted_artist != 'Desconocido':
            return extracted_title+extracted_artist

       
        #tendiramos q chequear que no este repetido 
        # pq podria quedar una clave 'Desconocido-Desonocido' varias veces
        #en caso de que no se encuentre un artista y un titulo muchas veces
        
        return title+uploader
#solo descargo el audio
def descargar_cancion(url, TEMP_PATH):
    name='%(title)s.%(ext)s'; 
    path= TEMP_PATH+name;
    ydl_opts = {
        'format': 'bestaudio/best',  #descargo el mejor formato d audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',#ouede ser otro formato 
            'preferredquality': '192',# calidad de audio en kbps¿? no tenfgo ni idea de audio asi q dejo este numero 
        }],
    
        #JAVI MODIFICA LA RUTA CON LA RUTA DEL FMPEG.EXE
    #(donde hayas descomprimido el fmpeg.zip) PQ SINO NO FUNCA
        #*
        'ffmpeg_location': r'C:\Users\bianc\Desktop\2do Sem 2024\ffmpeg-7.0.2-full_build\bin\fmpeg.exe',  #ruta ABSOLUTA a ffmpeg.exe, deberia ser relativa pero dsp lo arreglo
        'outtmpl': path,  #formatear el nombre pa que quede bonito 
    }
   
   

# Ruta y nombre del archivo de salida
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Desconocido')#obtiene el nombre de la cancion y si no lo encuentra devulve desconocido
                                                #GUARDA CON LOS REPETIDOS 
        uploader = info.get('uploader', 'Desconocido')#obtine el artista de la cancion y si no lo encuentra devuelve desconocido
    
        dicci['tittle+info']= path




TEMP_PATH= 'blablabla'#ponele q es una ruta valida
# descargo el audio
video_url = "https://www.youtube.com/watch?v=efS8lO4nCtQ&ab_channel=juanjannon4001"


if get_song_info(video_url) not in dicci: 
    #si no esta la cancion registrada en el dicci la descargo 
    descargar_cancion(video_url)


print ("todo ok")
