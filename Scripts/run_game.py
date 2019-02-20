import sys, os, bpy

directory = os.path.dirname(bpy.data.filepath)
appends = [
os.path.join(directory, "Scripts","Movement","player_movement.py"),
os.path.join(directory, "Scripts","maiutils.py")
]

for appends in file:
    if file not in sys.path:
       sys.path.append(file)

import player_movement
imp.reload(player_movement)

from bge import logic as L

scene = L.getCurrentScene()
SO = scene.objects;

cube = SO["Cube"];
PAUSE = 0;

RUN_TYPE = 0;

def run():
    global PAUSE

    if RUN_TYPE = 0:
        load_defaults()
    elif RUN_TYPE = 1:
        load_menu()


def load_defaults():
    pass

def load_menu():
    pass
