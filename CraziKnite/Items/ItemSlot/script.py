import ItemEntity

class item(ItemEntity.Item):
    def __init__(self,Name,col = 0,row = 0,spacing = 10):
        #print("beeep")
        super().__init__(Name,scale = 1)
        self.X = (col-5)*10
        self.Y = (row-5)*10
    def Active(self,level):
        x = level.player_sprite.center_x
        y = level.player_sprite.center_y
        self.center_x = self.X+x
        self.center_y = self.Y+y
        
