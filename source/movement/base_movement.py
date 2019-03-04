






print("dfasdf")

# import bge
# #Abbreviations:
# cont = bge.logic.getCurrentController()
# player = cont.owner
# keyboard = bge.logic.keyboard
#
#
# iAct = bge.logic.KX_INPUT_ACTIVE
# pvel = player.linearVelocity
# wkey = keyboard.events[bge.events.WKEY]
# skey = keyboard.events[bge.events.SKEY]
# akey = keyboard.events[bge.events.AKEY]
# dkey = keyboard.events[bge.events.DKEY]
#
#
# #Base values:
# #This is the base speed for character movement. Change only this and the whole script will remain proportional:
#
#
# bs = 10
#
#
# wmove = bs
# smove = -0.4*bs
# amove = -0.8*bs
# dmove = 0.8*bs
#
#
# awdmove = 0.6*bs
# asdmove = 0.3*bs
#
#
# #Always do this:
#
#
# player.setLinearVelocity((0, 0, 0), True)
# print(pvel)
#
#
# #Defining the groundMove function:
# def groundMove():
#
#     #Main Directions:
#     if iAct == wkey:
#         player.setLinearVelocity((0, wmove, 0), True)
#
#     if iAct == skey:
#         player.setLinearVelocity((0, smove, 0), True)
#
#     if iAct == akey:
#         player.setLinearVelocity((amove, 0, 0), True)
#
#     if iAct == dkey:
#         player.setLinearVelocity((dmove, 0, 0), True)
#
#     #Diagonal directions:
#     if iAct == wkey and dkey:
#         player.setLinearVelocity((awdmove, awdmove, 0), True)
#
#     if iAct == wkey and akey:
#         player.setLinearVelocity((-1 * awdmove, awdmove, 0), True)
#
#     if iAct == skey and dkey:
#         player.setLinearVelocity((asdmove, -1 * asdmove, 0), True)
#
#     if iAct == skey and akey:
#         player.setLinearVelocity((-1 * asdmove, -1 * asdmove, 0), True)
#
# groundMove()
