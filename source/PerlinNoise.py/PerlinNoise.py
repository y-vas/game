import pygame
import os
import random
import math
import numpy

MASTER_SEED = random.uniform(0, 1);

def makeNoise(x, y, z, wOffset, hOffset, randomizer, interpolator):
    prevX = math.floor(x/wOffset)
    nextX = (math.floor(x/wOffset)+1)
    prevY = math.floor(y/hOffset)
    nextY = (math.floor(y/hOffset)+1)
    fractionX = (x%wOffset)/wOffset
    fractionY = (y%hOffset)/hOffset

    v1 = randomizer(prevX,prevY,z)
    v2 = randomizer(nextX,prevY,z)
    v3 = randomizer(prevX,nextY,z)
    v4 = randomizer(nextX,nextY,z)

    i1 = interpolator(v1, v2, fractionX)
    i2 = interpolator(v3, v4, fractionX)

    return interpolator(i1, i2, fractionY)


def pixelArrayAndInterpolateDraw(screen, frequency, amplitude, randomizer, interpolator):
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    screenArray = pygame.surfarray.pixels3d(screen)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            value = makeNoise(x, y, frequency, wOffset, hOffset, randomizer, interpolator)*amplitude

            (aux, aux, aux) = screenArray[x][y]
            if aux+value < 0:
                screenArray[x,y] = (0,0,0)
            elif aux+value > 255:
                screenArray[x,y] = (255,255,255)
            else:
                screenArray[x,y] = (aux+value, aux+value, aux+value)
