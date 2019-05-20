import sys, os, bpy, imp, bge

## adding scripts to syspath
directory = os.path.dirname(bpy.data.filepath)
scripts = os.path.join(directory, "source")
if scripts not in sys.path:
   sys.path.append(scripts)


# from hud import game_menu as gm

PAUSE = 0;
RUN_TYPE = 1;
# STARTED = False;
# gm.menu();

def run():
    global PAUSE
    global RUN_TYPE

    if RUN_TYPE == 0:
        pass
    elif RUN_TYPE == 1:
        pass

def start_functions():
    global STARTED
    # gm.menu();
    pass



# def start_game():
# 	load_map()
# 	load_prefabrics()
# 	load_defaults()
#
# def load_map():
# 	sql = SQL()
# 	facec = sql.query("SELECT * FROM faces where distance = ").copy()
# 	for vc in faces:
# 		vtc = sql.query("select * from vertices where id = "+str(vc))
