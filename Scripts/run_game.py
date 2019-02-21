import sys, os, bpy, imp


directory = os.path.dirname(bpy.data.filepath)
appends = [
[os.path.join(directory, "Scripts","Movement","player_movement.py"), True],
[os.path.join(directory, "Scripts","HUD","game_menu.py"), True],
[os.path.join(directory, "Scripts","maiutils.py"), False]
]

sources = []
for file in appends:
    if file[1] == True:
        print("importing: "+file[0])
        sources.append(imp.load_source('', file[0]))

game_playng = sources[0];
game_menu = sources[1];

from bge import logic as L
from bge import events

scene = L.getCurrentScene()
SO = scene.objects;

cube = SO["Cube"];

PAUSE = 0;

RUN_TYPE = 1;

def run():
    global PAUSE
    global RUN_TYPE

    if RUN_TYPE == 0:
        game_playng.testdef()
    elif RUN_TYPE == 1:
        # game_menu.testdef();

        print(L.keyboard.events)
