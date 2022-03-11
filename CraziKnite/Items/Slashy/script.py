import ItemEntity
import Utility

class item(ItemEntity.Item):
    def __init__(self,Name):
        #print("beeep")
        super().__init__(Name,scale = 4)
        self.Do("Grounded")
        self.loop_animation = True
        self.PickUp = True
        self.ItemType = "Body"
        self.Slashing = False
        self.Charged = True
        self.Timer = 0
    def Active(self,level):
        self.facing_direction = self.Attatched.facing_direction
        if(self.Attatched == level.player_sprite):
           # print("ready...")
            if('z' in level.KeyPresses):
                if(self.Charged):
                    print("SLASHHH")
                    self.Do("Slash")
                    self.Delay = 5
                    self.loop_animation = False
                    self.Charged = False
                    self.Slashing = True
                    self.Timer = 100
            if(self.Timer<80):
                self.Slashing = False
                self.Do("InHand")
                self.loop_animation = True
            if(self.Timer<0):
                self.Charged = True
                self.Timer = 0
            self.Timer -= 1
        else:
            self.Do("Grounded")
            self.loop_animation = True
    def OnCollision(self,obj):
        print("col")
        print(self.Slashing)
        print(obj.LAYER)
        if(self.Slashing == True and obj.LAYER == "NPC"):
            Utility.Damage(obj,[2,6,0],2)
            print("DAMAGE!!!")
        #print(self.change_y)
                
