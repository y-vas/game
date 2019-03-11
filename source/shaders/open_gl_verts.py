import bgl
from bgl import *
from bge import logic as gl
import math

scene = gl.getCurrentScene()
cam = scene.active_camera;
#mt = math.sin(cam["ti"])

def display():
    glClear (bgl.GL_COLOR_BUFFER_BIT);
    glColor3f (1.0, 0.0, 0.0)
    glBegin(bgl.GL_POLYGON)
    glVertex3f (0.25, 0.25, 0.0)
    glVertex3f (0.75, 0.25, 0.0)
    glVertex3f (0.75, 0.75, 0.0)
    glVertex3f (0.25, 0.75, 0.0)
    glEnd()
#/* don\u2019t wait!
#  * start processing buffered OpenGL routines
#  */
    glFlush()

def init():
    glClearColor (0.0, 0.0, 0.0, 0.0);
    glMatrixMode(bgl.GL_PROJECTION);
    glLoadIdentity();
    glOrtho(mt, 1.0, 0.0, 1.0, -1.0, 1.0);

scene.post_draw = [init]
scene.post_draw = [display]
