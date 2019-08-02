import pygame
import os
import random
import math
import numpy

SCREEN_WIDTH, SCREEN_HEIGHT = 256, 256
MAX_AMPLITUDE = 255*2/5
MASTER_SEED = random.uniform(0, 1);


# --- PRNG ---

# no post-processing, takes an optional Z value to get a different set of random values for the same (X,Y), used for successive iterations
def deterministicRandom(x, y, z=0):
    random.seed(z+MASTER_SEED)
    random.seed(x*random.uniform(1,2)+MASTER_SEED)
    random.seed(y*random.uniform(1,2)+MASTER_SEED)
    result = random.uniform(-1, 1)
    return result


# smooths deterministicRandom(...) values, takes way too long and results are extremely bland so not recommended unless smooth noise is required
def smoothDeterministicRandom(x, y, z=0):
    corners = deterministicRandom(x-1,y-1,z) + deterministicRandom(x+1,y-1,z) + deterministicRandom(x-1,y+1,z) + deterministicRandom(x+1,y+1,z)
    sides = deterministicRandom(x-1,y,z) + deterministicRandom(x,y-1,z) + deterministicRandom(x+1,y,z) + deterministicRandom(x,y+1,z)

    return corners/16 + sides/8 + deterministicRandom(x, y, z)/4

# ------------


# --- INTERPOLATORS ---

# quickest but kinda harsh, not extremely bad though
def lerp(a, b, x):
    return a*(1-x) + b*x


# good smoothness and not too slow
def cosineInterpolation(a, b, x):
    ft = x * math.pi
    f = (1 - math.cos(ft)) * 0.5
    return a*(1-f) + b*f

# ---------------------

def getBlendModeFor(value):
    if(value<0):
        return pygame.BLEND_SUB
    else:
        return pygame.BLEND_ADD


def waitForInput():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


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


def pixelArrayAndInterpolateImg(screen, frequency, amplitude, randomizer, interpolator):
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            value = makeNoise(x, y, frequency, wOffset, hOffset, randomizer, interpolator)*amplitude

            [aux, aux, aux] = screen[x,y]
            if aux+value < 0:
                screen[x,y] = [0,0,0]
            elif aux+value > 255:
                screen[x,y] = [255,255,255]
            else:
                screen[x,y] = [aux+value, aux+value, aux+value]

    return screen


def frequencyFor(i):
    return 2**(i+1)


def amplitudeFor(i):
    return MAX_AMPLITUDE/(1.5**i)


def perlinNoise():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((127, 127, 127))
    os.system('call sendkeys.bat "pygame window" ""')

    i = 0
    # so we don't go below the actual screen resolution
    while frequencyFor(i) < SCREEN_WIDTH:
        print("Iteration {0}...".format(i))
        pixelArrayAndInterpolateDraw(screen, frequencyFor(i), amplitudeFor(i), deterministicRandom, cosineInterpolation)
        # displays screen
        pygame.display.flip()
        print("Done.")
        i+=1

    print("All done!")



def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    perlinNoise()
    waitForInput()
    pygame.quit()


if __name__ == "__main__":
    main()
