import sys, os, bpy

# adding scripts to syspath
scripts = os.path.join(os.path.dirname(bpy.data.filepath), "source")
if scripts not in sys.path:
   sys.path.append(scripts)

from engine.controller import run

view = run("movement");

def start():
    view.show();
    pass
