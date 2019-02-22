import bpy


def init(strna ,verts, edges, faces, mats):
    my_mesh = bpy.data.meshes.new(name=strna)
    my_mesh.from_pydata(verts,edges,faces)
    my_mesh.update(calc_edges = True)

    my_obj = bpy.data.objects.new(strna, my_mesh)
    my_obj.location = location=(0, 0, 0)

    for inx,value in enumerate(mats):
        my_obj.data.materials.append(value[0])
        apply_polygons(my_obj,value[1],inx)

    bpy.context.scene.objects.link(my_obj)



def apply_polygons(obj,faces, inx):
    for f in faces:
        obj.data.polygons[f].material_index = inx
