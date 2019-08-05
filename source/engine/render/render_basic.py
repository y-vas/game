from bge import logic, texture
from engine.render.build import *
from mathutils import Vector

# use it as a module and autoloait each time set the D on

sce = logic.getCurrentScene()
own = logic.getCurrentController().owner

wid = 50

faces =[[0,1,2,3]]
verts =[ Vector( (0,    0,1) ),
         Vector( (wid,  0,1) ),
         Vector( (wid,wid,1) ),
         Vector( (0,  wid,1) )
        ]

properties = {
              "timer": 10,
              "cont": 15
              }

draw = PostDraw(verts,faces,properties,"","")

def load():
    draw.use(sce);
