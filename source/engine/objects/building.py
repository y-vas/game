from engine.objects.structure import *

class Building(object):
    def __init__(self, height, type):
        self.HEIGHT = height
        self.TYPE = type
        self.STRUCTURE = Structure(20,"house");

    def generate(self):
        struc = self.STRUCTURE;
        struc.STRUC_HEIGHT = self.HEIGHT
        struc.set_plane_structure();
        struc.set_structure_extrusion(False);

        struc.add_material('gen', (0.749,0.5725,0.392), (1.0,1.0,1), 1.0);
        struc.add_material('blu', (0,0,1), (0.5,0.5,0), 0.5 );

        newFaces = []
        for face in struc.FACES:
            verts = struc.get_verts_from_face(face);

            if struc.enters_in_face(face)

            str = Structure(0.9, struc.get_xid("H"));
            str.set_simple_cercle(90);

            newv = struc.get_center_face(verts)
            quat_diff = struc.get_quat_face(verts)

            str.set_orientation(0, 0, 45)
            str.set_plane_struct_orient(quat_diff)
            str.set_plane_struct_pos(newv)

            str.delimite_structure_in_face(verts)
            str.STRUC_HEIGHT = 0.1
            str.set_structure_extrusion(False);

            newFaces.append(str)

        for fa in newFaces:
            struc.append_vectors(fa.get_structural_vectors())
            struc.append_faces_in_material(1,fa.get_faces_ids())
            struc.append_faces(fa.get_structural_faces())
        pass

    def getStructure(self):
        return self.STRUCTURE;
