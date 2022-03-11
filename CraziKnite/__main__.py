"""
CraziKnite main. Literally copy/pasted from python arcade totorial.
"""
import math
import os
from os import listdir
from os.path import isfile, join
import arcade
import EntityManager
import InventoryManager
import ItemManager

# Constants
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "CraziKnite"

# Movement speed of player, in pixels per frame
GRAVITY = 0.7
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

TILE_SCALING = 2

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_MOVEMENT_SPEED = 3
SPEED = 30000
JUMP_SPEED = 30000
JUMP_DECAY = 0.9

DATA_FILE = "gamedata"

LAYER_NAME_BACKDROP = "BACKDROP"
LAYER_NAME_IMMOBILE = "IMMOBILE"
LAYER_NAME_CLIMBABLE = "CLIMBABLE"
LAYER_NAME_MOBILE = "MOBILE"
LAYER_NAME_NPC = "NPC"
LAYER_NAME_PLAYER = "PLAYER"

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file,scale = 0.5):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        main_path = f"Entities/{name_folder}/Textures/{name_file}"
        onlyfiles = [f for f in listdir(main_path) if isfile(join(mypath, f))]
        while(c<len(onlyfiles)):
            self.Textures.append(load_texture_pair(onlyfiles[c]))
            self.Names.append(onlyfiles[c][:-4]) #ignore .png
            c += 1

        
