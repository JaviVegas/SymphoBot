import src.music_manager as music_manager
#pedir cancion verificar que la playlist no este vacia
#pedir lista de cancion 

def get_next_song(playlist):
    try:
        return playlist.next_song()
    
    except IndexError:
        return None
    

def add_to_playlist(url, playlist):
    song_info= music_manager.get_song(url)

    print(f"\n\n{song_info}\n\n")
    
    added = False
    if song_info is not None:

        # NO ANDA EL GET :( CUANDO SE HACE EL ?ADD <URL>.
        title = song_info.get('title', None)
        uploader = song_info.get('uploader', None)
        
        playlist.add_song({'URL': url,
                        'Title': title,
                        'Uploader': uploader
                        })
        
        added = True
    
    return playlist, added
    

def show_song_list(playlist):
    song_list = playlist.get_song_list()
    print(song_list)

    if song_list != "":
        return song_list
    
    else:
        return "The playlist is empty!"