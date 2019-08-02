#from bge import logic as L, render, events
import math ,mathutils, random, decimal
from mathutils import Vector, Euler
from imports.sqlite import sql
import bpy
import sys, os, shutil, time


def sql_query(query):
    sp = sql.SQL("data");
    return sp.execute(query)

def sql_insert(query):
    sp = sql.SQL("data");
    ser = sp.insert_and_get_last_serial(query)
    return ser

def import_image():
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    scripts = os.path.join(directory, "Scripts", "Imports", "PIL")
    map = os.path.join(directory, "Textures","Map","heightmap.jpg")

    if not scripts in sys.path:
        sys.path.append(scripts)

    im = Image.open(map)
    rgb_im = im.convert('RGB')
    basewidth = 1000

    wpercent = (basewidth/float(rgb_im.size[0]))
    hsize = int((float(rgb_im.size[1])*float(wpercent)))
    imgf = rgb_im.filter(ImageFilter.SMOOTH)
    img = imgf.resize((basewidth,hsize), Image.ANTIALIAS)

    width, height = img.size
    div = 1
    aux = [];
    faces = [];

    for wp in range(width):

        for hp in range(height):
            r, g, b = img.getpixel((wp, hp))
            aux.append(Vector((wp/div,hp/div,r/div)))

    for wp in range(width):
        if wp == width-1:
            continue;
        for hp in range(height):
            if hp == height-1:
                continue;
            faces.append([hp+(wp*width),hp+1+(wp*width),hp+1+((wp+1)*width),hp+((wp+1)*width)])
            # print([hp+(wp*width),hp+1+(wp*width),hp+1+((wp+1)*width),hp+((wp+1)*width)])

    ret = [aux,faces]
    return ret

def reloadTexts():
    ctx = bpy.context.copy()
    ctx['area'] = ctx['screen'].areas[0]
    for t in bpy.data.texts:
        if t.is_modified and not t.is_in_memory:
            print("  * Warning: Updating external script", t.name)
            oldAreaType = ctx['area'].type
            ctx['area'].type = 'TEXT_EDITOR'
            ctx['edit_text'] = t
            bpy.ops.text.resolve_conflict(ctx, resolution='RELOAD')
            ctx['area'].type = oldAreaType


def get_center_of_polygon(verts):
    p_center = Vector((0.0, 0.0, 0.0))

    if len(verts) == 0:
        return p_center

    for v in verts:
        p_center[0] += v[0]
        p_center[1] += v[1]
        p_center[2] += v[2]

    p_center[0] /= len(verts)
    p_center[1] /= len(verts)
    p_center[2] /= len(verts)

    return p_center


def get_points_where_edges_intersect_form_faces(face1,v_delim):
    out = [];
    for inx, vertex in enumerate(face1):
        beta = inx-1
        if inx == 0: beta = len(face1)-1;
        for index2 in range(len(v_delim)):
            beta2 = index2 - 1

            if index2 == 0:
                beta2 = len(v_delim)-1;

            v1 = v_delim[index2]
            v2 = v_delim[beta2]
            v3 = face1[inx]
            v4 = face1[beta]

            intersection = mathutils.geometry.intersect_line_line(v1,v2,v3,v4);

            if intersection == None: continue

            d1 = distance(v3,v4)
            d2 = distance(v3,intersection[0])
            d3 = distance(intersection[0],v4)

            if d2 > d1 or d3 > d1:
                continue;

            out.append(intersection[0])

    return out

def is_face_in_face(face,v_delim):
    center = get_center_of_polygon(v_delim)
    for vertex in face:
        for index2 in range(len(v_delim)):
            beta2 = index2-1
            if index2 == 0: beta2 = len(v_delim)-1;
            vec = mathutils.geometry.intersect_point_tri(vertex,center,v_delim[index2],v_delim[beta2])
            if vec != None:
                return True
    return False

def get_max_radius_in_vertices(verts):
    newv = get_center_of_polygon(verts)
    dist = 0
    for vect in verts:
        dista = distance(newv,vect)
        if dista > dist:
            dist = dista
    return dist

def get_points_that_are_in_delited_area(v_delim, face):
    center = get_center_of_polygon(v_delim)
    out = []
    for vertex in face:
        for index2 in range(len(v_delim)):
            beta2 = index2-1
            if index2 == 0: beta2 = len(v_delim)-1;
            vec = mathutils.geometry.intersect_point_tri(vertex,center,v_delim[index2],v_delim[beta2])
            if vec != None: out.append(vec)

    return out

def angleBetwenVectors(v1, v2):
    mag1 = math.sqrt(v1[0]**2+v1[1]**2)
    mag2 = math.sqrt(v2[0]**2+v2[1]**2)

    div = mag1*mag2
    res = (v2[0]*v1[0])+(v1[1]*v2[1])

    if div == 0: return 180
    fin = res/div

    if fin > 1: fin = 1
    if fin < -1: fin = -1

    x = math.acos(fin)
    y = x * 180 / math.pi

    if v2[0] < 0:
        y = -y

    return y

def angleTriangleBetwenVectors(v1, v2, v3):
    v12 = [(v2[0]-v1[0]),(v2[1]-v1[1])]
    v13 = [(v3[0]-v1[0]),(v3[1]-v1[1])]

    vs12 = math.sqrt((v12[0]**2)+(v12[1]**2));
    vs13 = math.sqrt((v13[0]**2)+(v13[1]**2));

    prod_escalar = v12[0]*v13[0]+v12[1]*v13[1]
    div = vs12*vs13

    if div == 0: return 180
    fin = prod_escalar/div

    if fin > 1: fin = 1 #redondeo
    if fin < -1: fin = -1 #redondeo

    ang = math.acos(fin)
    y = ang * 180 / math.pi

    return y

