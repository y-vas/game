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