class Level(arcade.View):
    """
    Main application class.
    """

    def __init__(self,name):
        """
        Initializer for the game
        """

        # Call the parent class and set up the window
        super().__init__()

        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        self.end_of_map = 0

        self.jump_needs_reset = False
        self.KeyPresses = []


        self.LVname = name
        self.MAP = name
        self.CallOnKeypress = []
        
    def setup(self):
        
        self.Jumping = False
        self.Force = 0
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=0.01,
                                                         gravity=(0,-5000))
        self.INVENTORY = InventoryManager.InventoryManager()
        self.INVENTORY.SetupSlots()
        self.INV_OPEN = False
        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Map name
        self.Data = "LVdata/"+self.LVname
        map_name = "Maps/"+self.LVname

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_BACKDROP: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_IMMOBILE: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_CLIMBABLE: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOBILE: {
                "use_spatial_hash": False,
            },
            LAYER_NAME_NPC: {
                "use_spatial_hash": False,
            },
            LAYER_NAME_PLAYER: {
                "use_spatial_hash": False,
            },
        }

        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        tile_map = self.tile_map

        self.immobile_list = tile_map.sprite_lists["IMMOBILE"]
        self.climbable_list = tile_map.sprite_lists["CLIMBABLE"]
        self.backdrop_list = tile_map.sprite_lists["BACKDROP"]
        self.mobile_list = tile_map.sprite_lists["MOBILE"]
        self.npc_list = tile_map.sprite_lists["NPC"]
        self.player_list = arcade.SpriteList()
        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.physics_engine.add_sprite_list(self.immobile_list,
                                            friction=0.2,
                                            collision_type="immobile",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.climbable_list,
                                            friction=20,
                                            collision_type="immobile",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        #player
        self.player_sprite = EntityManager.EntityManager.get("CraziKnite")
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 1000
        self.player_sprite.Unfreeze(self)
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=0.2,
                                       mass=1,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=1000,
                                       max_vertical_velocity=1000)
        slashy = ItemManager.ItemManager.get("Slashy") #TODO: remove
        slashy.center_x = 300
        slashy.center_y = 1100
        slashy.Unfreeze(self)
       # print('YEEE')
        #self.scene.add_sprite(LAYER_NAME_MOBILE, slashy)
        main_path = "LevelData/"+self.LVname[:-5]



        #         Loading functions:

        #load entities
        f = open(main_path+"/entity_list.txt")
        z = f.read()
        f.close()
        print("Z:" + z)
        if(len(z)>1):
            Entity_List = z[1:-1].split(",")
        else:
            Entity_List = []
        print(Entity_List)
        print("bleep")
        c = 0
        while(c<len(Entity_List)):
            data = Entity_List[c][1:-1].split(" ")
            print(data)
            entity = EntityManager.EntityManager.get(str(data[0]))
            entity.center_x = int(data[1])
            entity.center_y = int(data[2])
            entity.ID = str(data[3])
            entity.Unfreeze(self)
            c += 1

        #load items
        f = open(main_path+"/item_list.txt")
        z = f.read()
        f.close()
        if(len(z)>1):
            Entity_List = z[1:-1].split(",")
        else:
            Entity_List = []
        c = 0
        while(c<len(Entity_List)):
            data = Entity_List[c].split(" ")
            entity = ItemManager.ItemManager.get(str(data[0]))
            entity.center_x = int(data[1])
            entity.center_y = int(data[2])
            entity.ID = str(data[3])
            entity.Unfreeze(self)
            c += 1
        
        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)


        self.physics_engine.add_sprite_list(self.mobile_list,
                                            friction=0.2,
                                            moment_of_intertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                            collision_type="mobile")
        self.physics_engine.add_sprite_list(self.npc_list,
                                            friction=0.2,
                                            moment_of_intertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                           collision_type="npc")

        self.physics_engine.add_collision_handler("npc", "mobile", post_handler=self.HandleCollision)
        self.physics_engine.add_collision_handler("npc", "npc", post_handler=self.HandleCollision)
        self.physics_engine.add_collision_handler("npc", "player", post_handler=self.HandleCollision)
        #self.physics_engine.add_collision_handler("mobile", "player", post_handler=self.HandleCollision)
        self.physics_engine.add_collision_handler("mobile", "npc", post_handler=self.HandleCollision)
        self.physics_engine.add_collision_handler("mobile", "mobile", post_handler=self.HandleCollision)
    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()
    
        # Draw our Scene
        self.immobile_list.draw()
        self.backdrop_list.draw()
        self.climbable_list.draw()
        self.mobile_list.draw()
        self.npc_list.draw()
        self.player_list.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()



         #Draw hit boxes.
       # for mobile in self.mobile_list:
       #     mobile.draw_hit_box(arcade.color.GREEN, 3)
        
       # self.player_sprite.draw_hit_box(arcade.color.RED, 3)

    def process_keychange(self):
   
        # Process up/down
        if self.up_pressed and not self.down_pressed:
                if(self.Jumping):
                    self.Force = self.Force*JUMP_DECAY
                    self.physics_engine.apply_force(self.player_sprite, (0,self.Force))
                    if(self.Force<1000):
                        self.Force = 0
                        self.Jumping = False
                if (
                self.physics_engine.is_on_ground(self.player_sprite)
                and not self.jump_needs_reset
            ):
                    self.physics_engine.apply_force(self.player_sprite, (0,JUMP_SPEED))
                #print("jump!")
                    self.jump_needs_reset = True
                 #arcade.play_sound(self.jump_sound)
                    self.Jumping = True
                    self.Force = JUMP_SPEED

        # Process up/down when on a ladder and no movement
        # Process left/right
        if self.right_pressed and not self.left_pressed and not self.INV_OPEN:
            self.player_sprite.SetState("Moving")
            self.player_sprite.facing_direction = 0
            self.physics_engine.apply_force(self.player_sprite, (SPEED,0))
            self.physics_engine.set_friction(self.player_sprite, 0.0)
        elif self.left_pressed and not self.right_pressed and not self.INV_OPEN:
            self.player_sprite.SetState("Moving")
            self.player_sprite.facing_direction = 1
            self.physics_engine.apply_force(self.player_sprite, (-SPEED,0))
            self.physics_engine.set_friction(self.player_sprite, 0.0)
        else:
            self.player_sprite.change_x = 0
            self.player_sprite.SetState("Idle")
            self.physics_engine.set_friction(self.player_sprite, 1.0)
        #_______________________________


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
       # print("keypress!!!")
        if key == arcade.key.UP:# or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN:# or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT:# or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:# or key == arcade.key.D:
            self.right_pressed = True
            
        if key == arcade.key.Z:
            self.KeyPresses.append("z")
        elif key == arcade.key.X:
            self.KeyPresses.append("x")
        elif key == arcade.key.C:
            self.KeyPresses.append("c")
        elif key == arcade.key.A:
            self.KeyPresses.append("a")
        elif key == arcade.key.S:
            self.KeyPresses.append("s")
        elif key == arcade.key.E:
            self.KeyPresses.append("e")
        elif key == arcade.key.D:
            self.KeyPresses.append("d")
        

        self.process_keychange()
        c = 0
        while(c<len(self.CallOnKeypress)):
            self.CallOnKeyPress[c].OnKeyPress()
            c += 1
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP:# or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN:# or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT:# or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:# or key == arcade.key.D:
            self.right_pressed = False

        elif key == arcade.key.Z:
            self.KeyPresses.pop(self.KeyPresses.index("z"))
        elif key == arcade.key.X:
            self.KeyPresses.pop(self.KeyPresses.index("x"))
        elif key == arcade.key.S:
            self.KeyPresses.pop(self.KeyPresses.index("s"))
        elif key == arcade.key.C:
            self.KeyPresses.pop(self.KeyPresses.index("c"))
        elif key == arcade.key.A:
            self.KeyPresses.pop(self.KeyPresses.index("a"))
        elif key == arcade.key.E:
            self.KeyPresses.pop(self.KeyPresses.index("e"))
        elif key == arcade.key.D:
            self.KeyPresses.pop(self.KeyPresses.index("d"))
        c = 0
        while(c<len(self.CallOnKeypress)):
            self.CallOnKeyPress[c].OnKeyRelease()
            c += 1
        self.process_keychange()

    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, speed)

    def on_update(self, delta_time):
        """Movement and game logic"""

     #   print("PREEEE")
        # Move the player with the physics engine
        self.physics_engine.step()
        self.process_keychange()


               # Update Animations
      #  print("LEEEEEEE")
       # self.scene.update_animation(
       ##     delta_time,
        #    [
       #         LAYER_NAME_BACKDROP,
        #        LAYER_NAME_NPC,
        #        LAYER_NAME_MOBILE,
        #        LAYER_NAME_PLAYER,
       #     ],
       # )
        self.scene.update_animation([self.backdrop_list,
                                     self.mobile_list,
                                     self.npc_list,
                                     self.player_list])
     #   print("KEEEEEEEE")

        # Update moving platforms, enemies, and bullets
    #    self.scene.update([self.mobile_list,
       #                              self.npc_list,
       #                              self.player_list])
      #  print("XEEEEEEE")
          #  self.scene.update(self.INVEN)
        # See if the enemy hit a boundary and needs to reverse direction.
    #    for npc in self.scene[LAYER_NAME_NPC]:
    ##        npc.update(self)
    #    for mobile in self.scene[LAYER_NAME_MOBILE]:
    #        mobile.update(self)
        #Animation - Mobile
        c = 0
        while(c<len(self.mobile_list)):
            try:
                self.mobile_list[c].update_animation(delta_time)
            except:
                pass
            c += 1

        #Animation - Npc
        c = 0
        while(c<len(self.npc_list)):
            try:
                self.npc_list[c].update_animation(delta_time)
            except:
                pass
            c += 1
        #Animation - Player
        self.player_sprite.update_animation(delta_time)

        #main- mobile
        c = 0
        while(c<len(self.mobile_list)):
            try:
                self.mobile_list[c].update()
            except:
                pass
            c += 1
        #main - npc
        c = 0
        while(c<len(self.npc_list)):
            try:
                self.npc_list[c].update()
            except:
                pass
            c += 1
        #main- player
        self.player_sprite.update()
        # Position the camera
        self.center_camera_to_player()
    def HandleCollision(self,Obj1,Obj2, _arbiter, _space, _data):
        try:
            Obj1.OnCollision(Obj2)
        except:
            pass
        try:
            Obj2.OnCollision(Obj1)
        except:
            pass
    

def main():
    """Main function"""
    # init window
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    f = open(DATA_FILE,mode='r')
    data = f.read()
    f.close()
    #init a scene
    scene = Level(data)
    #setup scene
    window.show_view(scene)
    scene.setup()
    arcade.run()


if __name__ == "__main__":
    main()
