import bge
cont = bge.logic.getCurrentController()
obj = cont.owner
scene = bge.logic.getCurrentScene()
objList = scene.objects
cube = objList["Cube"]
to = cube

 # from = objº

distance = 0.0
face = 1
xray = 1
poly = 0
hit = obj.rayCast( to, from, distance, property, face, xray, poly)
