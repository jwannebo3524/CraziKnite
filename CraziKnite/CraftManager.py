import ItemManager
import arcade
import InventoryManager
from copy import deepcopy
class CraftAttributes:
  def __init__(self,Name):
    self.Craftable = True
    self.TimeFactor = 0.1
    self.Components = []
    self.Qualitative = []
    self.Quantitative = []
    self.Additive = []
    self.Type = Name
    
class CraftManager:
  def Combine(Object1,Object2): #object1 into object2
    if (not (Object1.Craft.Craftable and Object2.Craft.Craftable)):
      return
    x = deepcopy(Object2)
    c = 0
    while(c<len(Object1.Craft.Qualitative)):
      z = Object1.Craft.Qualitative[c]
      setattr(x,z,getattr(Object1,z))
      c += 1
    c = 0
    while(c<len(Object1.Craft.Quantitative)):
      z = Object1.Craft.Quantitative[c]
      if(getattr(x,z)):
        setattr(x,z,getattr(x,z)+getattr(Object1,z))
      else:
        setattr(x,z,getattr(Object1,z))
      c += 1
    c = 0
    while(c<len(Object1.Craft.Additive)):
      z = Object1.Craft.Additive
      if(getattr(x,z)):
        y = getattr(x,z)
        y2 = getattr(Object1,z)
        c2 = 0
        while(c2<len(y2)):
          y.append(y2)
          c2 += 1
        setattr(x,z,y)
      c += 1
    if(Object1.Name): #FIXTHIS
      par = " ".split(Object1.Name)
      mod = " ".join(par[:-1])
      x.Name.append(mod)
    x.GAMEFILEID.append(Object1.GAMEFILEID)
    
    

