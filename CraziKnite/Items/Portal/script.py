import ItemEntity

class item(ItemEntity.Item):
    def __init__(self,Name):
        #print("beeep")
        super().__init__(Name,scale = 4)
        self.Do("Idle")
        self.loop_animation = True
        self.PickUp = False
        self.ItemType = "Body"
        self.Target = "SplicedVallies_01" #default target
    def OnCollision(self,other):
        try:
            if(other.LAYER == "PLAYER"):
                other.MoveScenes(self.LVL.current,self.Target)
        except:
            print("uuuhhhh? whut?")
            
        #print(self.change_y)
                
