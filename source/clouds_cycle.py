from bge import logic as L
cont = L.getCurrentController()
scene = L.getCurrentScene()
SO = scene.objects

cam = SO['camera']
clouds = SO['Clouds']

def main(cont):
    own = cont.owner
    vel = own["clouds_velocity"]
    if cam["pause"] == False:
        clouds.applyRotation([0,vel,0], True)
