from bge import logic as L, render, events
from mathutils import Vector
import math ,mathutils, random

import sys, os, bpy

# adding scripts to syspath
directory = os.path.dirname(bpy.data.filepath)
scripts = os.path.join(directory, "source")
if scripts not in sys.path:
   sys.path.append(scripts)



cont = L.getCurrentController(); scene = L.getCurrentScene()
SO = scene.objects

bumper = SO["bumper"]; lifter = SO["lifter"]; orienter = SO["orienter"]; tilt = SO["tilt"]
cam = SO["camera"]; reset = SO["Reset"]; empty = SO["empty"]; xyori = SO["xy_ori"]
control = SO["control_cam"]; control2 = SO["control_cam2"]
rig = SO["rig"]

pause = cam["pause"]

max_angle = 0
walkmode = "walk" ; fightmode = False ; delta = 0.03
last_vel = lifter.getLinearVelocity(); frams = 0; list = []; wheel_rot_vel = 0

# life and status
HealtPoints = 1000
MaxHealth = 1000
ManaPoints = 1000
MaxMana = 1000
stamina = 1000
Experiencia = 0
Dificulty = 0
Level = 0
Weight = 0
MaxWeight = 100
damage_value = 50
stressed = False; stresstimer = 0; hit = 0

def run():
    global pause
    global max_angle, last_vel, list, wheel_rot_vel
    global walkmode, fightmode, frams, delta
    global stressed, stresstimer, hit
    global stamina

    frams += 1

    # Keyboard and Mouse Events --------------------------------------------------------------------------

    M = L.mouse.events; K = L.keyboard.events

    lmk= M[events.LEFTMOUSE]; rmk= M[events.RIGHTMOUSE]; mmk= M[events.WHEELUPMOUSE]
    wupKey= M[events.WHEELUPMOUSE]; wdownKey= M[events.WHEELDOWNMOUSE]

    wKey = K[events.WKEY]; aKey = K[events.AKEY]; sKey = K[events.SKEY]; dKey = K[events.DKEY]
    qKey = K[events.QKEY]; eKey = K[events.EKEY]; rKey = K[events.RKEY]; tKey = K[events.TKEY]
    fKey = K[events.FKEY]; gKey = K[events.GKEY];
    zKey = K[events.ZKEY]; xKey = K[events.XKEY]; cKey = K[events.CKEY]; vKey = K[events.VKEY]
    move_Keys = [wKey,aKey,sKey,dKey]

    lsKey = K[events.LEFTSHIFTKEY]; lcKey = K[events.LEFTCTRLKEY]; spKey = K[events.SPACEKEY]

    kxa = L.KX_INPUT_ACTIVE; kxn = L.KX_INPUT_NONE
    kxja = L.KX_INPUT_JUST_ACTIVATED; kxjr = L.KX_INPUT_JUST_RELEASED

    play = L.KX_ACTION_MODE_PLAY; loop = L.KX_ACTION_MODE_LOOP

    #-----------------------------------------------------------------------------------------------------

    ray = cont.sensors["ray"] ; bumper_ray = cont.sensors["lifter_ray"]
    grounded = cont.sensors["grounded"]

    speed = 0; top = 0.2

    if pause == False:
        Living_Status() # Life functions
        LetsMove() #moving enemies

        if ray.positive: xyori.worldPosition = ray.hitPosition
        else: xyori.worldPosition = reset.worldPosition

        if cKey == kxja:
            if walkmode == "walk": walkmode = "run"
            else: walkmode = "walk"

        if walkmode == "walk":
            speed = 30 ;top = 0.05 ; delta = 0.03
            if lsKey == kxja: walkmode = "sprint"
        else:
            speed = 50; top = 0.1 ; delta = 0.015
            if lsKey == kxa: speed = 80; top = 0.15; walkmode = "sprint"
        if lsKey == kxjr: walkmode = "walk"

        ray_diference = lifter.worldPosition.z - bumper_ray.hitPosition[2] -0.5

        ## Mouse Mov ## ---------
        mouse = cont.sensors["mouse_movement"]
        maxRot = 1.5; smother = 0.001

        x = (render.getWindowWidth() / 2 - mouse.position[0]); y = (render.getWindowHeight() / 2 - mouse.position[1])
        max_angle= max_angle+int(y) * smother

        if max_angle > maxRot+0.01: control.localOrientation = [maxRot, 0, 0]; max_angle = maxRot
        if max_angle < -maxRot-0.01: control.localOrientation = [-maxRot, 0, 0]; max_angle = -maxRot
        if max_angle < maxRot and max_angle > -maxRot: control.applyRotation((int(y)*smother, 0, 0), True)

        control2.applyRotation((0 , 0, int(x)*smother), False)
        render.setMousePosition(int(render.getWindowWidth()/2), int(render.getWindowHeight() / 2))

        #Camera Vision ----------------
        if cam.lens < 70:
            if wupKey == kxa:
               cam.lens += 5

        if cam.lens > 25:
            if wdownKey == kxa:
               cam.lens -= 5

        ## Movement ##
        a = 0; b = 0; angle = control2.worldOrientation; alpha = False; bravo = False

        if wKey == kxa: b += angle[0][0]; a += -angle[1][0]; alpha = True
        elif sKey == kxa: b+= -angle[0][0]; a += angle[1][0]; alpha = True
        if aKey == kxa: b+= -angle[1][0]; a += -angle[0][0]; bravo = True
        elif dKey == kxa: b += angle[1][0]; a += angle[0][0]; bravo = True

        charlie = 0.1
        if alpha == True and bravo == True: charlie = 0.07
        a = a*charlie; b = b*charlie

        ## Rotation twords velocity
        an = math.atan2(b,a)
        quat_a = mathutils.Quaternion((0, 0, 1), an+math.pi/2)
        non_move = rig.worldOrientation.to_quaternion()

        ## Acceleration Tilt
        acc = ((last_vel - lifter.getLinearVelocity())/L.getAverageFrameRate())*speed/2
        list.append([acc.x,acc.y])

        fr = 3
        if frams == fr:
           avx = 0; avy = 0
           for i in list: avx += i[0]; avy += i[1]
           avx = avx/fr; avy = avy/fr

           # filter
           if abs(avx) > top: avx = top
           if abs(avx) < -top: avx = -top
           if abs(avy) > top: avy = top
           if abs(avy) < -top: avy = -top

           tilt.worldOrientation = [avx,avy,0]
           list = []; frams = 0

        last_vel = lifter.getLinearVelocity()

        ## Finshed prceseces ## Animations
        #atacks

        if stressed == False: #no combatint
           if lmk == kxa: stressed = True ; stresstimer = 0
           rig.playAction("calm", 1, 40, 0, 0, 5, loop)
        else:
           if stresstimer == 500: stressed = False
           if lmk == kxja and any(move_Keys) == False:
              stresstimer = 0

              if hit == 0: hit += 1; rig.playAction("direct_hit-l", 0, 8, 1, 0, 3, play)
              else: hit = 0; rig.playAction("direct_hit-r", 0, 8, 1, 0, 3, play)

           if rig.getActionFrame(1) >= 7:
              print("damage")

           rig.playAction("stressed", 1, 30, 0, 0, 5, loop)
           stresstimer += 1

        #run/walk/sprint
        wheel_rot_vel += round(math.sqrt(last_vel.x**2+last_vel.y**2),2)*delta
        if wheel_rot_vel > 5: wheel_rot_vel = 0
        action_frame = round((wheel_rot_vel)*6)

        for i in move_Keys:
            if i == kxa:
                rig.playAction(walkmode, action_frame, action_frame, 0, 0, 0, play)
                if grounded.positive:
                   lifter.setLinearVelocity((a*speed,b*speed,0), False)
                   orienter.worldOrientation = quat_a.to_euler()
            #if i == kxjr:
            #  rig.playAction("stopwalk", 0, 12, 0, 0, 0, play)
        orient = orienter.worldOrientation.to_quaternion()*tilt.worldOrientation.to_quaternion()
        rig.worldOrientation  = non_move.slerp(orient,0.1)

        if spKey == kxa and ray_diference < 0.1:
            lifter.applyForce([ 0, 0, 150], 0)
    else:
        for x in range(0,10):
            rig.stopAction(x)

