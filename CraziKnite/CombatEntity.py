import arcade
from os import listdir
from os.path import isfile, join
def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class CombatEntity(arcade.Sprite):
    def __init__(self,name,scale = 1):
        super().__init__()

        # Default to facing right
        self.facing_direction = 0

        self.cur_animation = "Idle"
        self.loop_animation = False
        # Used for image sequences
        self.cur_texture = 0
        self.scale = scale

        main_path = "Entities/"+name+"/t"
        onlyfiles = listdir(main_path)
        c = 0
        self.Textures = []
        self.Names = []
        while(c<len(onlyfiles)):
            self.Textures.append(load_texture_pair(main_path+"/"+onlyfiles[c]))
            self.Names.append(onlyfiles[c][:-4]) #ignore .png
            c += 1
        print(self.Names)
        self.texture = self.Textures[0][self.facing_direction]

        self.AC = 5
        self.TempAC = 0
        self.HP = 10
        #D and D!!
        self.EquipedItems = []
        self.MaxEquiped = 5
        self.Inventory = []
        self.Resistances = []
        self.Immunities = []
        self.Proficiencies = []
        self.ProfScores = []
        
        self.RadXMod = 0
        self.RadYMod = 0

        self.IntervalCounter = 0
        self.Delay = 1
        self.center_x = 0
        self.center_y = 0
        self.GAMEFILEID = ""
        self.EntityCollisionTrigger = False
        self.ObjectCollisionTrigger = False
        self.EntityCollisions = []
        self.ObjectCollisions = []
    def Freeze(self):
        self.remove_from_sprite_lists()
    def Unfreeze(self,level):
        level.npc_list.append(self)
        self.LVL = level
    #Animation:
    def SetState(self,state):
        if(not self.cur_animation == str(state)):    
            self.cur_animation = str(state)
            self.cur_texture = 1
            self.IntervalCounter = 0
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
                self.cur_texture = 1
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
            self.ObjectCollisions = []
        if(len(self.EntityCollisions)>0):
            for z in self.EntityCollisions:
                self.OnEntityCollision(z)
        if(len(self.ObjectCollisions)>0):
            for z in self.ObjectCollisions:
                self.OnObjectCollision(z)
        self.Active(level)
    def Active(self,level):
        donothing = 0
    def Save(self,file):
        f = open(file,mode='w')
        f.write(str(self.center_x)+"?!?END...SYMBOL!?!"+str(self.center_y)+"?!?END...SYMBOL!?!"+str(DATA))
        f.close()
    def MoveScenes(self,From,To):
        LevelManager.Move(self,From,To)
        while(c<len(self.Inventory)):
            self.Inventory[c].MoveScenes(From,To)
            c += 1
        while(c<len(self.EquipedItems)):
            self.EquipedItems[c].MoveScenes(From,To)
            c += 1
    def update(self): 
        self.Passive()
        self.Update(self.LVL)
    def Passive(self):
        donothingvar = 0
    def OnObjectCollision(self,obj):
        donothing = 0
    def OnEntityCollision(self,ent):
        donothing = 0
    
