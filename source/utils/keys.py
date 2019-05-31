from bge import logic

keyboard = logic.keyboard.events

def presed(key):
    return keyboard[key] == logic.KX_INPUT_JUST_ACTIVATED
