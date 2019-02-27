import sys, os, bpy, imp

directory = os.path.dirname(bpy.data.filepath)
scripts = os.path.join(directory, "code")
if scripts not in sys.path:
   sys.path.append(scripts) #adding scripts to syspath

from hud import game_menu as gm
from bge import logic as L
from bge import events

L.addScene("Hud",1)

scene = L.getCurrentScene()
SO = scene.objects;
cube = SO["Cube"];

PAUSE = 0;

RUN_TYPE = 1;

gm.menu();

def run():
    global PAUSE
    global RUN_TYPE

    if RUN_TYPE == 0:
        # game_playng.testdef()
        pass
    elif RUN_TYPE == 1:
        # print(L.getSceneList()[1])
        pass
