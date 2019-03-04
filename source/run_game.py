import sys, os, bpy, imp

directory = os.path.dirname(bpy.data.filepath)
scripts = os.path.join(directory, "code")
if scripts not in sys.path:
   sys.path.append(scripts) #adding scripts to syspath

from hud import game_menu as gm
import bge

PAUSE = 0;
RUN_TYPE = 1;
STARTED = False;
gm.menu();

def run():
    global PAUSE
    global RUN_TYPE

    if RUN_TYPE == 0:

        pass
    elif RUN_TYPE == 1:

        pass

def start_functions():
    global STARTED

    gm.menu();
    pass
