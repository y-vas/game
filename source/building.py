from vertex_gen import Structure as gen
import object_generation as obj_gen

def generateStruc():
    print("------------------------------------------ New Structure ------------------------------------------")

    ut.reloadTexts()
    ut.delete_objects_from_layer(0)

    # sta = gen.Structure(5,"struc")
    # sta.make_object();

    obj_gen.init("__Main_Structure__",
         sta.get_vectors(),
         [],
         sta.get_faces(),
         sta.get_materials()
        )

    # sta2 = sta.get_delimiters_as_areas();
    # init(sta2[0],sta2[1],sta2[2],sta2[3])

class Building(object):
    """docstring for Building."""
    def __init__(self, height):
        super(Building, self).__init__()
        self.HEIGHT = height

        sta = Structure(5,"struc");

generateStruc();


# import bpy
# import structured_face as struc
#
# for o in bpy.data.objects:
#     bpy.data.objects.remove(o,True)
#
# def init(verts, edges, faces ,strna):
#     my_mesh = bpy.data.meshes.new(name=strna)
#     my_obj = bpy.data.objects.new(strna, my_mesh)
#     my_obj.location = location=(0, 0, 0)
#     bpy.context.scene.objects.link(my_obj)
#     my_mesh.from_pydata(verts,edges,faces)
#     my_mesh.update(calc_edges = True)
#
# print("-----------------------------------------------")
#
# sta = struc.randomStructure(5,"struc")
# sta.startTestHole();
# init(sta.VERTICES,sta.EDGES,sta.FACES,"struc")

# sta2 = sta.getDelimitersAsArea();
# init(sta2[0],sta2[1],sta2[2],sta2[3])
