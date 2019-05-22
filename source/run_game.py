import sys, os, bpy, bge

## adding scripts to syspath
directory = os.path.dirname(bpy.data.filepath)
if scripts not in sys.path:
   sys.path.append(os.path.join(directory, "source"))



class run(object):
    def __init__(self):
        super(RUN, self).__init__()
        self.RUN_TYPE = "pass"
        self.OBJECTS = {}

    def run(self):
        if self.RUN_TYPE == "pass":
            print("runing")
            pass

        if self.RUN_TYPE == "struc":
            from engine.objects import structure as st
            from engine.objects import structure_test as loader

            sta = st.Structure(5,"struc")
            sta.make_object();
            loader.init("__Main_Structure__",
                 sta.get_vectors(), [],
                 sta.get_faces(),
                 sta.get_materials()
                )
            sta.save_structure()
            self.RUN_TYPE = "pass"
            pass

        if self.RUN_TYPE == "render":
            from engine.render import render_basic as rb
            rb.load();
            pass

        if self.RUN_TYPE == "makedraw":
            from engine.objects import structure as st
            from engine.render import build

            sta = st.Structure(5,"struc")
            vals = sta.get_stored("struc")

            properties = {"timer": 10, "cont": 15 }

            draw = build.PostDraw(vals["verts"],vals["faces"], properties,"","")
            self.OBJECTS["draw"] = draw;
            self.RUN_TYPE = "draw"

            pass

        if self.RUN_TYPE == "draw":
            self.OBJECTS["draw"].use(bge.logic.getCurrentScene())
            pass

    def loader(self):
        pass
