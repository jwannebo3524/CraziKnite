import ItemEntity

class item(ItemEntity.Item):
    def __init__(self,Name):
        #print("beeep")
        super().__init__(Name,scale = 1)
        self.Do("Icon")
        self.loop_animation = True
   # def Active(self,level):
        
                
