import bge

class run():
    def __init__(self, type):
        super(run, self).__init__()
        self.RUN_TYPE = type
        self.OBJECTS = {}

        if self.RUN_TYPE == "draw":
            from engine.objects import structure as st
            from engine.render import build

            sta = st.Structure(5,"struc")
            vals = sta.get_stored("struc")

            properties = {"timer": 10, "cont": 15 }

            draw = build.PostDraw(vals["verts"],vals["faces"], properties,"","")
            self.OBJECTS["draw"] = draw;

            pass

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

        if self.RUN_TYPE == "teststruc":
            from engine.objects import structure as st
            from engine.objects import structure_test as loader

            sta = st.Structure(4,"test")
            sta.make_test_object();
            loader.init("__Main_Structure__",
                 sta.get_vectors(), [],
                 sta.get_faces(),
                 sta.get_materials())

            sta.save_structure()
            self.RUN_TYPE = "pass"
            pass

        if self.RUN_TYPE == "loadstruc":
            from engine.objects import structure as st
            from engine.objects import structure_test as loader

            sta = st.Structure(5,"test")
            dict = sta.get_stored()

            loader.init("__Main_Structure__",
                 dict["verts"], [],
                 dict["faces"], [])

            self.RUN_TYPE = "pass"

        if self.RUN_TYPE == "movement":
            import sys
            bge.logic.LibLoad(sys.path[0]+'/source/data/move.blend', 'Scene')


    def show(self):
        if self.RUN_TYPE == "movement":
            cube = bge.logic.getCurrentScene().objects['cube']
            cube.applyRotation((0 , 0, 0.01))

        if self.RUN_TYPE == "draw":
            self.OBJECTS["draw"].use(bge.logic.getCurrentScene())
            pass

        if self.RUN_TYPE == "render":
            from engine.render import render_basic as rb
            rb.load();
            pass
