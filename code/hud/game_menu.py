from imports.obj_gen import vert_gen
from bge import logic
from bge import events
from mathutils import Vector
import bpy
import copy



def menu():
    scene = logic.getCurrentScene()
    objects = scene.objects;

    print(logic.getCurrentScene().objects)
    vects = vert_gen.generateStruc()

    print(bpy.data.meshes[5])

    # obje = objects[0]
    # objects.append("dfasdf")

    scene.addObject('Cube', objects[0])

    scene.objects["Cube"].worldOrientation = [1,5,0]
    scene.objects["Cube"].meshes
    mesh = scene.objects["Cube"].meshes[0];

    print(dir(scene.objects["Cube"].meshes[0]))
    print(objects)


    mesh.transform(1)
    # bpy.context.scene.objects.link(my_obj)




    pass



    # camera = L.getCurrentScene().active_camera
    #
    # # A sphere of radius 4.0 located at [x, y, z] = [1.0, 1.0, 1.0]
    # if (camera.sphereInsideFrustum([1.0, 1.0, 1.0], 4) != camera.OUTSIDE):
    # print("dfasdf")
