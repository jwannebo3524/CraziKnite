import arcade
import importlib

class ItemyManager:
    def get(Name):
        try:
          print("Items."+Name)
          module = importlib.import_module('Items.'+Name+'.script')
          my_instance = module.item(Name)
          return my_instance
        except:
          print("Error loading item")
          return
    def getIcon(Name):
        try:
          print("Items."+Name)
          module = importlib.import_module('Items.'+Name+'.icon')
          my_instance = module.item(Name)
          return my_instance
        except:
          print("Error loading item icon")
          return
        
