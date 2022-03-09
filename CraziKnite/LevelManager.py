from os import listdir
import os
from os.path import isfile, join
class LevelManager:
    def Move(THING,FROM,TO):
        if(isfile("LevelData/"+FROM+"/"+THING.GAMEFILEID)):
            os.remove("LevelData/"+FROM+"/"+THING.GAMEFILEID)
        THING.Save("LevelData/"+TO+"/"+THING.GAMEFILEID)
    
