import bge
# from bge.events import *
# from utils.keys import *

class run():
    def __init__(self, type):
        self.RUN_TYPE = type
        self.OBJECTS = {};

    def prepare(self):
        if self.RUN_TYPE == "draw":
            from engine.objects import structure as st
            from engine.render import build

            sta = st.Structure(5,"struc")
            dict = sta.get_stored()

            properties = {"timer": 10, "cont": 15 }
            draw = build.PostDraw(dict["verts"],dict["faces"], properties,"","")
            self.OBJECTS["draw"] = draw;

        if self.RUN_TYPE == "struc":
            from engine.objects import structure as st
            from engine.objects import structure_test as loader

            sta = st.Structure(4,"struc")
            sta.make_object();
            loader.init("__Main_Structure__",
                 sta.get_vectors(), [],
                 sta.get_faces(),
                 sta.get_materials())

            sta.save_structure()
            self.RUN_TYPE = "pass"
            pass

        if self.RUN_TYPE == "build":
            from engine.objects import building as st
            from engine.objects import structure_test as loader

            build = st.Building(20,"simple")
            build.generate();

            sta = build.getStructure();

            loader.init("__Main_Structure__",
                 sta.get_vectors(), [],
                 sta.get_faces(),
                 sta.get_materials()
            )

            self.RUN_TYPE = "pass";
            bge.logic.endGame();
            pass

        if self.RUN_TYPE == "teststruc":
            from engine.objects import structure as st
            from engine.objects import structure_test as loader

            sta = st.Structure(4,"test2")
            sta.make_test_object();
            loader.init("__Main_Structure__", sta.get_vectors(), [], sta.get_faces(), sta.get_materials())

            sta.save_structure()
            self.RUN_TYPE = "pass"
            pass

        if self.RUN_TYPE == "loadstruc":
            from engine.objects import structure as st
            from engine.objects import structure_test as loader

            sta = st.Structure(5,"test2")
            sta.get_stored()

            # gl backface culling
            # blender colision
            # to whatch

            loader.init("__Main_Structure__", sta.VERTICES, [], sta.FACES, [])
            self.RUN_TYPE = "pass"

    def show(self):
        if self.RUN_TYPE == "draw":
            self.OBJECTS["draw"].use(bge.logic.getCurrentScene())
            pass

        if self.RUN_TYPE == "render":
            from engine.render import render_basic as rb
            rb.load();
            pass

        if self.RUN_TYPE == "game":
            print("runing")
            pass
