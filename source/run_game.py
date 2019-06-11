import sys, os, bpy

# adding scripts to syspath
directory = os.path.dirname(bpy.data.filepath)
scripts = os.path.join(directory, "source")
if scripts not in sys.path:
   sys.path.append(scripts)

from engine.controller import run

view = run("bge");
view.prepare();

def start():
    view.show();
