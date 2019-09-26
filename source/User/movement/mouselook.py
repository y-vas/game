
from bge import logic
from bge import render
from bge import events as e

class newMouselook:
    def __init__(self, cont):
        self.cont = cont
        self.own = cont.owner

        # Default settings
        self.defSensitivity = 0.0005
        self.defInvert = 1
        self.defCapped = False
        self.defEnable = True
        self.defCursor = False
        self.defUseparent = False

        self.main()

    def main(self):
        # Run main functions
        self.windowSize()       # self.size
        self.getMouse()         # self.mouse
        self.mouseMove()        # self.move

        self.mouseSensitivity() # self.sensitivity
        self.mouseInvert()      # self.invert
        self.mouseCap()         # self.capped
        self.mouseEnable()      # self.enable
        self.useParent()        # self.useparent

        self.showCursor()

        self.mouseUse()
        self.mouseCenter()

        self.useLoc()

        self.dynamicMovement()

    ###################################################

    def windowSize(self):
        width = render.getWindowWidth()
        height = render.getWindowHeight()

        self.size = (width, height)

    ###################################################

    def getMouse(self):
        mouse = None

        for i in self.cont.sensors:
            if str(i.__class__) == "<class 'SCA_MouseSensor'>":
                if i.mode == 9:
                    mouse = i

        self.mouse = mouse

    ###################################################

    def mouseMove(self):
        if self.mouse != None:
            x = self.size[0]/2 - self.mouse.position[0]
            y = self.size[1]/2 - self.mouse.position[1]

            if 'mouseINIT' not in self.own:
                self.own['mouseINIT'] = True
                x = 0
                y = 0

            if not self.mouse.positive:
                x = 0
                y = 0

            self.move = (x, y)

    ###################################################

    def mouseSensitivity(self):
        sen = self.defSensitivity

        if 'Adjust' in self.own:
            if self.own['Adjust'] < 0.0:
                self.own['Adjust'] = 0.0

            sen = self.own['Adjust'] * self.defSensitivity

        self.sensitivity = sen

    ###################################################

    def mouseInvert(self):
        invert = self.defInvert

        if 'Invert' in self.own:
            if self.own['Invert'] == True:
                invert = -1
            else:
                invert = 1

        self.invert = invert

    ###################################################

    def mouseCap(self):
        capped = self.defCapped

        if 'Cap' in self.own:
            import mathutils as m
            from math import pi

            if self.own['Cap'] > 180:
                self.own['Cap'] = 180
            if self.own['Cap'] < 0:
                self.own['Cap'] = 0

            camParent = self.own.parent
            camOri = self.own.localOrientation

            camZ = [camOri[0][2], camOri[1][2], camOri[2][2]]

            pZ = [0.0, 0.0, 0.1]

            v1 = m.Vector(camZ)
            v2 = m.Vector(pZ)

            rads = m.Vector.angle(v2, v1)
            angle = rads * (180.00 / pi)

            capAngle = self.own['Cap']

            moveY = self.move[1] * self.invert

            if (angle > (90 + capAngle/2) and moveY > 0) or (angle < (90 - capAngle/2) and moveY < 0) == True:
                capped = True

        self.capped = capped

    ###################################################

    def mouseEnable(self):
        enable = self.defEnable

        if 'Enable' in self.own:
            if self.own['Enable'] == True:
                enable = True
            else:
                enable = False

        self.enable = enable

    ###################################################

    def showCursor(self):
        notset = False
        if 'Cursor' in self.own:
            if self.own['Cursor'] == True:
                cursor = True
            else:
                cursor = False
        else:
            notset = True

        if notset == False:
            if cursor == True:
                render.showMouse(1)
            else:
                render.showMouse(0)

    ###################################################

    def useParent(self):
        useparent = self.defUseparent

        if self.own.parent != None:
            if 'UseParent' not in self.own:
                useparent = True
            else:
                if self.own['UseParent'] == True:
                    useparent = True
                else:
                    useparent = False

        if self.own.parent == None:
            useparent = False

        self.useparent = useparent

    ###################################################

    def mouseUse(self):
        if self.capped == True:
            vert = 0
        else:
            vert = self.move[1] * self.sensitivity * self.invert

        horz = self.move[0] * self.sensitivity * self.invert

        if self.enable == True:
            ori = self.own.localOrientation.to_euler()
            ori.x += vert

            if self.useparent == False:
                ori.z += horz
            else:
                ori2 = self.own.parent.localOrientation.to_euler()
                ori2.z += horz
                self.own.parent.localOrientation = ori2

            self.own.localOrientation = ori

    ###################################################

    def mouseCenter(self):
        if self.mouse != None:
            pos = self.mouse.position

            if pos != [int(self.size[0]/2), int(self.size[1]/2)]:
                if self.enable == True:
                    render.setMousePosition(int(self.size[0]/2), int(self.size[1]/2))

    ###################################################

    # meant for non-parented cameras
    # lMove
    def useLoc(self):
        if 'lMove' in self.own and self.own['lMove'] == True and self.own.parent == None:

            key = logic.keyboard.events

            if 'lSpeed' in self.own:
                loc = self.own['lSpeed']
            else:
                loc = 0.05

            if 'lFly' in self.own:
                fly = self.own['lFly']
            else:
                fly = 0.05

            layout = 1

            if 'Layout' in self.own:
                if self.own['Layout'] != 1 or self.own['Layout'] != 2:
                    layout = 1
                if self.own['Layout'] == 1:
                    layout = 1
                elif self.own['Layout'] == 2:
                    layout = 2

            if layout == 1:
                up = key[e.WKEY] == 2
                down = key[e.SKEY] == 2
                left = key[e.AKEY] == 2
                right = key[e.DKEY] == 2

                flyUp = key[e.QKEY] == 2
                flyDown = key[e.EKEY] == 2
            elif layout == 2:
                up = key[e.IKEY] == 2
                down = key[e.KKEY] == 2
                left = key[e.JKEY] == 2
                right = key[e.LKEY] == 2

                flyUp = key[e.OKEY] == 2
                flyDown = key[e.UKEY] == 2

            move = [0, 0, 0]
            fmove = [0, 0, 0]

            # Up
            if up:
                move[2] = -loc

            # Down
            if down:
                move[2] = loc

            # Left
            if left:
                move[0] = -loc

            # Right
            if right:
                move[0] = loc

            # Fly up
            if flyUp:
                fmove[2] = fly

            # Fly down
            if flyDown:
                fmove[2] = -fly

            self.own.applyMovement(move, True)
            self.own.applyMovement(fmove, False)

    ###################################################

    # Designed for a camera parented to a Dynamic object
    # dMove
    def dynamicMovement(self):
        if self.own.parent != None:
            if 'dMove' in self.own and self.own['dMove'] == True:
                parent = self.own.parent
                k = logic.keyboard.events

                layout = 1
                fly = False

                if 'Layout' in self.own:
                    if self.own['Layout'] != 1 or self.own['Layout'] != 2:
                        layout = 1
                    if self.own['Layout'] == 1:
                        layout = 1
                    elif self.own['Layout'] == 2:
                        layout = 2

                if 'dFly' in self.own:
                    if self.own['dFly'] == True:
                        fly = True
                    else:
                        fly = False

                if layout == 1:
                    up = k[e.WKEY] == 2
                    down = k[e.SKEY] == 2
                    left = k[e.AKEY] == 2
                    right = k[e.DKEY] == 2

                    jump = k[e.SPACEKEY] == 2
                    crouch = k[e.LEFTSHIFTKEY] == 2
                elif layout == 2:
                    up = k[e.IKEY] == 2
                    down = k[e.KKEY] == 2
                    left = k[e.JKEY] == 2
                    right = k[e.LKEY] == 2

                    jump = k[e.SPACEKEY] == 2
                    crouch = k[e.RIGHTSHIFTKEY] == 2

                col = None
                ray = None
                keyboard = None
                #"<class 'KX_TouchSensor'>"
                #"<class 'KX_RaySensor'>"
                for i in parent.sensors:
                    if str(i.__class__) == "<class 'KX_TouchSensor'>":
                        col = i
                    if str(i.__class__) == "<class 'KX_RaySensor'>":
                        ray = i

                for i in self.own.sensors:
                    if str(i.__class__) == "<class 'SCA_KeyboardSensor'>":
                        keyboard = i

                # Keyboard Inactive Timer
                # Keyboard shuts off Negative Pulse after 2 seconds
                # of keyboard inactivity
                if keyboard != None:
                    if 'KIT' not in self.own:
                        self.own['KIT'] = 120

                    if keyboard.positive:
                        self.own['KIT'] = 120
                        keyboard.useNegPulseMode = True
                    elif self.own['KIT'] > 0:
                        self.own['KIT'] -= 1

                    if self.own['KIT'] <= 0:
                        keyboard.useNegPulseMode = False

                rray = False
                ccol = False

                if ray != None:
                    ray.range = 2
                    if 'dRange' in self.own:
                        ray.range = self.own['dRange']
                    ray.axis = 5
                    # 5 = -Z axis

                    if ray.positive:
                        rray = True

                if col != None:
                    if col.positive:
                        ccol = True

                speed = 10
                jspeed = 0
                jumpspeed = 10
                limit = .75

                if 'dSpeed' in self.own:
                    speed = self.own['dSpeed']
                if 'dJump' in self.own:
                    jumpspeed = self.own['dJump']

                if 'air' not in parent:
                    parent['air'] = False

                if crouch and parent['air'] == False and fly == False:
                    speed = speed/3
                    limit = .95

                fspeed = speed * (up - down)
                sspeed = speed * (right - left)

                if fspeed and sspeed:
                    fspeed *= 0.70710678
                    sspeed *= 0.70710678

                if col != None and ray != None:
                    if (parent['air'] == True or not ccol) and fly == False:
                        fspeed *= .005
                        sspeed *= .005

                if jump and parent['air'] == False and rray and not crouch:
                    jspeed = jumpspeed
                    parent['air'] = True

                if jump and fly == True:
                    jspeed = 1

                elif ccol and not jump:
                    parent['air'] = False

                parent.localLinearVelocity[0] += sspeed
                parent.localLinearVelocity[1] += fspeed
                parent.localLinearVelocity[2] += jspeed

                dispIndex = 0 # disposable index counter

                for i in parent.localLinearVelocity:
                    if dispIndex != 2:
                        if i > speed:
                            i = speed
                        if i < -speed:
                            i = -speed
                    parent.localLinearVelocity[dispIndex] = i
                    dispIndex += 1

                if parent['air'] == False or (fly == True and crouch):
                    if not up and not down:
                        parent.localLinearVelocity[1] -= parent.localLinearVelocity[1]*limit
                    if not left and not right:
                        parent.localLinearVelocity[0] -= parent.localLinearVelocity[0]*limit
                elif parent['air'] == True and fly == False:
                    dispIndex = 0
                    parent.applyForce([0, 0, -10], True)
                    for i in parent.localLinearVelocity:
                        ii = i*0.02

                        if dispIndex != 2:
                            parent.localLinearVelocity[dispIndex] += ii

                        dispIndex += 1
                if fly == True and crouch == True:
                    parent.localLinearVelocity[2] = .175

def main():
    cont = logic.getCurrentController()
    own = cont.owner

    if 'mouselookMain' not in own:
        own['mouselookMain'] = newMouselook(cont)

    own['mouselookMain'].main()

main()
