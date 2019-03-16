from bgl import *
import bge

## use it as a module the post draw thing
## also add a timer

sce = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
own = cont.owner

shaderVertString = """
void main()
{
    gl_Position = ftransform();
}
"""

shaderFragString = """
uniform float timer;
void main()
{
    gl_FragColor = vec4(1.0, sin(timer), 1.0, 1.0);
}
"""

def shaderStuff():

    own["program"] = glCreateProgram()

    shaderVert = glCreateShader(GL_VERTEX_SHADER)
    shaderFrag = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(shaderVert, shaderVertString)
    glShaderSource(shaderFrag, shaderFragString)

    glCompileShader(shaderVert)
    glCompileShader(shaderFrag)

    glAttachShader(own["program"], shaderVert)
    glAttachShader(own["program"], shaderFrag)

    glLinkProgram(own["program"])

    glDeleteShader(shaderVert)
    glDeleteShader(shaderFrag)

shaderStuff()

def triangle():

    glUseProgram(own["program"])
    glUniform1f(glGetUniformLocation(own["program"], "timer"), own["timer"])
    glBegin(GL_TRIANGLES)
    glVertex3f(-10,0, 0)
    glVertex3f(10,0, 0)
    glVertex3f(0,0, 10)
    glEnd()
    glUseProgram(0)

def postDrawTriangle():

    sce.post_draw = [triangle]
