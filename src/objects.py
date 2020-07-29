import math
import mainutils as ut
from mathutils import Euler ,Matrix
from mathutils import Vector as vtr
from mathutils.geometry import intersect_line_line_2d
from mathutils.geometry import intersect_line_line

class Object():
    def __init__(self, size = 5, points = 30):
        self.size   = size
        self.points = points
        self.verts = []
        self.edges = []
        self.colors= []

    def cercle(self):
        for i in range( 0 , self.points ):
            theta = 2.0 * math.pi * float(i) / float( self.points )
            x = self.size * math.cos(theta)
            y = self.size * math.sin(theta)
            self.verts.append((x, y, 0))

        for i ,e in enumerate(self.verts):
            if i is 0:
                self.edges.append((len(self.verts) -1 , 0 ))
                continue
            self.edges.append(( i-1 , i))

        self.obicex((0,0,0))

        self.colors = tuple([ (1,0,0) for x in self.verts ])

    def obicex( self, pos ):
        d = 1
        for v in self.verts:
            if ut.distance( pos, v ) > d:
                print('----------------------')





    def cut(self):
        v3 = ( 0, 0, 0 )
        v4 = ( 0, self.size * 2 , 0 )

        self.verts.append( v3 )
        self.verts.append( v4 )

        vl = len( self.verts )

        # self.edges.append( (vl-2,vl-1))

        everts = []

        # print(v3,v4)
        for edge in self.edges:
            # print(edge)

            v1 = self.verts[edge[0]]
            v2 = self.verts[edge[1]]

            print('-' * 20)
            print( v1, v2 )
            ins = intersect_line_line_2d(v1,v2,v3,v4)

            if ins != None:
                everts.append( ( ins.x, ins.y , 0) )


        for x in everts:
            self.verts.append(x)

            vs = len( self.verts ) - 1
            print(self.verts[vs])
            print(self.verts[vl-2])
            print(x)

            self.edges.append( ( vl-2, vs ) )

    def plane(self,strech=None,type=1):
        self.verts = []
        if strech != None: self.delimiters = [ [ vtr((0,0,0)),strech ] ]
        vects, face = [], []

        half = int(self.points / 2)
        v1 = self.rvec(z=0,zd=False,delimited=False);
        vects.append([v1,self.sid()])

        for vect in range( half - 1 ):
            vn = self.rvec( z=0, zd=False, delimited=False )
            vec = vn + vects[-1][0]

            for i,vk in enumerate(vects):
                if i == 0:
                    continue

                if intersect_line_line(vk[0],vects[i-1][0],vects[-1][0],vec):
                    bad = True
                    break

            vn = self.rvec(z=0,zd=False,delimited=False)
            vec = vn + vects[-1][0]


            vects.append([vec,self.sid()])
            pass

            self.verts = vects;
        else:
            for vect in range( self.points ):
                vec = self.rvec(z=0,zd=False);
                vects.append([vec,self.sid()]);

            self.verts = vects;
            self.verts.sort(reverse = True, key = ut.takeSecond)

        for x in self.verts:
            face.append(x[1]);

        self.FACES = [[face,self.sid()]];

        # while self.check_angles() == False:
        #     self.set_structure_min_angles();

    def save_structure(self):
        name = self.NAME;

        que = ut.sql_query("select count(*) as cont from structures where name like '"+name+"%' ")[0][0];
        if que > 0: name = self.NAME + "_" + str(que);

        id = ut.sql_insert("INSERT INTO structures (name) VALUES ('" + name + "')");
        for face in self.FACES:
            verts = self.get_verts_from_face(face);
            face_verts = ""
            for vert in verts:
                que = "SELECT id FROM vertices WHERE x ='"+str(vert.x)+"' AND y ='"+str(vert.y)+"' AND z='"+str(vert.z)+"'; ";
                v = ut.sql_query(que);
                # reuse the vertices to save posible space

                if len(v) > 0:
                    face_verts += str(v[0][0])+","
                    continue;

                vid = ut.sql_insert("INSERT INTO vertices (x,y,z) VALUES ('"+str(vert.x)+"','"+str(vert.y)+"','"+str(vert.z)+"')");
                face_verts += str(vid)+","

            # need to convert face_vert into string to catch them better
            ut.sql_insert("INSERT INTO faces (verts,id_structure) VALUES ('"+face_verts+"',"+str(id)+")");
            pass

        print(name+" : STORED")
        pass

    def get_stored(self):
        structure = ut.sql_query("SELECT id FROM structures WHERE name = '"+self.NAME+"' ;")
        if structure == None :
            print("This object does not exist in your database!!");
            return None;

        stored_verts = [];
        stored_faces = [];

        faces = ut.sql_query("SELECT verts FROM faces WHERE id_structure = '"+str(structure[0][0])+"' ")

        for face in faces:
            stored_face = []
            for vert in face[0].split(","):
                if vert == "":
                    continue;

                v = ut.sql_query("SELECT x,y,z FROM vertices WHERE id = "+vert)[0]

                vert_pos = len(stored_verts);
                v = vtr( (v[0],v[1],v[2]) );

                if v in stored_verts:
                    vert_pos = stored_verts.index(v)
                    stored_face.append(vert_pos);
                    continue;

                stored_verts.append(v);
                stored_face.append(vert_pos);
                pass

            if len(stored_face) < 3:
                print("A stored face doesn't have all the needet vertices!!");
                continue;

            stored_faces.append(stored_face);

        dict = { "faces" : stored_faces, "verts" : stored_verts }

        return dict

    def mkobj(self,strech=1):
        self.plane(strech = strech);
        # self.set_simple_cercle(72);
        # self.set_structure_extrusion(False);
        # self.add_material('gen', (0.749,0.5725,0.392), (1.0,1.0,1), 1.0);
        # self.add_material('blu', (0,0,1), (0.5,0.5,0), 0.5);
        # self.add_multipe_holes_in_face(self.FACES[3],0.7,1,8,0,0)

        # newFaces = []
        # for face in self.FACES:
        #     newFaces.append(self.add_hole_in_face(face,0.9))
        #
        # # newFaces.append(self.add_hole_in_face(self.FACES[2],2))
        # for fa in newFaces:
        #     self.append_vectors(fa.get_structural_vectors())
        #     self.append_faces_in_material(1,fa.mhf_ids())
        #     self.append_faces(fa.get_structural_faces())

    def add_multipe_holes_in_face(self,face,size, holsx, holsy, hx, hy):
        verts = self.get_verts_from_face(face)
        radi = ut.get_max_radius_in_vertices(verts)
        newv = ut.get_center_of_polygon(verts)
        normal = mathutils.geometry.normal(*verts)
        quat_diff = normal.to_track_quat('Z','X').to_euler()
        for x in range(holsx):
            for y in range(holsy):
                str = Object(size/1.5,self.get_xid("H"));
                str.set_simple_cercle(90);
                str.set_plane_struct_orient(Euler((0, 0, math.radians(45)), 'XYZ'))
                # vc = vtr((-((holsx*size)/2)+x*size+size/2+hx,-((holsy*size)/2)+y*size+size/2,0+hy))
                # str.set_plane_struct_pos(vc);
                str.set_plane_struct_orient(quat_diff)
                str.delimite_structure_in_face(verts)
                str.set_plane_struct_pos(newv);
                self.append_vectors(str.get_structural_vectors())
                self.append_faces_in_material(1,str.mhf_ids())
                self.append_faces(str.get_structural_faces())


    def add_hole_in_face(self, face, rad):
        verts = self.get_verts_from_face(face)
        str = Object(rad,self.get_xid("H"));
        str.plane();
        # str.set_simple_cercle(90);

        newv = ut.get_center_of_polygon(verts)
        normal = mathutils.geometry.normal(*verts)
        quat_diff = normal.to_track_quat('Z','X').to_euler()

        str.set_plane_struct_orient(Euler((0, 0, math.radians(45)), 'XYZ'))
        str.set_plane_struct_orient(quat_diff)
        str.set_plane_struct_pos(newv)

        str.delimite_structure_in_face(verts)
        # str.STRUC_HEIGHT = 0.01
        # str.set_structure_extrusion(False);
        return str

    def add_object_in_face(self, face, rad, height):
        verts = self.get_verts_from_face(face)
        str = Object(rad,self.get_xid("H"));
        str.set_simple_cercle(90);

        newv = ut.get_center_of_polygon(verts)
        normal = mathutils.geometry.normal(*verts)
        quat_diff = normal.to_track_quat('Z','X').to_euler()

        str.set_plane_struct_orient(Euler((0, 0, math.radians(45)), 'XYZ'))
        str.set_plane_struct_orient(quat_diff)
        str.set_plane_struct_pos(newv)

        str.delimite_structure_in_face(verts)
        str.STRUC_HEIGHT = height
        str.set_structure_extrusion(False);
        return str

    def enters_in_face(self,face,verts):
        strv = self.get_verts_from_face(face);
        if ut.is_face_in_face(strv,verts) == False:
            return False

        intersectons = ut.get_points_where_edges_intersect_form_faces(strv,verts)
        if len(intersectons) == 0:
            return False

        return True;


    def delimite_structure_in_face(self, v_delim):
        verts = self.mhv()

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

        print(self.verts)
        print("---------")
        for i, value in enumerate(self.verts):
            angle = ut.angles_of_a_triangle(center, vec ,value[0]);

            # print(angle)
            # print(value)
            #
            # v = vtr((value[0][0],value[0][1],value[0][2]))
            # eul = v.to_track_quat('-Z','Y').to_euler()
            # v2 = vtr((eul[0],eul[1],eul[2]))
            # value[0] = v2

            # https://forum.unity.com/threads/how-to-get-a-360-degree-vector3-angle.42145/
            value.append( angle )

        self.verts.sort(key = ut.sort_by_angle)

        for value in self.verts:
            value.pop(2)

        face = []
        for x in self.verts:
            face.append(x[1])

        self.FACES = [[face,self.sid()]]

    def get_verts_from_face(self, face):
        verts = []
        for id in face[0]:
            for ve in self.verts:
                if ve[1] == id:
                    verts.append(ve[0])
        return verts

    def get_verts_from_face_id(self, id):
        face = self.FACES[id]
        verts = []
        for id in face[0]:
            for ve in self.verts:
                if ve[1] == id:
                    verts.append(ve[0])
        return verts

    def get_verts_and_id_from_face(self, face):
        verts = []
        for id in face:
            for ve in self.verts:
                if ve[1] == id:
                    verts.append(ve)
        return verts

    def set_plane_struct_pos(self,position):
        for vert in self.verts:
            vert[0][0] += position[0];
            vert[0][1] += position[1];
            vert[0][2] += position[2];

    def set_plane_struct_orient(self,rot):
        for x in self.verts:
            x[0].rotate(rot)

    def set_orientation(self,x,y,z):
        rot = Euler((math.radians(x), math.radians(y), math.radians(z)), 'XYZ')
        for x in self.verts:
            x[0].rotate(rot)

    def get_center_face(self,verts):
        center = ut.get_center_of_polygon(verts)
        return center

    def get_quat_face(self,verts):
        normal = mathutils.geometry.normal(*verts)
        return normal.to_track_quat('Z','X').to_euler()


    def set_structure_extrusion(self, normal = False):
        vertes = self.get_verts_from_face_id(0)
        normalVec = mathutils.geometry.normal(*vertes)

        inverse = -1;
        if normal == True:
            inverse  = 1;

        inverse = inverse * self.STRUC_HEIGHT;

        verts = [];
        face = [];

        for i,e in enumerate(self.verts):
            vect = self.verts[i][0]

            vct = vtr((
                vect[0]+ (normalVec[0] * inverse),
                vect[1]+(normalVec[1]*inverse),
                vect[2]+(normalVec[2]*inverse))
                    )
            idv = self.sid();
            verts.append([vct,idv])
            face.append(idv)

        self.FACES.append([face, self.sid()])

        for i, vec in enumerate(verts):
            if i == len(self.verts)-1:
                face = [self.verts[i][1],verts[i][1],verts[0][1],self.verts[0][1]]
            else:
                face = [self.verts[i][1],verts[i][1],verts[i+1][1],self.verts[i+1][1]]
            self.FACES.append([face, self.sid()])

        self.append_vectors(verts)

    def set_random_delimiters(self,size,cuant, area):
        spaces = [];
        for p in range(cuant):
            radius = rint(0,area*100)/100
            spaces.append( [ ut.randVect3D(size,size,0),radius ] )

        self.delimiters = spaces

    def rvec(self,x=1,y=1,z=1,xd=True,yd=True,zd=True,delimited=True,persistance=100):
        vec = None
        min = self.size
        for vects in range(persistance):
            vx = rint(-x * 100 * min ,y * 100 * min )/100
            vy = rint(-x * 100 * min ,y * 100 * min )/100
            vz = rint(-z * 100 * min ,z * 100 * min )/100
            vec= vtr(( vx, vy, vz ))

            if not delimited: return vec
            if not self.vdelimited(vec,xd,yd,zd):
                return vec

        return vec

    def vdelimited(self,V,x=True,y=True,z=True,delimiter=[]):
        delimiters = self.delimiters if delimiter != [] else delimiter
        for d in delimiters:
            A = d[0]
            lx = 0 if not x else (V[0]-A[0])**2
            ly = 0 if not x else (V[1]-A[1])**2
            lz = 0 if not x else (V[2]-A[2])**2
            dist = math.sqrt(lx+ly+lz)
            if dist <= d[1]:
                return True;
        return False

    def set_structure_min_angles(self):
        for i in range(len(self.verts)):
            if i == 0: continue;
            b = i-1; c = i +1;
            if c == len(self.verts): c = 0;
            ve1 = self.verts[i][0]
            ve2 = self.verts[b][0]
            ve3 = self.verts[c][0]
            if ut.angleTriangleBetwenVectors(ve1,ve2,ve3) < self.NORMALIZED_ANGLES:
                self.remove_vector_index(i)
                break

    def remove_vector_index(self, indexvtr):
        id = self.verts[indexvtr][1]
        del self.verts[indexvtr]
        for face in self.FACES:
            for i,e in enumerate(face):
                if e == id:
                    del face[i]

    def remove_vector_id(self, id):
        for n, v in enumerate(self.verts):
            if v[1] == id: self.verts.remove(n)

        for n,face in enumerate(self.FACES):
            for i in face:
                if i > id: self.FACES[n].remove(id);

    def remove_vector(self, vector):
        id = ""
        for n, v in enumerate(self.verts):
            if v == vector:
                id = self.verts[n][1]
                self.verts.remove(n)

        for n,face in enumerate(self.FACES):
            for i in face:
                if i > id: self.FACES[n].remove(id);

    def check_angles(self):
        if len(self.verts) == 5:
            return True
        for index in range(len(self.verts)):
            if index != 0:
                c = 0; b = index-1; c = index +1;
                if c == len(self.verts): c = 0;
                ve2 = self.verts[b][0]
                ve3 = self.verts[c][0]
                ang = ut.angleTriangleBetwenVectors(self.verts[index][0],ve2,ve3);
                if ang < self.NORMALIZED_ANGLES:
                    return False
        return True

    def get_delimiters_as_areas(self):
        vectors = []; faces = []; edges = []
        verts = 0
        for space in self.delimiters:
            delimiter_vector = space[0]
            radius = space[1]
            face = []; radi = 0;
            while radi < 360:
                radi += 1
                if radi % 24 == 0:
                    vec = vtr((0, radius,0))
                    vec.rotate(Euler((0.0, 0, math.radians(radi)), 'XYZ'))
                    vecF = vtr((vec[0]+delimiter_vector[0], vec[1]+delimiter_vector[1], vec[2]+delimiter_vector[2]))
                    vectors.append(vecF)
                    face.append(verts)
                    verts += 1
            faces.append(face)
        struct = [vectors,edges,faces,self.NAME+"_Delimiters"]
        return struct

    def mhv(self):
        vert = []
        for x in self.verts:
            vert.append( x[0] )
        return vert

    def dfv(self):
        vert = []
        for x in self.verts:
            v = x[0]
            vert.append((v.x,v.y,v.z))
        return vert

    def dfe(self):
        fc = self.dff()

        edges = []
        for x in range(len(self.verts)):
            for f in fc:

                for i, v in enumerate(f):
                    if v == x:
                        mm = list(f+f+f)
                        del mm[i]

                        l = mm.index(v)

                        e1 = (mm[l],mm[l+1])
                        e2 = (mm[l-1],mm[l])

                        edges.append(e1)
                        edges.append(e2)

        nedges = []

        for x,y in edges:
            l ,lf= (x,y) , (y,x)
            if l not in nedges and lf not in edges: nedges.append(l)

        edges = list(set(nedges))

        return edges

    def dff(self):
        faces = []
        for face in self.FACES:
            aface = []
            for id in face[0]:
                for i, ve in enumerate(self.verts):
                    if id == ve[1]:
                        aface.append(i)
            faces.append( tuple(aface) )
        return tuple(faces)

    def mhf_ids(self):
        faces = []
        for face in self.FACES:
            faces.append(face[1])
        return faces

    def add_vertices(self, vertices):
        for v in vertices:
            self.verts.append([v,self.sid()])

    def get_structural_vectors(self):
        return self.verts

    def get_vector(self, index):
        return self.verts[index][0]

    def get_structural_faces(self):
        return self.FACES

    def append_vectors(self,vectors):
        for value in vectors:
            self.verts.append(value)

    def append_faces(self,faces):
        for face in faces:
            self.FACES.append(face)

    def set_structure_from_image(self):
        ret = ut.import_image("heightmap.jpg")
        self.verts = ret[0]
        self.FACES = ret[1]

    def clean_structure(self):
        self.verts = []
        self.FACES = []
        self.EDGES = []

    def sid(self):
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
