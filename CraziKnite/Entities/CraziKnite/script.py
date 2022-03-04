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
    def __init__(self,name,scale = 1):
        super().__init__(name)

        