def Living_Status():
   global pause
   global HealtPoints, damage_value
   damage = cont.sensors["damage"]
   if damage.positive: HealtPoints -= damage_value

def Distance(point, target):
    x = point.worldPosition.x ; y = point.worldPosition.y
    Vx= target.worldPosition.x ; Vy= target.worldPosition.y
    distance = math.sqrt((x-Vx)**2+(y-Vy)**2)
    return distance

def LetsMove():
  global stressed

  for i in SO:
    if 'enemy' in i:
        rig = SO[str(i.children[0])]
        an = math.atan2(i.getLinearVelocity().y,i.getLinearVelocity().x)
        quat_a = mathutils.Quaternion((0, 0, 1), an+math.pi/2)

        if stressed == True and Distance(lifter,i) < 10:
          an = math.atan2(bumper.worldPosition.y-i.worldPosition.y,bumper.worldPosition.x-i.worldPosition.x)

          quat_a = mathutils.Quaternion((0, 0, 1), an+math.pi/2)

          angle = rig.worldOrientation = quat_a.to_matrix()
          print(angle[1][0])

          i.setLinearVelocity((angle[1][0], angle[0][1],0), False)

          rig.playAction("stressed", 1, 30, 0, 0, 0, L.KX_ACTION_MODE_LOOP)
        else:
            i.setLinearVelocity((i["x"],i["y"],0), False)
            quat_a = mathutils.Quaternion((0, 0, 1), an+math.pi/2)
            rig.worldOrientation = quat_a.to_euler()
            if i["change_dir_timer"] < i["end_timer"]:
              i["change_dir_timer"] += 1
              rig.playAction("walk", 1, 30, 0, 0, 0, L.KX_ACTION_MODE_LOOP)
            else:
              i["change_dir_timer"] = 0
              i["end_timer"] = random.randint(50,200)
              i["x"] = random.uniform(-3,3); i["y"] = random.uniform(-3,3)

        quat_a = mathutils.Quaternion((0, 0, 1), an+math.pi/2)
        rig.worldOrientation = quat_a.to_euler()
