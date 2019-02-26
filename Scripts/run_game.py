import sys, os, bpy, imp


directory = os.path.dirname(bpy.data.filepath)

game_menu = imp.load_source('', os.path.join(directory, "Scripts","HUD","game_menu.py") );

from bge import logic as L
from bge import events

L.addScene("Hud",1)

scene = L.getCurrentScene()

HUD = L.getSceneList()

SO = scene.objects;

cube = SO["Cube"];

PAUSE = 0;

RUN_TYPE = 1;

def run():
    global PAUSE
    global RUN_TYPE

    if RUN_TYPE == 0:
        # game_playng.testdef()
        pass
    elif RUN_TYPE == 1:
        print(L.getSceneList()[1])

        # game_menu.menu(L.getCurrentScene().active_camera);
