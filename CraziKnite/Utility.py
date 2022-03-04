import random
def Damage(Entity,DmgVector,Modifier,Type = "Normal"):
    if(Entity.HP):
        if(Entity.AC):
            roll = random.randint(1,20)
            if(roll+Modifier>Entity.AC):
                c = 0
                while(c<DmgVector[0]):
                    Dmg += random.randint(1,DmgVector[1])
                    c += 1
                Dmg += DmgVector[2]
                if(roll == 20):
                    Dmg = Dmg*2
                if(Entity.Resistances):
                    if(Type in Entity.Resistances):
                        Dmg = Dmg*0.5
                if(Entity.Immunities):
                    if(Type in Entity.Immunities):
                        Dmg = 0
                Entity.HP -= Dmg
        else:
            c = 0
            while(c<DmgVector[0]):
                Dmg += random.randint(1,DmgVector[1])
                c += 1
            Dmg += DmgVector[2]
            if(Entity.Resistances):
                if(Type in Entity.Resistances):
                    Dmg = Dmg*0.5
            if(Entity.Immunities):
                if(Type in Entity.Immunities):
                    Dmg = 0
            Entity.HP -= Dmg
            
