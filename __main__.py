"""
CraziKnite main. Literally copy/pasted from python arcade totorial.
"""
import math
import os
from os import listdir
from os.path import isfile, join
import arcade
import MassInit
import EntityManager

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "CraziKnite"

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

TILE_SCALING = 0.1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_MOVEMENT_SPEED = 1

DATA_FILE = "gamedata"

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

        
class Game(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
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

        self.SceneData = []
        self.SceneKeys = []
    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Map name
        map_name = ":resources:tiled_maps/map_with_ladders.json"

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

        #player
        self.player_sprite = EntityManager.get("CraziKnite")
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        
        # -- mobile
        Mobile_Layer = self.tile_map.object_lists[LAYER_NAME_MOBILE]

        for my_object in Mobile_Layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            obj_type = my_object.properties["type"]
            obj = EntityManager.get(obj_type)
            
            self.scene.add_sprite(LAYER_NAME_MOBILE, obj)

        # -- NPC
        NPC_Layer = self.tile_map.object_lists[LAYER_NAME_NPC]

        for my_object in NPC:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            obj_type = my_object.properties["type"]
            obj = EntityManager.get(obj_type)
            
            self.scene.add_sprite(LAYER_NAME_NPC, obj)



        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_MOBILE],
            gravity_constant=GRAVITY,
            ladders=self.scene[LAYER_NAME_CLIMBABLE],
            walls=self.scene[LAYER_NAME_IMMOBILE]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

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
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                 #arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            
        if key == arcade.key.z:
            self.KeyPresses.append("z")
        elif key == arcade.key.x:
            self.KeyPresses.append("x")
        elif key == arcade.key.c:
            self.KeyPresses.append("c")
        elif key == arcade.key.a:
            self.KeyPresses.append("a")
        elif key == arcade.key.s:
            self.KeyPresses.append("s")
        

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        elif key == arcade.key.z:
            self.KeyPresses.pop(self.KeyPresses.index("z"))
        elif key == arcade.key.x:
            self.KeyPresses.pop(self.KeyPresses.index("x"))
        elif key == arcade.key.s:
            self.KeyPresses.pop(self.KeyPresses.index("s"))
        elif key == arcade.key.c:
            self.KeyPresses.pop(self.KeyPresses.index("c"))
        elif key == arcade.key.a:
            self.KeyPresses.pop(self.KeyPresses.index("a"))

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

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

               # Update Animations
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_BACKDROP,
            ],
        )

        # Update moving platforms, enemies, and bullets
        self.scene.update(
            [LAYER_NAME_NPC, LAYER_NAME_PLAYER, LAYER_NAME_MOBILE]
        )

        # See if the enemy hit a boundary and needs to reverse direction.
        for npc in self.scene[LAYER_NAME_NPC]:
            npc.update(self)
        for mobile in self.scene[LAYER_NAME_MOBILE]:
            mobile.update(self)

        # Position the camera
        self.center_camera_to_player()


def main():
    """Main function"""
    # init window
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    
    data =
    #init a scene
    scene = Game()
    #setup scene
    scene.setup()
    arcade.run()


if __name__ == "__main__":
    main()
