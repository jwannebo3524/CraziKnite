from os import listdir
import os
from os.path import isfile, join

#needs fixing.
class LevelManager:
    def Move(THING,FROM,TO):
        try:
            if(THING.LAYER == "NPC" or THING.LAYER == "PLAYER"):
                if(isfile("LevelData/"+FROM+"/entity_list.txt")):
                    f = open("LevelData/"+FROM+"/entity_list.txt","rw")
                    z = f.read()
                    Entity_List = ",".split(z[1:-1])
                    n = Entity_List.index(THING.center_x) #FIXTHIS later
                    
                THING.Save("LevelData/"+TO+"/"+THING.GAMEFILEID)
            else:
                if(isfile("LevelData/"+FROM+"/"+THING.GAMEFILEID)):
                    os.remove("LevelData/"+FROM+"/"+THING.GAMEFILEID)
                THING.Save("LevelData/"+TO+"/"+THING.GAMEFILEID)
        except:
            pass
