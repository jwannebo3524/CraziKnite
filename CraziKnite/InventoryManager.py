import ItemManager
import EntityManager
import arcade


class InventoryManager:
  def __init__(self):
    self.InventorySlots = []
    self.EquipedSlots = []
    self.Inventories = []
    self.ItemIcons = []
    self.ItemEntities = []
    self.Equiped = []
    self.EquipedIcons = []
    self.ID = 0
    self.Open = False
    #[Name,DataFile]
  def Save(self):
    f = open("InventoryData")
    f.write([self.Inventories,self.Equiped])
    f.close()
  def Load(self):
    f = open("InventoryData")
    raw = f.read()
    #TODO: convert raw to array
  def LoadTab(self,ID):
    self.Open = True
    c = 0
    while(c<len(self.Inventories[ID])):
      icon = ItemManager.ItemManager.getIcon(self.Inventories[ID][c][0])
      self.ItemIcons.append(icon)
      entity = ItemManager.ItemManager.get(self.Inventories[ID][c][1])
      self.ItemEntities.append(entity)
      c += 1
  def DisplayInventory(self,level):
    self.Open = True
    c = 0
    while(c<len(self.ItemIcons)):
      if(self.ItemIcons[c]):
        self.ItemIcons[c].Attatch(self.InventorySlots[c])
        self.ItemIcons[c].Unfreeze(level)
      self.InventorySlots[c].Unfreeze(level)
      c += 1
  def CloseInventory(self,level):
    self.Open = False
    c = 0
    while(c<len(self.ItemIcons)):
      if(self.ItemIcons[c]):
        self.ItemIcons[c].Freeze()
      self.InventorySlots[c].Freeze()
      c += 1
  def DisplayEquipped(self,level):
    c = 0 
    while(c<len(self.EquipedIcons)):
      if(self.EquipedIcons[c]):
        self.EquipedIcons[c].Attach(self.EquipedSlots[c])
        self.EquipedIcons[c].Unfreeze(level)
        self.EquipedItems[c].Unfreeze(level)
      self.EquipedSlots.Unfreeze(level)
      c += 1
  def Equip(self,level,z,to): #allows equiping blank spaces. Inventory must be open.
    icon = None
    entity = None
    if(self.EquipedIcons[to]):
        icon = self.EquipedIcons[to]
        entity = self.Equiped[to]
    if(self.ItemIcons[z]):
      self.Equiped[to] = self.ItemEntities[z]
      self.EquipedIcons[to] = self.ItemIcons[c]
      self.Equiped[to].Unfreeze(level)
      self.EquipedIcons[to].Unfreeze(level)
      self.Equiped[to].Attach(level.player_sprite)
      self.EquipedIcons[to].Attach(self.EquipedSlots[to])
      
    else:
      self.Equiped[to] = None
      self.EquipedIcons[to] = None
    if(icon):
      self.ItemIcons[z] = icon
      self.ItemEntities[z] = entity
      entity.Freeze()
      self.ItemIcons[z].Attach(self.InventorySlots[z])
    else:
      self.ItemIcons[z] = None
      self.ItemEntities[z] = None
      
    
    