def angles_of_a_triangle(A, B, C):
    cat_adj = distance(A,B)
    cat_opu = distance(C,B)

    div = cat_opu/cat_adj
    prep = A.cross(C)
    dir = prep.dot(B)

    if dir < 0:
        div = -div

    return div


def angles_of_a_triangle_beta(A, B, C):
    AB = Vector( ( (B[0]-A[0]) , (B[1]-A[1]) , (B[2]-A[2]) ) )
    AC = Vector( ( (C[0]-A[0]) , (C[1]-A[1]) , (C[2]-A[2]) ) )
    BC = Vector( ( (C[0]-B[0]) , (C[1]-B[1]) , (C[2]-B[2]) ) )

    mg1 = magnitude(AB)
    mg2 = magnitude(AC)
    mg3 = magnitude(BC)

    nrm1 = norm(AB,mg1)
    nrm2 = norm(AC,mg2)
    nrm3 = norm(BC,mg3)

    res = nrm1.dot(nrm2)

    angle = math.atan(res)
    print(angle)

    # return angle
    return angle

def delete_objects_from_layer(layer):
    for o in bpy.data.objects:
        if o.layers[layer] == True:
            bpy.data.objects.remove(o,True)

def middleVector(v1,v2):
    p1 = ((v2[0]-v1[0])+(v1[0]*2))/2
    p2 = ((v2[1]-v1[1])+(v1[1]*2))/2
    return Vector((p1,p2,0))


def inAreaVector(area, ve):
    if distanceBetwenVectors(ve,Vector((area[0],area[1],0))) < area[2]:
        return True
    return False

def takeSecond(elem):
    return angleBetwenVectors(Vector((0, 1, 0)), elem[0])

def sort_by_angle(elem):
    return elem[2]

def randVect2D(x,y):
    vx = random.randint(-x*100,y*100)/100
    vy = random.randint(-x*100,y*100)/100
    vec = Vector((vx, vy, 0))
    return vec

def randVect3D(x,y,z):
    vx = random.randint(-x*100,y*100)/100
    vy = random.randint(-x*100,y*100)/100
    vz = random.randint(-z*100,z*100)/100
    vec = Vector((vx, vy, vz))
    return vec

def Direction(point, target):
    x = point.worldPosition.x
    y = point.worldPosition.y
    Vx= target.worldPosition.x
    Vy= target.worldPosition.y

    distance_x = x-Vx
    distance_y = y-Vy
    distance = math.sqrt((distance_x)**2+(distance_y)**2)

    direction_x = distance_x/distance
    direction_y = distance_y/distance

    return [direction_x, direction_y]

def Distance(point, target):
    x = point.worldPosition.x ; y = point.worldPosition.y
    Vx= target.worldPosition.x ; Vy= target.worldPosition.y
    distance = math.sqrt((x-Vx)**2+(y-Vy)**2)
    return distance

def distance(A, B):
    return math.sqrt((B[0]-A[0])**2+(B[1]-A[1])**2+(B[2]-A[2])**2)

def magnitude(A):
    return math.sqrt(A[0] * A[0] + A[1] * A[1] + A[2] * A[2])

def distanceBetwenVectors(v1, v2):
    x = v1[0] ; y = v1[1]
    Vx= v2[0] ; Vy= v2[1]
    distance = math.sqrt((x-Vx)**2+(y-Vy)**2)
    return distance

def Generate_Object(what, where, rang, loops):
    for x in range(1, loops):
        road_range_x = float(decimal.Decimal(random.randrange(-rang, rang))/100)
        road_range_y = float(decimal.Decimal(random.randrange(-rang, rang))/100)

        SO[where].localPosition = [ road_range_x, road_range_y, 0 ]
        scene.addObject(what,where, 0)

    SO[where].localPosition = [ 0, 0, 3.0 ]

def ListAllObjects(targets, posi = 0):
    enemies = []; pos = []
    if posi == 0:
        for enemy in SO:
            if enemy.name.startswith(targets):
                enemies.append(enemy)
        return enemies
    else:
        for enemy in SO:
            if enemy.name.startswith(targets):
                enemies.append(enemy)
                pos.append(enemy.worldPosition)
        return enemies, pos

def getNearObject(typeof, point):
    sorted_objects = ListAllObjects(typeof)
    distance = 20000
    NearObject = point
    for obj in sorted_objects:
        if Distance(point, obj) < distance:
            distance = Distance(point, obj)
            NearObject = obj
    return NearObject

def inArea(pointA,pointB, target):
    xa = pointA.worldPosition.x; ya = pointA.worldPosition.y
    xb = pointB.worldPosition.x; yb = pointB.worldPosition.y

    rangex = range(xa,xb)
    rangey = range(ya,yb)

    xt = target.worldPosition.x
    yt = target.worldPosition.y

    if xt in rangex and yt in rangey:
        return True
    else:
        return False

def inRange(objlist,pointA,pointB):
    inRangePoints = []
    for point in objlist:
        if inArea(pointA, pointB, point) == True:
            inRangePoins.append(point)
    return inRangePoints


def dot(vU, vV):
	return vU[0]*vV[0]+vU[1]*vV[1]+vU[2]*vV[2];

def norm2(v):
	return v[0]*v[0]+v[1]*v[1]+v[2]*v[2];

def norm(v,mag):
	return Vector((v[0]/mag,v[1]/mag,v[2]/mag));

def cross(b,c):
	return Vector((b[1]*c[2]-c[1]*b[2],b[2]*c[0]-c[2]*b[0],b[0]*c[1]-c[0]*b[1]));
