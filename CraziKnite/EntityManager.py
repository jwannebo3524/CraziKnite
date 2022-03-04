import arcade
import importlib
class EntityManager:
    def get(Name):
       # try:
        print("Entities."+Name)
        module = importlib.import_module('Entities.'+Name+'.script')
        my_instance = module.entity(Name)
        return my_instance
        #except:
          #  print("Error loading entity")
          #  return
        
class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file,scale = 0.5):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        main_path = f"/Textures/{name_file}"
        onlyfiles = [f for f in listdir(main_path) if isfile(join(mypath, f))]
        while(c<len(onlyfiles)):
            self.Textures.append(load_texture_pair(onlyfiles[c]))
            self.Names.append(onlyfiles[c][:-4]) #ignore .png
            c += 1
