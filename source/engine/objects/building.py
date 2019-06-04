from engine.objects.structure import *

class Building(object):
    def __init__(self, height, type):
        self.HEIGHT = height
        self.TYPE = type
        self.STRUCTURE = Structure(20,"house");

    def generate(self):
        struc = self.STRUCTURE;
        struc.set_plane_structure();
        struc.set_structure_extrusion(False);
        pass

    def getStructure(self):
        return self.STRUCTURE;
