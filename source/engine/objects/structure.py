import mathutils ,random ,math
import mainutils as ut
from random import randint
from mathutils import Vector, Euler ,Matrix

# def generateStruc():
#     print("----------------------------------- New Structure ------------------------------------------");
#     # ut.reloadTexts()
#     # ut.delete_objects_from_layer(0)
#     # sta = Structure(5,"struc")
#     sta = Structure(5,"struc")
#     sta.make_object();
#     obj_gen.init("__Main_Structure__",
#          sta.get_vectors(),
#          [],
#          sta.get_faces(),
#          sta.get_materials()
#         )
#
#     # return sta.get_vectors()
#     # sta = ut.import_image();
#     # obj_gen.init("__Main_Structure__",
#     #      sta[0],
#     #      [],
#     #      sta[1],
#     #      []
#     #     )
#     # for x in sta[1]:
#         # pass
#     # ser = ut.sql_insert("INSERT INTO _type (tp_type, tp_def) VALUES (15,'test')")
#     # print(ser)
#     # data = ut.sql_query("SELECT tp_type FROM _type ;")
#     # print(data)
#     # sta2 = sta.get_delimiters_as_areas();
#     # init(sta2[0],sta2[1],sta2[2],sta2[3])

class Structure():
    def __init__(self, size = 5, name = "build"):
        self.NAME = name;
        self.START_POINTS = 20;
        self.VERTICES = [];      # [Vector(x,y,z), id ]
        self.FACES = [];         # [[id1, id2..] , id ]
        self.MATERIALS = [];     # [mat.., [fid, fid2]]
        self.DELIMITERS = [];
        self.NORMALIZED_ANGLES = 60
        self.SIZE = size
        self.STRUC_HEIGHT = 2
        self.IDS = 0;

    def save_structure(self):
        name = self.NAME
        i = 1;
        while len(ut.sql_query("SELECT name FROM structures WHERE name ="+name)) > 0:
            name = self.NAME+"_"+i;

        id = ut.sql_insert("INSERT INTO structures (name) VALUES ("+name+")");
        for face in self.FACES:
            verts = self.get_verts_from_face(face);
            face_verts = []
            for vert in verts:
                v = ut.sql_query("SELECT id FROM vertices WHERE x ="+vert.x+" y="+vert.y+" z ="+vert.z);
                # reuse the vertices to save posible space
                if len(v) > 0:
                    face_verts.append(v["id"]);
                    continue;

                vid = ut.sql_insert("INSERT INTO vertices (x,y,x) VALUES ("+vert.x+","+vert.y+","+vert.z+")");
                face_verts.append(vid);

                pass
            # need to convert face_vert into string to catch them better
            id = ut.sql_insert("INSERT INTO faces (verts,id_structure) VALUES ("+face_vers+","+id+")");
            pass
        pass

    def get_stored(self,name):
        structure = ut.sql_query("SELECT id FROM structures WHERE name = "+name)

        if structure == None :
            print("This object do not exist in your database!!");
            return None;

        stored_verts = stored_faces = [];

        faces = ut.sql_query("SELECT verts FROM faces WHERE id_structure = "+structure["id"])
        for face in faces:
            stored_face = []
            for vert in face["verts"].split(","):
                v = ut.sql_query("SELECT * FROM vertices WHERE id = "+vert)

                vert_pos = len(stored_verts);
                v = Vector((v["z"],v["y"],v["z"]));

                if v in stored_verts:
                    vert_pos = stored_verts.index(v)
                    stored_face.append(vert_pos);
                    continue;

                stored_verts.append(v);
                stored_face.append(vert_pos);
                pass

            if len(stored_face) < 3:
                print("A stored face doesn't all the needet vertices!!");
                continue;

            # triangulation // could be useful
            # if traingulated and len(stored_face) != 3:
            #     for v in stored_face:
            #
            #         pass

            stored_faces.append(stored_face);

        dict = {
        "faces" : stored_faces,
        "verts" : stored_verts
        }

        return dict

    def render_object():
        pass

    def make_object(self):
        self.set_plane_structure();
        self.set_simple_cercle(72);
        self.set_structure_extrusion(False);

        self.add_material('gen', (0.749,0.5725,0.392), (1.0,1.0,1), 1.0)
        self.add_material('blu', (0,0,1), (0.5,0.5,0), 0.5)
        # self.add_multipe_holes_in_face(self.FACES[3],0.7,1,8,0,0)

        newFaces = []
        for face in self.FACES:
            newFaces.append(self.add_hole_in_face(face,0.9))

        # newFaces.append(self.add_hole_in_face(self.FACES[2],2))
        for fa in newFaces:
            self.append_vectors(fa.get_structural_vectors())
            self.append_faces_in_material(1,fa.get_faces_ids())
            self.append_faces(fa.get_structural_faces())

        # self.save_structure();


    def add_multipe_holes_in_face(self,face,size, holsx, holsy, hx, hy):
        verts = self.get_verts_from_face(face)
        radi = ut.get_max_radius_in_vertices(verts)
        newv = ut.get_center_of_polygon(verts)
        normal = mathutils.geometry.normal(*verts)
        quat_diff = normal.to_track_quat('Z','X').to_euler()
        for x in range(holsx):
            for y in range(holsy):
                str = Structure(size/1.5,self.get_xid("H"));
                str.set_simple_cercle(90);
                str.set_plane_struct_orient(Euler((0, 0, math.radians(45)), 'XYZ'))
                # vc = Vector((-((holsx*size)/2)+x*size+size/2+hx,-((holsy*size)/2)+y*size+size/2,0+hy))
                # str.set_plane_struct_pos(vc);
                str.set_plane_struct_orient(quat_diff)
                str.delimite_structure_in_face(verts)
                str.set_plane_struct_pos(newv);
                self.append_vectors(str.get_structural_vectors())
                self.append_faces_in_material(1,str.get_faces_ids())
                self.append_faces(str.get_structural_faces())
            pass
        pass


    def add_hole_in_face(self, face, rad):
        verts = self.get_verts_from_face(face)
        str = Structure(rad,self.get_xid("H"));
        str.set_simple_cercle(90);

        newv = ut.get_center_of_polygon(verts)
        normal = mathutils.geometry.normal(*verts)
        quat_diff = normal.to_track_quat('Z','X').to_euler()

        str.set_plane_struct_orient(quat_diff)
        str.set_plane_struct_pos(newv)

        str.delimite_structure_in_face(verts)
        # str.STRUC_HEIGHT = 0.01
        str.set_structure_extrusion(False);

        return str


    def delimite_structure_in_face(self, v_delim):
        verts = self.get_vectors()

        # radi_d = ut.get_max_radius_in_vertices(v_delim)
        # radi_s = ut.get_max_radius_in_vertices(verts)
        # if radi_s > radi_d:

        if ut.is_face_in_face(verts,v_delim) == False:
            self.clean_structure()
            return

        intersectons = ut.get_points_where_edges_intersect_form_faces(verts,v_delim)
        if len(intersectons) == 0:
            return

        p1 = ut.get_points_that_are_in_delited_area(v_delim,verts)
        p2 = ut.get_points_that_are_in_delited_area(verts,v_delim)

        self.clean_structure()
        self.add_vertices(intersectons); self.add_vertices(p1); self.add_vertices(p2)

        center = ut.get_center_of_polygon(verts)
        vec = self.get_vector(0);

        print(self.VERTICES)
        print("---------")
        for i, value in enumerate(self.VERTICES):
            angle = ut.angles_of_a_triangle(center, vec ,value[0]);

            # print(i)
            print(angle)
            print(value)

            # v = Vector((value[0][0],value[0][1],value[0][2]))
            # eul = v.to_track_quat('-Z','Y').to_euler()
            # v2 = Vector((eul[0],eul[1],eul[2]))
            # value[0] = v2

            # https://forum.unity.com/threads/how-to-get-a-360-degree-vector3-angle.42145/
            value.append( angle )

        self.VERTICES.sort(key = ut.sort_by_angle)

        for value in self.VERTICES:
            value.pop(2)

        face = []
        for x in self.VERTICES:
            face.append(x[1])

        self.FACES = [[face,self.get_search_id()]]



    def get_verts_from_face(self, face):
        verts = []
        for id in face[0]:
            for ve in self.VERTICES:
                if ve[1] == id:
                    verts.append(ve[0])
        return verts

    def get_verts_from_face_id(self, id):
        face = self.FACES[id]
        verts = []
        for id in face[0]:
            for ve in self.VERTICES:
                if ve[1] == id:
                    verts.append(ve[0])
        return verts

    def get_verts_and_id_from_face(self, face):
        verts = []
        for id in face:
            for ve in self.VERTICES:
                if ve[1] == id:
                    verts.append(ve)
        return verts

    def set_plane_struct_pos(self,position):
        for vert in self.VERTICES:
            vert[0][0] += position[0];
            vert[0][1] += position[1];
            vert[0][2] += position[2];

    def set_plane_struct_orient(self,rot):
        for x in self.VERTICES:
            x[0].rotate(rot)

    # def getInWichFaceDoorWillBe(self):
    #      v1indx = randint(0,self.START_POINTS-1);
    #      v2indx = v1indx+1;
    #
    #      vr1 = self.VERTICES[v1indx];
    #      vr2 = self.VERTICES[v2indx];
    #      vr3 = Vector((vr1[0],vr1[1],self.STRUC_HEIGHT))
    #      vr4 = Vector((vr2[0],vr2[1],self.STRUC_HEIGHT))
    #
    #      v3indx = next((i for i, e in enumerate(self.VERTICES) if e == vr3))
    #      v4indx = next((i for i, e in enumerate(self.VERTICES) if e == vr4))
    #
    #      face = [v1indx,v3indx,v4indx,v2indx] # no canviar la estructura
    #      return face

    def set_plane_structure(self):
        self.VERTICES = []
        vects = []; face = []
        for vect in range(self.START_POINTS):
            vec = self.rand_vector_out_of_structure_delimiters();
            vects.append([vec,self.get_search_id()]);
        self.VERTICES = vects;
        self.VERTICES.sort(reverse = False, key = ut.takeSecond)
        for x in self.VERTICES:
            face.append(x[1])
        self.FACES = [[face,self.get_search_id()]]

        while self.check_angles() == False:
            self.set_structure_min_angles();


    def set_structure_extrusion(self, normal = False):
        vertes = self.get_verts_from_face_id(0)
        normalVec = mathutils.geometry.normal(*vertes)

        inverse = -1;
        if normal == True: inverse  = 1;
        inverse = inverse*self.STRUC_HEIGHT
        verts = []; face = [];

        for i,e in enumerate(self.VERTICES):
            vect = self.VERTICES[i][0]
            vct = Vector((vect[0]+(normalVec[0]*inverse),vect[1]+(normalVec[1]*inverse),vect[2]+(normalVec[2]*inverse)))
            idv = self.get_search_id();
            verts.append([vct,idv])
            face.append(idv)

        self.FACES.append([face, self.get_search_id()])

        for i, vec in enumerate(verts):
            if i == len(self.VERTICES)-1:
                face = [self.VERTICES[i][1],verts[i][1],verts[0][1],self.VERTICES[0][1]]
            else:
                face = [self.VERTICES[i][1],verts[i][1],verts[i+1][1],self.VERTICES[i+1][1]]
            self.FACES.append([face, self.get_search_id()])

        self.append_vectors(verts)

    def set_random_delimiters(self):
        spaces = []; siz = self.DELIMITERS_RADIUS
        for p in range(self.START_POINTS):
            if p % self.DELIMITERS_DIVIDER == 0:
                radius = randint(self.DELIMITERS_RADIUS/2*100,self.DELIMITERS_RADIUS*100)/100
                spaces.append([ut.randVect3D(siz,siz,0),radius])
        self.DELIMITERS = spaces

    def rand_vector_out_of_structure_delimiters(self):
        badVert = True; trys = 0
        while badVert == True:
            vec = ut.randVect3D(self.SIZE,self.SIZE,0);
            trys += 1
            if trys > 100: return vec
            if badVert == self.is_vector_in_delimiters(vec):
                return vec

    def rand_vector_out_of_structure_delimiters3D(self):
        badVert = True; trys = 0
        while badVert == True:
            vec = ut.randVect3D(self.SIZE,self.SIZE,self.SIZE);
            trys += 1
            if trys > 100: return vec
            if badVert == self.is_vector_in_delimiters(vec):
                return vec


    def is_vector_in_delimiters(self, vector):
        for d in self.DELIMITERS:
            if ut.distanceBetwenVectors(d[0],vector) < d[1]:
                return True;
        return False

    def set_structure_min_angles(self):
        for i in range(len(self.VERTICES)):
            if i == 0: continue;
            b = i-1; c = i +1;
            if c == len(self.VERTICES): c = 0;
            ve1 = self.VERTICES[i][0]
            ve2 = self.VERTICES[b][0]
            ve3 = self.VERTICES[c][0]
            if ut.angleTriangleBetwenVectors(ve1,ve2,ve3) < self.NORMALIZED_ANGLES:
                self.remove_vector_index(i)
                break


    def remove_vector_index(self, indexVector):
        id = self.VERTICES[indexVector][1]
        del self.VERTICES[indexVector]
        for face in self.FACES:
            for i,e in enumerate(face):
                if e == id:
                    del face[i]

    def remove_vector_id(self, id):
        for n, v in enumerate(self.VERTICES):
            if v[1] == id: self.VERTICES.remove(n)

        for n,face in enumerate(self.FACES):
            for i in face:
                if i > id: self.FACES[n].remove(id);

    def remove_vector(self, vector):
        id = ""
        for n, v in enumerate(self.VERTICES):
            if v == vector:
                id = self.VERTICES[n][1]
                self.VERTICES.remove(n)

        for n,face in enumerate(self.FACES):
            for i in face:
                if i > id: self.FACES[n].remove(id);

    def check_angles(self):
        if len(self.VERTICES) == 5:
            return True
        for index in range(len(self.VERTICES)):
            if index != 0:
                c = 0; b = index-1; c = index +1;
                if c == len(self.VERTICES): c = 0;
                ve2 = self.VERTICES[b][0]
                ve3 = self.VERTICES[c][0]
                ang = ut.angleTriangleBetwenVectors(self.VERTICES[index][0],ve2,ve3);
                if ang < self.NORMALIZED_ANGLES:
                    return False
        return True

    def get_delimiters_as_areas(self):
        vectors = []; faces = []; edges = []
        verts = 0
        for space in self.DELIMITERS:
            delimiter_vector = space[0]
            radius = space[1]
            face = []; radi = 0;
            while radi < 360:
                radi += 1
                if radi % 24 == 0:
                    vec = Vector((0, radius,0))
                    vec.rotate(Euler((0.0, 0, math.radians(radi)), 'XYZ'))
                    vecF = Vector((vec[0]+delimiter_vector[0], vec[1]+delimiter_vector[1], vec[2]+delimiter_vector[2]))
                    vectors.append(vecF)
                    face.append(verts)
                    verts += 1
            faces.append(face)
        struct = [vectors,edges,faces,self.NAME+"_Delimiters"]
        return struct

    def get_vectors(self):
        vert = []
        for x in self.VERTICES:
            vert.append(x[0])
        return vert

    def get_faces(self):
        faces = []
        for face in self.FACES:
            aface = []
            for id in face[0]:
                for i, ve in enumerate(self.VERTICES):
                    if id == ve[1]:
                        aface.append(i)
            faces.append(aface)
        return faces

    def get_faces_ids(self):
        faces = []
        for face in self.FACES:
            faces.append(face[1])
        return faces

    def add_vertices(self, vertices):
        for v in vertices:
            self.VERTICES.append([v,self.get_search_id()])

    def get_structural_vectors(self):
        return self.VERTICES

    def get_vector(self, index):
        return self.VERTICES[index][0]

    def get_structural_faces(self):
        return self.FACES

    def append_vectors(self,vectors):
        for value in vectors:
            self.VERTICES.append(value)

    def append_faces(self,faces):
        for face in faces:
            self.FACES.append(face)

    def set_simple_cercle(self, divider ):
        self.clean_structure()
        face = [];

        radi = 360;
        while radi > 0:
            radi -= 1
            if radi % divider == 0:
                vec = Vector((0, self.SIZE,0))
                vec.rotate(Euler((0.0, 0, math.radians(radi)), 'XYZ'))
                id = self.get_search_id();
                self.VERTICES.append([vec,id])
                face.append(id)

        self.FACES.append([face,self.get_search_id()])

        # if divider == 90:
        #     self.set_plane_struct_orient(Euler((0, 0, math.radians(45)), 'XYZ'))



    def set_structure_from_image(self):
        ret = ut.import_image("heightmap.jpg")
        self.VERTICES = ret[0]
        self.FACES = ret[1]

    def clean_structure(self):
        self.VERTICES = []
        self.FACES = []
        self.EDGES = []

    def get_search_id(self):
        self.IDS += 1
        return self.NAME+"_ID"+str(self.IDS)

    def get_xid(self, tip):
        self.IDS += 1
        return tip+str(self.IDS)


    def add_material(self ,name, diffuse, specular, alpha):
        import bpy
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = diffuse
        mat.diffuse_shader = 'LAMBERT'
        mat.diffuse_intensity = 1.0
        mat.specular_color = specular
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.5
        mat.alpha = alpha
        mat.ambient = 1
        self.MATERIALS.append([mat,[]])

    def append_faces_in_material(self, mat, faces):
        for f in faces:
            self.MATERIALS[mat][1].append(f)


    def get_materials(self):
        mates = []
        for value in self.MATERIALS:
            facesmat = []
            for f in value[1]:
                for i,x in enumerate(self.FACES):
                    if x[1] == f:
                        facesmat.append(i)
            mates.append([value[0],facesmat])

        return mates
