#! /usr/bin/python

from bge import logic, events, constraints
import camera_rig
    
    

def run():
    cont = logic.getCurrentController()
    scene = logic.getCurrentScene()
    own = cont.owner  
    
    # Keyboard Mouse Events ############################################################################
    mouse = logic.mouse.events
    lmKey= mouse[events.LEFTMOUSE]
    rmKey= mouse[events.RIGHTMOUSE]
    midKey= mouse[events.WHEELUPMOUSE]
    wupKey= mouse[events.WHEELDOWNMOUSE]
    mxKey= mouse[events.MOUSEX]
    myKey= mouse[events.MOUSEY]
    
    keyboard = logic.keyboard.events 
    wKey = keyboard[events.WKEY]
    sKey = keyboard[events.SKEY]
    dKey = keyboard[events.DKEY]
    aKey = keyboard[events.AKEY]
    lshKey = keyboard[events.LEFTSHIFTKEY]
        
    kInput = cont.sensors ["keyimput"]
    nkInput = cont.sensors ["keyinput"]
    non = nkInput.events == []
    
    kxa = logic.KX_INPUT_ACTIVE
    kxn = logic.KX_INPUT_NONE
    kxjr = logic.KX_INPUT_JUST_RELEASED
    kxja = logic.KX_INPUT_JUST_ACTIVATED
    
    """
    print(nkInput.events)
    if kInput.positive:
        print(kInput.events) 
    """    
    
    # Action ############################################################################################
    
    Animation(lmKey == kxja, "direct_hit", 11,  
    
    if lmKey == kxja:
        #OutsideEvents(True, 0.01):
         own.playAction("direct_hit",  0 , 11, layer=1, priority=0, blendin=5, play_mode=logic.KX_ACTION_MODE_PLAY, layer_weight=0.0, ipo_flags=0, speed=1, blend_mode=logic.KX_ACTION_BLEND_BLEND)
         
    if lmKey == kxa:
        scene.objects['Player.001']['postimer'] = 0
       
        OutsideEvents(True, 0.01)
        own.playAction("stressed",  0 , 30, layer=0, priority=0, blendin=5, play_mode=logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1, blend_mode=logic.KX_ACTION_BLEND_BLEND)
    
    if  non and lmKey == kxn and scene.objects['Player.001']['postimer'] >= 5:
        
        OutsideEvents(False)
        own.playAction("calm",  0 , 720, layer=0, priority=0, blendin=5, play_mode=logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1, blend_mode=logic.KX_ACTION_BLEND_BLEND)
    
    if wKey == kxa:
        scene.objects['Player.001']['postimer'] = 5
        OutsideEvents(True, 0.04)
        own.playAction("walk",  0 , 48, layer=0, priority=0, blendin=5, play_mode=logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1.3,  blend_mode=logic.KX_ACTION_BLEND_BLEND)

    if wKey == kxa and lshKey == kxa:
        OutsideEvents(True, 0.08)
        own.playAction("run",  0 , 24, layer=0, priority=0, blendin=3, play_mode=logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0,  speed=1, blend_mode=logic.KX_ACTION_BLEND_BLEND)
 
 

    
def Animation(user_event = non, name="calm", end = 720, movement = False, time = True):
    if user_event:
        own.playAction(name,  0 , end, 
        layer=0, 
        priority=0, 
        blendin=5, 
        play_mode=logic.KX_ACTION_MODE_LOOP, 
        layer_weight=0.0, 
        ipo_flags=0, 
        speed=1, 
        blend_mode=logic.KX_ACTION_BLEND_BLEND)
        
        if movement == False: 
            OutsideEvents(False, 0.04)
        if time ==True:
            scene.objects['Player.001']['postimer'] = 5
     
def OutsideEvents(cammove, spdX = 0, spdY = 0, spdZ = 0):
    scene = logic.getCurrentScene()
    scene.objects['Camera.000']['Free_Move'] = cammove
    scene.objects['Player.001'].applyMovement((spdY,spdX,spdZ), True)
    
    

    