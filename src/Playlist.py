
class Playlist():
   
    def __init__(self) :
        self._song_list= []
    
    def get_list_size(self):
        return len(self._song_list)

    def clear_list(self):
        self._song_list.clear()

    def add_song(self, dicci):
        self._song_list.append(dicci)
    
    def next_song(self): 
        return self._song_list.pop(0)
    
    def get_song_list(self):
        msg=""
        num= 0
        for song in self._song_list:
            msg += f"{num:02d}. {song['Title']} - {song['Uploader']}\n"
            num += 1

        return msg
    
