#from bge import logic as L, render, events
import math ,mathutils, random, decimal
from mathutils import Vector, Euler

# scene = L.getCurrentScene()
# SO = scene.objects

def getIncenter(verts):
    for i, e in enumerate(verts):
        if index != 0:
            charly = 0; beta = index-1; charly = index +1;
            if charly == len(self.VERTICES): charly = 0;
            ve1 = self.VERTICES[index]
            ve2 = self.VERTICES[beta]
            ve3 = self.VERTICES[charly]
            ang = ut.angleTriangleBetwenVectors(self.VERTICES[index],ve2,ve3);
            if ang < self.NORMALIZED_ANGLES:
                self.VERTICES[index] = ut.middleVector(ve2,ve3)

def getAvarageWhiteSpaces(points ,divider ,x,y,z ,diameter):
    # x,y,z son los delimitadores para saber donde se generaran los centros de las areas
    # xDiameter es el diametro maximo de la area e yD...
    spaces = []
    for p in range(points):
        if p % divider == 0:
            spaces.append([randVect3D(x,y,z),random.randint(-diameter*100,diameter*100)/100])
    return spaces

def lerp(a, b, x):
    return a*(1-x) + b*x

def cosineInterpolation(a, b, x):
    ft = x * math.pi
    f = (1 - math.cos(ft)) * 0.5
    return a*(1-f) + b*f

def deterministicRandom(x, y, z=0):
    random.seed(z+MASTER_SEED)
    random.seed(x*random.uniform(1,2)+MASTER_SEED)
    random.seed(y*random.uniform(1,2)+MASTER_SEED)
    result = random.uniform(-1, 1)
    return result

def smoothDeterministicRandom(x, y, z=0):
    corners = deterministicRandom(x-1,y-1,z) + deterministicRandom(x+1,y-1,z) + deterministicRandom(x-1,y+1,z) + deterministicRandom(x+1,y+1,z)
    sides = deterministicRandom(x-1,y,z) + deterministicRandom(x,y-1,z) + deterministicRandom(x+1,y,z) + deterministicRandom(x,y+1,z)

    return corners/16 + sides/8 + deterministicRandom(x, y, z)/4



def angleBetwenVectors(v1, v2):
    mag1 = math.sqrt(v1[0]**2+v1[1]**2)
    mag2 = math.sqrt(v2[0]**2+v2[1]**2)

    div = mag1*mag2
    res = (v2[0]*v1[0])+(v1[1]*v2[1])

    if div == 0: return 180
    fin = res/div

    if fin > 1: fin = 1,
    if fin < -1: fin = -1,

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

    if fin > 1: fin = 1;
    if fin < -1: fin = -1;

    ang = math.acos(fin)
    y = ang * 180 / math.pi

    return y

def middleVector(v1,v2):
    p1 = ((v2[0]-v1[0])+(v1[0]*2))/2
    p2 = ((v2[1]-v1[1])+(v1[1]*2))/2
    return Vector((p1,p2,0))


def getWhiteSpaces(spaces):
    vectors = []
    faces = []
    edges = []

    verts = 0
    for space in spaces:
        face = []
        radi = 0;
        while radi < 360:
            radi += 1
            if radi % 10 == 0:
                eul = Euler((0.0, 0, math.radians(radi)), 'XYZ')
                vec = mathutils.Vector((space[0], space[1]+space[2],0))
                vec.rotate(eul)
                vecF = mathutils.Vector((vec[0]+space[0], vec[1]+space[1], vec[2]))
                vectors.append(vecF)
                face.append(verts)
                verts += 1

        faces.append(face)

    struct = [vectors,edges,faces,"white_spaces"]
    return struct

def getDelimiters(spaces):
    vectors = []
    faces = []
    edges = []

    verts = 0
    for space in spaces:
        face = []
        radi = 0;
        while radi < 360:
            radi += 1
            if radi % 10 == 0:
                eul = Euler((0.0, 0, math.radians(radi)), 'XYZ')
                vec = mathutils.Vector((space[0], space[1]+space[2],0))
                vec.rotate(eul)
                vecF = mathutils.Vector((vec[0]+space[0], vec[1]+space[1], vec[2]))
                vectors.append(vecF)
                face.append(verts)
                verts += 1

        faces.append(face)

    struct = [vectors,edges,faces,"white_spaces"]
    return struct


def inAreaVector(area, ve):
    if distanceBetwenVectors(ve,Vector((area[0],area[1],0))) < area[2]:
        return True
    return False

def takeSecond(elem):
    return angleBetwenVectors(Vector((0, 1, 0)), elem)

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
