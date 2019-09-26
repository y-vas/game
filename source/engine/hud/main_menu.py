from bge import logic, events, render

cont = logic.getCurrentController()
own = cont.owner
scene = logic.getCurrentScene()
SO = scene.objects
bar = SO['terminal_text']
frase = SO['text_terminal']
Hbar = SO['Plane.002']

menubar = SO['menu']
colist = [SO['col1'],SO['col2'],SO['col3'],SO['col4'],SO['col5'],SO['col6'],SO['col7'],SO['col8']]

def run():
    mouse = logic.mouse.events
    lmKey= mouse[events.LEFTMOUSE]
    esc = cont.sensors['ESC']
    f1 = cont.sensors['F1']

    contB = cont.sensors['continue']
    #save = cont.sensors['save_game']
    #load = cont.sensors['load_game']
    #options = cont.sensors['options']
    #extra = cont.sensors['extras']
    end = cont.sensors['end']

    keyEvents = logic.keyboard.events
    #bsKey = keyEvents[events.BACKSPACEKEY]
    hitKey = [k for k in keyEvents \
                if keyEvents[k] == logic.KX_INPUT_JUST_ACTIVATED]
    if end.positive:
        if lmKey == logic.KX_INPUT_JUST_ACTIVATED:
            logic.endGame()
    elif contB.positive:
        if lmKey == logic.KX_INPUT_JUST_ACTIVATED:
            menu(False)
    if esc.positive and own["pause"] == False:
        menu(True)
    elif esc.positive and own["pause"] == True:
        menu(False)

    if f1.positive and own ["terminal"] == True:
        own ["terminal"] = False
        bar.setVisible(False)
        own["word"] = ""
        frase.text = own["word"]
    elif f1.positive and own ["terminal"] == False:
        own ["terminal"] = True

    if own ["terminal"] == True:
        bar.setVisible(True)
        if hitKey != [] and hitKey != [13]:
            characterValue = events.EventToCharacter(hitKey[0], True)
            own["word"] += characterValue
        #elif bsKey == logic.KX_INPUT_JUST_ACTIVATED:
        #    own["word"] = ""       and hitKey != [133]

        elif hitKey == [13]:

            # COMANDOS ########################
            if own["word"] == "MASALUD":
                Hbar["health"] += 100
            elif own["word"] == "MISALUD":
                Hbar["health"] -= 100
            elif own["word"] == "SALUD":
                Hbar["health"] = 100
            elif own["word"] == "MAMANA":
                Hbar["mana"] += 100
            elif own["word"] == "MIMANA":
                Hbar["mana"] -= 100
            elif own["word"] == "MANA":
                Hbar["mana"] = 100
            elif own["word"] == "TOP":
                Hbar["mana"] = Hbar["health"] = 100
            elif own["word"] == "END":
                logic.endGame()
            else:
                logic.sendMessage("comand", own["word"])
            own["word"] = ""
        frase.text = own["word"]
        frase.resolution = 5

def menu(Vis = False):
    render.setMousePosition(int(render.getWindowWidth()/2), int(render.getWindowHeight()/2))
    logic.sendMessage("pause")
    render.showMouse(Vis)
    own["pause"] = Vis
    menubar.setVisible(Vis)
    for i in colist:
        i.setVisible(Vis)
        i.color=[0.5,0,0,True]
    MenuSection(0)

def MenuSection(option = 0):
    if option == 0: #Default
        SO['col1'].text = "Continuar"
        SO['col2'].text = "Guardar Partida"
        SO['col2'].text = "Cargar"
        SO['col3'].text = "Opciones"
        SO['col4'].text = "Configuracion"
        SO['col5'].text = "Extras"
        SO['col6'].text = "Menu Principal"
        SO['col7'].text = "Salir"
        SO['col8'].text = "Desarrollador"
    if option == 1: #Cargar Partida
        SO['col1'].text = "Continuar"
        SO['col2'].text = "Partida_x"
        SO['col2'].text = "Partida_x"
        SO['col3'].text = "Partida_x"
        SO['col4'].text = "Partida_x"
        SO['col5'].text = "Partida_x"
        SO['col6'].text = "Partida_x"
        SO['col7'].text = "Partida_x"
        SO['col8'].text = "Atras"
