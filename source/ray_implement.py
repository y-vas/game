import bge

# get controller
cont = bge.logic.getCurrentController()

# get object that controller is attached to
obj = cont.owner

# get the current scene
scene = bge.logic.getCurrentScene()

# get a list of the objects in the scene
objList = scene.objects

# get the object named Cube
cube = objList["Cube"]

# raycast to game object named "Cube"
to = cube

# raycast from object python controller attached to
from = obj

# Ray stretches all the way to the other object center
distance = 0.0

# property on an other object that will trip the ray
property = "BlueTeam"

# return face normal
face = 1

# xray is enabled
xray = 1

# don't return polygon
poly = 0

# get GameObject, hit position and angle.
hit = obj.rayCast( to, from, distance, property, face, xray, poly)
