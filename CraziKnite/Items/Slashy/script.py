import ItemEntity

class item(ItemEntity.Item):
    def __init__(self,Name):
        #print("beeep")
        super().__init__(Name,scale = 1)
        self.Do("Grounded")
        self.loop_animation = True
        self.PickUp = True
        self.ItemType = "Body"
    def Active(self,level):
        if(self.Attatched == level.player_sprite):
            if('z' in level.KeyPresses):
                self.Do("Slash")
                self.loop_animation = False
        else:
            self.Do("Grounded")
            self.loop_animation = True
        self.change_y = self.change_y - 1
        print(self.change_y)
                
