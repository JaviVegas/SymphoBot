import src.Playlist
import src.music_manager as music
#pedir cancion verificar que la playlist no este vacia
#pedir lista de cancion 

def getNextSong(playlist):
    try:
        return playlist.nextSong()
    except IndexError:
        return None

def addToPlaylist(url, playlist):
    info= music.get_song()
    title = info.get('title', 'Desconocido')
    uploader = info.get('uploader', 'Desconocido')
    
    playlist.addSong((url,uploader, title))
    return playlist
    
