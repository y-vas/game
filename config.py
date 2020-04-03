import math, sys

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16
WALKING_SPEED = 20
FLYING_SPEED = 50
GRAVITY = 20.0
MAX_JUMP_HEIGHT = 2.0 # About the height of a block.
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

if sys.version_info[0] >= 3:
    xrange = range

BG_COLOR = [1,1,1,1]
