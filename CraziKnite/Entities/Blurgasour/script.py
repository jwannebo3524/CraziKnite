import arcade
from os import listdir
from os.path import isfile, join
import CombatEntity
import Utility
def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class entity(CombatEntity.CombatEntity):
    def __init__(self,name,scale = 0.5):
        super().__init__(name,scale = scale)
        self.HeadArmor = None
        self.InHand = None
        self.BodyArmor = None
        self.Charms = []
        self.Interacting = False
        self.RadXMod = 5
        self.RadYMod = 5
        self.LAYER = "NPC"
        self.Range = 2000
        self.HitRange = 100
        self.Speed = 2000
        self.Timer = 0
        self.Charged = True
        self.AC = 10
        self.HP = 20
    def Active(self,level):
       # print("tick!")
        if(level.player_sprite.center_x<self.center_x+self.HitRange and level.player_sprite.center_x>self.center_x-self.HitRange):
            #print("YEEEEEEEEEE")
            if(level.player_sprite.center_x>self.center_x):
                self.facing_direction = 1
                
            else:
                self.facing_direction = 0
                
            if(self.Charged):
                self.Do("Firepuke")
                self.Charged = False
                self.Timer = 50
                Utility.Damage(level.player_sprite,[1,6,0])
                print("DAMAGE :)")
            else:
                self.Timer-= 1
                if(self.Timer<0):
                    self.Do("Idle")
                if(self.Timer<-100):
                    self.Charged = True
                    self.Timer = -401
        elif(level.player_sprite.center_x<self.center_x+self.Range and level.player_sprite.center_x>self.center_x-self.Range):
            if(level.player_sprite.center_x>self.center_x):
                self.facing_direction = 1
                level.physics_engine.apply_force(self, (self.Speed,0))
            else:
                self.facing_direction = 0
                level.physics_engine.apply_force(self,(-self.Speed,0))
            #print("YRRRRRRRRRRRRRRRRR")
            self.Do("Walking")
            self.Delay = 10
           # print(self.cur_animation)
        
            

        
