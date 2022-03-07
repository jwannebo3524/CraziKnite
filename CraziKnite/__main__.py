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
GRAVITY = (0,0.6)
PLAYER_JUMP_SPEED = 20
DAMPING = 0.2
PLAYER_FRICTION = 0.2
PLAYER_MASS = 10
PLAYER_MAX_HORIZONTAL_SPEED = 100
IMM_FRICTION = 0.2

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

PLAYER_MOVEMENT_SPEED = 4

DATA_FILE = "gamedata"

LAYER_NAME_BACKDROP = "BACKDROP"
LAYER_NAME_IMMOBILE = "IMMOBILE"
LAYER_NAME_CLIMBABLE = "CLIMBABLE"
LAYER_NAME_MOBILE = "MOBILE"
LAYER_NAME_NPC = "NPC"
LAYER_NAME_PLAYER = "PLAYER"

PLAYER_MOVE_FORCE_ON_GROUND = 40
JUMP_FORCE = 20

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
    def setup(self):
        self.INVENTORY = InventoryManager.InventoryManager()
        self.INVENTORY.SetupSlots()
        self.INV_OPEN = False
        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        """Set up the game here. Call this function to restart the game."""
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DAMPING,
                                                         gravity=GRAVITY)
        
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

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        tile_map = self.tile_map
        self.immobile_list = tile_map.sprite_lists["IMMOBILE"]
        self.player_list = arcade.SpriteList()
        self.mobile_list = tile_map.sprite_lists["MOBILE"]
        self.npc_list = tile_map.sprite_lists["NPC"]
        self.climbable_list = tile_map.sprite_lists["CLIMBABLE"]

        #player
        self.player_sprite = EntityManager.EntityManager.get("CraziKnite")
        self.player_sprite.center_x = 10
        self.player_sprite.center_y = 1000
        self.player_list.append(self.player_sprite)

        slashy = ItemManager.ItemManager.get("Slashy")
        slashy.center_x = 30
        slashy.center_y = 1000
       # print('YEEE')
        slashy.Unfreeze(self)
        main_path = "LevelData/"+self.LVname[:-5]


        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_HORIZONTAL_SPEED)
        self.physics_engine.add_sprite_list(self.immobile_list,
                                            friction=IMM_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.mobile_list,
                                            friction=IMM_FRICTION,
                                            collision_type="wall",
                                            )
        self.physics_engine.add_sprite_list(self.climbable_list,
                                            friction=IMM_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

     #   files = listdir(main_path)
       # c = 0
      #  while(c<len(files)):
       #     inst = EntityManager.get(files[c])
       #     inst.Load(main_path+"/"+files[c])
        #    c += 1

        # -- mobile
 #       Mobile_Layer = self.tile_map.object_lists[LAYER_NAME_MOBILE]
#
  #      for my_object in Mobile_Layer:
   #         cartesian = self.tile_map.get_cartesian(
    #            my_object.shape[0], my_object.shape[1]
#            )
 #           obj_type = my_object.properties["type"]
 #           obj = EntityManager.EntityManager.get(obj_type)
  #          obj.init()
  #          obj.center_x = cartesian[0]
  #          obj.center_y = cartesian[1]
            
  #          self.scene.add_sprite(LAYER_NAME_MOBILE, obj)

        # -- NPC
 #       NPC_Layer = self.tile_map.object_lists[LAYER_NAME_NPC]
#
 #       for my_object in NPC:
  #          cartesian = self.tile_map.get_cartesian(
   #             my_object.shape[0], my_object.shape[1]
   #         )
   #         obj_type = my_object.properties["type"]
   #         obj = EntityManager.EntityManager.get(obj_type)
    #        obj.init()
    #        obj.center_x = cartesian[0]
   #         obj.center_y = cartesian[1]
            
    #        self.scene.add_sprite(LAYER_NAME_NPC, obj)



        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
      #  print("BEEEE")
    #    print("ZEEEEE")

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.player_list.draw()
        self.immobile_list.draw()
        self.mobile_list.draw()
        self.climbable_list.draw()
        self.npc_list.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()



        # Draw hit boxes.
        # for wall in self.wall_list:
        #     wall.draw_hit_box(arcade.color.BLACK, 3)
        #
        # self.player_sprite.draw_hit_box(arcade.color.RED, 3)

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.facing_direction = 1
            # Create a force to the left. Apply it.
            force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.player_sprite.SetState("Moving")
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.facing_direction = 0
            self.player_sprite.SetState("Moving")
            # Create a force to the right. Apply it.
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.player_sprite, 1.0)
            self.player_sprite.SetState("Idle")

        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        if self.up_pressed and is_on_ground:
            self.physics_engine.apply_force(self.player_sprite,(0,JUMP_FORCE))

        if self.right_pressed and self.INV_OPEN:
            self.INVENTORY.FlipRight(self)
        if self.left_pressed and self.INV_OPEN:
            self.INVENTORY.FlipLeft(self)

        #_______________________________
        if ('e' in self.KeyPresses):
            self.INVENTORY.OpenInventory(self)
            self.INV_OPEN = True
        else:
            if(self.INV_OPEN):
                self.INVENTORY.CloseInventory(self)
                self.INV_OPEN = False

        self.player_sprite.ProcessKeychange(self)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
     #   print("keypress!!!")
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
        self.process_keychange()

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

       # print("PREEEE")
        # Move the player with the physics engine

        # Update animations
   #     if self.physics_engine.can_jump():
    #        self.player_sprite.can_jump = False
    #    else:
     #       self.player_sprite.can_jump = True

     #   if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
      #      self.player_sprite.is_on_ladder = True
      #      self.process_keychange()
     #   else:
      ##      self.player_sprite.is_on_ladder = False
     #       self.process_keychange()

               # Update Animations
      #  print("LEEEEEEE")
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_BACKDROP,
                LAYER_NAME_NPC,
                LAYER_NAME_MOBILE,
                LAYER_NAME_PLAYER
            ],
        )
      #  print("KEEEEEEEE")

        # Update moving platforms, enemies, and bullets
        self.scene.update(
            [LAYER_NAME_NPC, LAYER_NAME_PLAYER, LAYER_NAME_MOBILE]
        )
      #  print("XEEEEEEE")
          #  self.scene.update(self.INVEN)
        # See if the enemy hit a boundary and needs to reverse direction.
    #    for npc in self.scene[LAYER_NAME_NPC]:
    ##        npc.update(self)
    #    for mobile in self.scene[LAYER_NAME_MOBILE]:
    #        mobile.update(self)
        self.player_sprite.Update(self)
        # Position the camera
        self.center_camera_to_player()
        self.physics_engine.step()
        


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
