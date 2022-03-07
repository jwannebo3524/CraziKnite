import arcade
from os import listdir
from os.path import isfile, join
import LevelManager
import random
#item
def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]
class Item(arcade.Sprite):
    
    def __init__(self,name,facing = 0,scale = 1):
        super().__init__()

        # Default to facing right
        self.facing_direction = facing

        self.cur_animation = "Idle"
        self.loop_animation = False
        # Used for image sequences
        self.cur_texture = 0
        self.scale = scale
        self.NAME = name
        main_path = "Items/"+name+"/t"
        onlyfiles = listdir(main_path)
        c = 0
        self.Textures = []
        self.Names = []
        while(c<len(onlyfiles)):
            self.Textures.append(load_texture_pair(main_path+"/"+onlyfiles[c]))
            self.Names.append(onlyfiles[c][:-4]) #ignore .png
            c += 1
        print(self.Names)
        self.texture = self.Textures[facing][self.facing_direction]
        self.Attatched = None
        self.offsetX = 0
        self.offsetY = 0
        self.EntityCollisionTrigger = False
        self.ObjectCollisionTrigger = False
        self.EntityCollisions = []
        self.ObjectCollisions = []
        self.center_x = 0
        self.center_y = 0
        self.DATA = []
        self.InLevel = ""
        self.GAMEFILEID = ""
        self.HASHID = 0
    def Freeze(self):
        self.remove_from_sprite_lists()
    def Unfreeze(self,level):
        level.mobile_list.append(self)
        self.LVL = level
    def SetAttatched(self,attached):
        self.Attached = attached
    def update(self): 
        try:
            d = (self.Attached.facing_direction-0.5)*2
            self.center_x = self.Attached.center_x + (d*self.offsetX*self.Attatched.RadXMod)
            self.center_y = self.Attached.center_y + (d*self.offsetY*self.Attatched.RadYMod)
        except:
            donothingvar = 0
        self.Passive()
        self.Update(self.LVL)
    def Update(self,level):
        if(self.EntityCollisionTrigger):
            self.EntityCollisions = arcade.check_for_collision_with_lists(
                self,
                [
                    level.scene["NPC"],
                    level.scene["PLAYER"],
                ],
            )
        else:
            self.EntityCollisions = []
        if(self.ObjectCollisionTrigger):
            self.ObjectCollisions = arcade.check_for_collision_with_lists(
                self,
                [
                    level.scene["MOBILE"],
                ],
            )
        else:
            self.EntityCollisions = []
        if(len(self.EntityCollisions)>0):
            for z in self.EntityCollisions:
                self.OnEntityCollision(z)
        if(len(self.ObjectCollisions)>0):
            for z in self.ObjectCollisions:
                self.OnObjectCollision(z)
        self.Active(level)
    def Passive(self): 
        donothingvar = 0
    def Do(self,action):
        self.SetState(action)
        
    def OnEntityCollision(self,col):
        donothingvar = 0
    def OnObjectCollision(self,col):
        donothingvar = 0
    def Active(self,level):
        donothingvar = 0

    def Save(self,file):
        f = open(file,mode='w')
        f.write(str(self.center_x)+"?!?END...SYMBOL!?!"+str(self.center_y)+"?!?END...SYMBOL!?!"+str(self.DATA))
        f.close()
    def Load(self,file):
        try:
            f = open(file,mode='r')
            z = f.read()
            f.close()
            array = "?!?END...SYMBOL!?!".split(z)
            self.center_x = array[0]
            self.center_y = array[1]
            k = array[2][1:-1]
            self.DATA = ",".split(k)
        except:
            print("rawr")
        self.GAMEFILEID = file
    def MoveScenes(self,From,To):
        LevelManager.Move(self,From,To)
        

    #Animation:
    def SetState(self,state):
        if(not self.cur_animation == str(state)):    
            self.cur_animation = str(state)
            self.cur_texture = 0
    def update_animation(self,delta_time):
        at = self.cur_animation+str(self.cur_texture)
        if(at in self.Names):
            self.texture = self.Textures[self.Names.index(at)][self.facing_direction]
            self.IntervalCounter += 1
            if(self.IntervalCounter>self.Delay):
                self.cur_texture += 1
                self.IntervalCounter = 0
        else:
            if(self.loop_animation):
                self.cur_texture = 0
                if(at in self.Names):
                    self.texture = self.Textures[self.Names.index(at)][self.facing_direction]
                    self.IntervalCounter += 1
                    if(self.IntervalCounter>self.Delay):
                        self.cur_texture += 1
                        self.IntervalCounter = 0
            else:
                self.cur_texture = 0
                self.IntervalCounter = 0
                self.cur_animation = "Idle"
  #  def __eq__(self,other):
  #      try:
  #          return self.HASHID==other.HASHID
   #     except:
    #        return False
  #  def __hash__(self):
   #     return self.HASHID
    
