import ItemEntity

class item(ItemEntity.Item):
    def __init__(self,Name):
        #print("beeep")
        super().__init__(Name,scale = 4)
        self.Do("Grounded")
        self.loop_animation = True
        self.PickUp = True
        self.ItemType = "Body"
    def Active(self,level):
        self.facing_direction = self.Attatched.facing_direction
        if(self.Attatched == level.player_sprite):
           # print("ready...")
            if('z' in level.KeyPresses):
               # print("SLASHHH")
                self.Do("Slash")
                self.Delay = 5
                self.loop_animation = False
            else:
                self.Do("InHand")
        else:
            self.Do("Grounded")
            self.loop_animation = True
        #print(self.change_y)
                
