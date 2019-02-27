import bge

def main(cont):
    cam = cont.owner
    sens = cont.sensors['pause']
    comand = cont.sensors['word']
    enable = cont.actuators['enable']
    desable = cont.actuators['disable']
    filtro = cont.actuators['Filter 2D']

    ## PAUSE ##
    if sens.positive and cam["pause"] == True:
        cam["pause"] = False
        cont.activate(desable)
    elif sens.positive and cam["pause"] == False:
        cam["pause"] = True
        cont.activate(enable)
        cont.activate(filtro)

    ## ## ## ##

    if comand.positive:
        word = str(comand.bodies[0])
        if word == "SPEED":
            cam["velocity"] = 1
        if word == "FLASH":
            cam["velocity"] = 2
        if word == "QUIKSILVER":
            cam["velocity"] = 3
        if word == "SONIC":
            cam["velocity"] = 4
        
