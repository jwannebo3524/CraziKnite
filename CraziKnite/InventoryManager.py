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
    self.MaxItemsInTab = 100
    self.ThrowYVel = 0.1
    self.ThrowXVel = 4
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
    if(ID>=len(self.Inventories)):
      self.Inventories.append([])
    self.Open = True
    c = 0
    while(c<len(self.Inventories[ID])):
      icon = ItemManager.ItemManager.getIcon(self.Inventories[ID][c][0])
      self.ItemIcons.append(icon)
      entity = ItemManager.ItemManager.get(self.Inventories[ID][c][0])
      self.ItemEntities.append(entity)
      
      entity.Load(self.Inventories[ID][c][1])
      c += 1

  def DisplayInventory(self,level):
    self.Open = True
    c = 0
    while(c<self.MaxItemsInTab):
      try:
        self.ItemIcons[c].Attatch(self.InventorySlots[c])
        self.ItemIcons[c].Unfreeze(level)
      except:
        donothingvar = 0
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
      try:
        self.EquipedIcons[c].Attach(self.EquipedSlots[c])
        self.EquipedIcons[c].Unfreeze(level)
        self.EquipedItems[c].Unfreeze(level)
      except:
        donothingvar = 0
      self.EquipedSlots.Unfreeze(level)
      c += 1
  def Equip(self,level,z,to): #allows equiping blank spaces. Inventory must be open.
    icon = None
    entity = None
    try:
      icon = self.EquipedIcons[to]
      entity = self.Equiped[to]
    except:
      donothingvar = 0
    try:
      self.Equiped[to] = self.ItemEntities[z]
      self.EquipedIcons[to] = self.ItemIcons[c]
      self.Equiped[to].Unfreeze(level)
      self.EquipedIcons[to].Unfreeze(level)
      self.Equiped[to].Attach(level.player_sprite)
      self.EquipedIcons[to].Attach(self.EquipedSlots[to])
    except:
      donothingvar = 0
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
  def PickUp(self,level,item): # item entity
    DataFile = item.GAMEFILEID
    name = item.Name #check this.
    c = 0
    k = 0
    k2 = 0
    found = False
    while(c<len(self.Inventories)): #find empty slot
      c2 = 0
      while(c2<len(self.Inventories[c])):
        if(not self.Inventories[c][c2]):
          k = c
          k2 = c2
          c += 99999999999999
          c2 += 99999999
          found = True
        c2 += 1
      if(c2<self.MaxItemsInTab and not found):
         found = True
         k = c
         k2 = c2
         c += 99999999999999
         c2 += 999999999
    if(found == False):
     self.Inventories.append([])
     self.Inventories[-1].append([name,DataFile])
    else:
     self.Inventories[k][k2] = [name,DataFile]
  def Throw(self,level,z):
    self.Equiped[z].Attach(None)
    self.Equiped[z].change_y = self.ThrowYVel
    dir = level.player_sprite.facing_direction #check this
    normdir = (dir*2)-1
    self.Equiped[z].change_x = self.ThrowXVel*normdir
    self.EquipedIcon[z] = None
    self.Equiped[z] = None
  def FlipRight(self,level):
    if(self.ID+1<len(self.Inventories)):
      self.ID += 1
      self.CloseInventory(level)
      self.LoadTab(self.ID)
      self.DisplayInventory(level)
  def FlipLeft(self,level):
    if(self.ID-1>=0):
      self.ID -= 1
      self.CloseInventory(level)
      self.LoadTab(self.ID)
      self.DisplayInventory(level)
  def OpenInventory(self,level):
    self.LoadTab(self.ID)
    self.DisplayInventory(level)
  def SetupSlots(self):
    c4 = 999
    c = -5
    while(c<5):
      c2 = -5
      while(c2<5):
        self.InventorySlots.append(ItemManager.ItemManager.get("ItemSlot"))
        self.InventorySlots[-1].X = c*10
        self.InventorySlots[-1].Y = c2*10
        self.InventorySlots[-1].center_x = c*10
        self.InventorySlots[-1].center_y = c2*10
        self.InventorySlots[-1].HASHID = c4
        c4 += 1
        c2 += 1
      c += 1
    
    
