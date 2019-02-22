from bge import logic

cont = logic.getCurrentController()
own = cont.owner
scene = logic.getCurrentScene()
Hbar = scene.objects['Plane.027']
HRig = scene.objects['Armature']
MRig = scene.objects['Armature.001']

def main():

    if Hbar["meter"] > Hbar["health"]:
        Hbar["meter"] -= 1
    if Hbar["meter"] < Hbar["health"]:
        Hbar["meter"] += 1

    if Hbar["meter_m"] > Hbar["mana"]:
        Hbar["meter_m"] -= 1
    if Hbar["meter_m"] < Hbar["mana"]:
        Hbar["meter_m"] += 1

    HRig.playAction("life_action", Hbar["meter"], Hbar["meter"])
    MRig.playAction("life_action.001", Hbar["meter_m"], Hbar["meter_m"])


class Player(object):
    def __init__(self, arg):
        self.HEALTH = 1000
        self.MAXHEALTH = 1000
        # self.MANAPOINTS = 1000
        # self.MAXMANA = 1000
        # self.STAMINA = 1000
        # self.EXPERIENCE = 0
        # self.LEVEL = 1
        # self.BAGAGE = 0
        # self.MAXBAGAGE = 100

    def add_life(self,quant):
        self.HEALTH += quant
    def set_life(self,quant):
        self.MAXHEALTH = quant
    def get_life(self):
        return self.HEALTH
