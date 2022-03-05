import ItemEntity

class item(ItemEntity.Item):
    def __init__(self,Name):
        #print("beeep")
        super().__init__(Name,scale = 1)
        self.X = (col-5)*10
        self.Y = (row-5)*10
    def Active(self,level):
        if(self.Attatched = level.player_sprite):
            if('z' in level.KeyPresses):
                self.Do("Slash")
        else:
            self.Do("Flat")
                
