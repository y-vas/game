import pygame as pg
from src.object import Object
from time import time

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    print("The GLCUBE example requires PyOpenGL")
    raise SystemExit


start_time = time()

obj = Object(
    size = 5,
    points= 11
)

obj.mkobj( strech = 5 )
obj.cercle(3)


CUBE_POINTS = obj.verts
CUBE_COLORS = obj.colors()
CUBE_QUAD_VERTS = ()
CUBE_EDGES = obj.edges

print(CUBE_COLORS)
exit()

def drawcube():
    global start_time
    global CUBE_POINTS ,CUBE_COLORS ,CUBE_QUAD_VERTS, CUBE_EDGES

    if start_time <= time() - 1:
        start_time = time()

        obj.cercle(3)
        CUBE_POINTS = obj.verts
        CUBE_COLORS = obj.colors()
        CUBE_QUAD_VERTS = ()
        CUBE_EDGES = obj.edges

    allpoints = list(zip(CUBE_POINTS, CUBE_COLORS))

    glBegin(GL_QUADS)
    for face in CUBE_QUAD_VERTS:
        for vert in face:
            pos, color = allpoints[vert]
            glColor3fv(color)
            glVertex3fv(pos)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex3fv(pos)

    glEnd()


def init_gl_stuff():
    glEnable(GL_DEPTH_TEST)  # use our zbuffer
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(450.0, 640 / 480.0, 0.1, 1000.0)  # setup lens
    glTranslatef(0.0, 0, -40.0)  # move back
    glRotatef(0, 0, 1, 0)  # orbit higher


def main():
    "run the demo"
    # initialize pygame and setup an opengl display
    pg.init()

    fullscreen = True
    pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF )

    init_gl_stuff()

    going = True
    while going:
        # check for quit'n events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                going = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")

                        pg.display.set_mode(
                            (640, 480), pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN
                        )

                    else:
                        print("Changing to windowed mode")
                        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)

                    fullscreen = not fullscreen
                    init_gl_stuff()

        # clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # orbit camera around by 1 degree
        glRotatef(1, 0, 0, 1)

        drawcube()
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()
