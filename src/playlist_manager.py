
from collections import deque

#cola= deque()
#cola.append("taylor swift")
#cola.append("lana del rey")
#cola.append("suede")
#cola.append("the smiths")

import emoji


##DICCI = {
##    "LoboBobo's server": {
##        "Chat de voz 1": {
##            "Queue": deque(),
##            "Last-Played": None
##        },
##       "Otro canal": {
##            "Queue": deque(),
##            "Last-Played": None
##       }
##    }
##}
DICCI={}

async def add_to_playlist(url, channel, server):
  
    if server not in DICCI:
        DICCI[server] = {}
        print("El servidor no estaba en el diccionario. Se ha creado.")

 
    if channel not in DICCI[server]:
        DICCI[server][channel] = {
            "Queue": deque(), 
            "Last-Played": None
        }
        print(f"el canal '{channel}' no estaba en el servidor. Se ha creado")

 
    DICCI[server][channel]["Queue"].append(url)
    print(f"canción agregada a la cola del canal '{channel}' en el servidor '{server}'.")

    # 
    print("contenido actual de la cola en el canal:", DICCI[server][channel]["Queue"])
    



