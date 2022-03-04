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

class entity(arcade.Sprite):
    def __init__(self,name,scale = 1):
        super().__init__()
        print("something's working?")

        # Default to facing right
        self.facing_direction = 0

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
            print("beep?")
        print(self.Names)
        self.texture = self.Textures[0][self.facing_direction]
    def Update(self,level):
        donothing = 0
