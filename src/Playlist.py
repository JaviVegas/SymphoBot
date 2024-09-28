
#[
#    {url: {
    #       Artistaartista, cancion)},  
#]
class Playlist():
   
    def __init__(self) :
        self._songList=[]
        
    def clearList(self):
        self._songList.clear()

    def addSong(self, dicci):
        self._songList.append(dicci)
    
    def nextSong(self): 
        return self._songList.pop(0)
    
    def listSong(self):
        msg=""
        for song in self._songList:
            print ()
            msg += f"\n {song[1]} - {song[2]}"
        return msg
    
