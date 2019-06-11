import bge, bpy
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

            sta = st.Structure(5,"test2")
            sta.get_stored()

            # gl backface culling
            # blender colision
            # to whatch

            loader.init("__Main_Structure__", sta.VERTICES, [], sta.FACES, [])
            self.RUN_TYPE = "pass"

        if self.RUN_TYPE == "bge":
            from engine.objects import structure as st
            from engine.objects import structure_test as loader

            sta = st.Structure(12,"test")
            sta.set_plane_structure();
            loader.init("x1", sta.get_vectors(), [], sta.get_faces(), sta.get_materials());

            obj = bpy.data.objects["x1"]

            obj.select = True;
            bpy.context.scene.objects.active = obj;
            bpy.ops.object.editmode_toggle()

            bpy.ops.mesh.extrude_region_move(
                MESH_OT_extrude_region={"mirror":False},
                TRANSFORM_OT_translate={"value":(0, 0, 5),
                "constraint_axis":( False,  False,  True),
                "constraint_orientation":'NORMAL', "mirror":False,
                "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH',
                "proportional_size": 1, "snap": False, "snap_target":'CLOSEST',
                "snap_point":(0, 0, 0), "snap_align": False, "snap_normal":(0, 0, 0),
                "gpencil_strokes": False, "texture_space": False, "remove_on_cancel":False,
                "release_confirm": False, "use_accurate": False }
            );

            bpy.context.area.type = "VIEW_3D";

            bpy.ops.mesh.loopcut_slide( MESH_OT_loopcut={
                "number_cuts":1, "smoothness": 0, "falloff":'INVERSE_SQUARE',
                "edge_index":33, "mesh_select_mode_init": ( True, False, False )},
                TRANSFORM_OT_edge_slide = { "value":0, "single_side":False, "use_even":False,
                "flipped":False, "use_clamp":True, "mirror":False, "snap": False,
                "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False,
                "snap_normal":(0, 0, 0), "correct_uv":False, "release_confirm":False,
                "use_accurate": False }
            );

            bge.logic.endGame();


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
