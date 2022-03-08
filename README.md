# CraziKnite
Ya

YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE


**Editing Instructions:**


---Desining a level---
  -Install the Tiled Map Editor program
  -Learn how to use it
  -Every scene must have 6 layers: 3 object lists and 3 tilemaps
  Tilemaps (caps matter):
  BACKDROP
  IMMOBILE
  CLIMBABLE
  
  Objet lists (caps still matter):
  MOBILE
  NPC
  PLAYER
  
  The "Type" attribute controls the entity class
  The "DATAFILE" attribute will control the entity instance if applicable
  NPCs will be able to cross scenes without having been built into each one, so no need to manually put the same npc in 20 levels.
  
---Designing an entity---

  - Make a folder with the entity name in the "Entities" folder. Avoid weird charecters and possibly spaces.
  - Create a folder called "t" inside of the entity folder. This will hold the textures/animations. See the animations section for more information
  - Create a python file in the enity folder and name it "script.py"
  - See the example (nonexistant, refer to CraziKnite for now but ignore most of it)
  - See docs for info on commands (nonexistant, TODO)

-- Designing an item--
 - Just like an entity, but use the "Items" folder, and create a python file calles "icon.py" and copy/paste that from the example (nonexsistant, see Slashy item for now)

--- Designing an animation/texture ---

  - Open a painting program (ex: "GIMP" on linux)
  - Draw something
  - save as a png, with the name being the action it represents. Start with a capital letter, end with the frame number. (ex: "Idle1.png" for the first frame of the idle animation. a one frame animation is identical to an image, so if you aren't drawing an animation, just put a 1 at the end. See Slashy item for example.
  - Add it to the "t" folder of the entity/item it is for
- If it is for a map, ignore most of the instructions before this and save it somewhere reasonable (TODO: create a folder for map textures and tile images)
