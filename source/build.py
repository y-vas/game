# import bpy
# import structured_face as struc
#
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
#
# sta2 = sta.getDelimitersAsArea();
# init(sta2[0],sta2[1],sta2[2],sta2[3])
