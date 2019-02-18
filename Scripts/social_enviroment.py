from bge import logic as L
import math
import random
from random import randint
import mainutils as ut

cont = L.getCurrentController()
own = cont.owner;
scene = L.getCurrentScene()

SO = scene.objects;
player = SO["lifter"]
player = SO["player_capsule"]


def start():
    if own["pause"] == False:
       print("citizens dissable")
       break

def run():
    goto = cont.actuators["goto"]
    chek = cont.sensors["chek"]

    if chek.positive:
        own["calc"] = False

    if own["moving"] == True:
        goto_name = player
        if own["calc"] == False:
            shortdistance = 1000
            for i in SO:
                if 'spawner' in i:
                    rdm = randint(0,1)
                    if rdm == 1:
                        res = ut.Distance(own,i)
                        if res < shortdistance:
                            shortdistance = res
                            goto_name = i
                        print(res)
            own["calc"] = True
        else:
            goto.target = goto_name
            cont.activate(goto)
            own["moving"] = False


# ////////// citizens_2
    #
    # if i["moving"] == False:
    #     closest = []
    #     for f in list:
    #         if Distance(i,f) < 30:
    #             closest.append(f)
    #     i["target"] = random.choice(closest)
    #
    #     goto = i.getVectTo(i["target"])[1]
    #     i["x"] = goto.x; i["y"] = goto.y
    #     i["moving"] = True
    # else:
    #     tgt = SO[str(i["target"])]
    #     i.applyMovement((i["x"]*own["speed"],i["y"]*own["speed"],0))
    #     if Distance(i,tgt) < 1:
    #         i["moving"] = False




def runSpawner():
    list = []
    for i in SO:
        if 'spawner' in i:
            list.append(i)

    if own["population"] != own["max_spawn"]:
        spawning = []
        for f in list:
            if ut.Distance(player,f) < 30:
                spawning.append(f)

        choice = random.choice(spawning)
        scene.addObject("enemy_cube", choice)
        own["population"] += 1

    for i in SO:
        if 'citizen' in i:
            i["citizen"] = "citizen"+str(random.randint(0,999))
            if i["moving"] == False:
                closest = []
                for f in list:
                    if ut.Distance(i,f) < 30:
                        closest.append(f)
                i["target"] = random.choice(closest)
                i["moving"] = True
            else:
                tgt = SO[str(i["target"])]
                i.actuators["stering"].target = i["target"]
                if ut.Distance(i,tgt) < 1:
                    i["moving"] = False
