import arcade
from os import listdir
from os.path import isfile, join
import CombatEntity
def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class entity(CombatEntity.CombatEntity):
    def __init__(self,name,scale = 2):
        super().__init__(name,scale = scale)
        self.HeadArmor = None
        self.InHand = None
        self.BodyArmor = None
        self.Charms = []
        self.Interacting = False
    def ProcessKeychange(self,level):
        if("d" in level.KeyPresses):
            if(self.Interacting == False):
                self.Interacting = True
                self.ObjectCollisionTrigger = True
        else:
            if(self.Interacting == True):
                self.Interacting = False
                self.ObjectCollisionTrigger = False
    def OnObjectCollision(self,obj):
        try:
            if(obj.PickUp):
                if(obj.ItemType == "Head"):
                    if(self.HeadArmor):
                        self.HeadArmor.SetAttatched(None)
                        self.HeadArmor.center_x = self.center_x + 5
                        self.HeadArmor.change_x = -5
                        self.HeadArmor.change_y = 1
                        self.HeadArmor.PickUp = True
                        self.HeadArmor = None
                    self.HeadArmor = obj
                    obj.SetAttatched(self)
                    obj.PickUp = False
                if(obj.ItemType == "Body"):
                    if(self.BodyArmor):
                        self.BodyArmor.SetAttatched(None)
                        self.BodyArmor.center_x = self.center_x + 5
                        self.BodyArmor.change_x = -5
                        self.BodyArmor.change_y = 1
                        self.BodyArmor.PickUp = True
                        self.BodyArmor = None
                    self.BodyArmor = obj
                    obj.SetAttatched(self)
                    obj.PickUp = False
                if(obj.ItemType == "Charm"):
                    self.Charms.append(obj)
                    obj.SetAttatched(self)
                    obj.PickUp = False
        except:
            donothingvar = 0
    def Unfreeze(self,lvl):
        self.LVL = lvl
        lvl.player_list.append(self)

        
