from bge import logic as L
from random import randint
import math
import random
import mathutils
import utils

cont = L.getCurrentController()
own = cont.owner;
scene = L.getCurrentScene()
SO = scene.objects; player = SO["lifter"]

def WalckCitizens(targets, frams ,stressed, walkpoint):
  for i in targets:
      if i["enemy"] == False:
          road_points = utils.ListAllObjects(walkpoint)
          i["target"] = random.choice(road_points); i["target"].worldScale = [1,1,1]

          route = [];

          smallest = (10**10);  small_point = "";
          for point in road_points:
              for x in road_points:
                  if point.worldPosition == i["target"].worldPosition:
                      pass
                  if utils.Distance(point,i)+utils.Distance(x,i["target"]) < smallest:
                      smallest = utils.Distance(point,i)+utils.Distance(x,i["target"])
                      small_point = point
          small_point.worldScale = [1,0.5,0.5]

          i["enemy"] = True;

      objective = i["target"]
      objective_distance = utils.Distance(i,objective)

      if objective_distance < 0.5:
          i["target"] = utils.getNearObject("WGT-torso",i)

      dirs = utils.Direction(i,objective)
      i.setLinearVelocity((-dirs[0],-dirs[1],0), False)
      if frams == 3: scene.addObject("WGT-elbow_target.ik.R.001",i, 0)
