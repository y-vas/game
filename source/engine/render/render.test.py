import bge
from bgl import *
from bge import events, texture

## use it as a module the post draw thing
## also add a timer

sce = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
own = cont.owner

VertexShader = """
attribute vec4 Tangent;
varying vec4 fragPos;
varying vec3 T, B, N; //tangent binormal normal
varying vec3 viewPos;
varying vec2 texCoord;

void main() {
	vec3 pos = vec3(gl_Vertex);

	T   = Tangent.xyz;
	B   = cross(gl_Normal, Tangent.xyz);
	N   = gl_Normal;

    texCoord = gl_MultiTexCoord0.xy;
    fragPos = ftransform();
    viewPos = pos - gl_ModelViewMatrixInverse[3].xyz;
    gl_Position = ftransform();
}

"""

FragmentShader = """

varying vec3 viewPos;
varying vec4 fragPos;
uniform float timer;
vec4 circle(vec2 uv, vec2 pos, float rad, vec3 color) {
	float d = length((pos) - uv) - rad;
	float t = clamp(d, 0.0, 2.0);
	return vec4(color, 1.0 - t);
}
void main() {
    vec4 color = vec4(0.0);
    vec4 black = vec4(0.0);
    vec4 red = vec4(1.0, 0.0, 0.0, 1.0);

    vec2 p = viewPos/vec2(20, 20);
    int val = int(floor(p.x-sin(timer)) + floor(p.y-cos(timer)));

    val = abs(val);

    if( val % 2 == 1) color = black;
    else  color = red;

    vec2 uv = fragPos.xy;
	vec3 orange = vec3(1.0, 0.5, 0.3);
	vec4 circle = circle(viewPos, fragPos.xy/1000 , tan(timer)*0.4, orange);
    vec4 col = 0.5 + 0.5*sin(timer+vec4(0,2,4,0));
	gl_FragColor = mix(color, circle, circle.a);

}
"""

def compile_shader(shader_type, shader_source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_source)
    glCompileShader(shader)
    success = Buffer(GL_INT, [1])
    glGetShaderiv(shader, GL_COMPILE_STATUS, success)
    if (success[0] == GL_TRUE):
        return shader
    glGetShaderiv(shader, GL_INFO_LOG_LENGTH, success);
    success[0] = success[0] + 1
    log = Buffer(GL_BYTE, [success[0]])
    start = Buffer(GL_INT, [1])
    start[0] =0
    glGetShaderInfoLog(shader, success[0]+1,start, log)
    py_log = log[:]
    py_log_str = ""
    for c in py_log:
        py_log_str += str(chr(c))
    print(str(py_log_str))
    return shader

def load_shaders(vertex_shader, fragment_shader):

    own["program"] = glCreateProgram()

    shaderVert = compile_shader(GL_VERTEX_SHADER,vertex_shader)
    shaderFrag = compile_shader(GL_FRAGMENT_SHADER,fragment_shader)

    glAttachShader(own["program"], shaderVert)
    glAttachShader(own["program"], shaderFrag)

    glLinkProgram(own["program"])

    glDeleteShader(shaderVert)
    glDeleteShader(shaderFrag)

load_shaders(VertexShader,FragmentShader)

def triangle():
    glUseProgram(own["program"])
    glUniform1f(glGetUniformLocation(own["program"], "timer"), own["timer"])
    #glUniform1i(glGetUniformLocation(own["program"],"reflectionSampler",), 1)
    #glUniform1i(glGetUniformLocation(own["program"],"refractionSampler",), 0)
    #glUniform1i(glGetUniformLocation(own["program"],"normalSampler",), 2)
    '''
    objbuf = texture.imageToArray(texture.ImageFFmpeg( bge.logic.expandPath("//source//textures//105.jpg")), "RGBA")

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glBlendFunc(GL_ONE,GL_ONE_MINUS_SRC_ALPHA)
    texBuf = Buffer(GL_INT, 1)
    glGenTextures(1, texBuf)
    glActiveTexture(GL_TEXTURE)
    glBindTexture(GL_TEXTURE_2D, texBuf.to_list()[0])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 512, 512,0, GL_RGBA, GL_UNSIGNED_BYTE, objbuf)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR)
            '''
    wid = 50
    glBegin(GL_POLYGON)
    glVertex3f (0,0, 1.0)
    glVertex3f (wid,0, 1.0)
    glVertex3f (wid,wid, 1.0)
    glVertex3f (0,wid, 1.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f (0,0, 20.0)
    glVertex3f (wid,0, 20.0)
    glVertex3f (wid,wid, 20.0)
    glVertex3f (0,wid, 20.0)
    glEnd()

    '''
    glDeleteTextures(1, texBuf)
    glDisable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)
    '''
    glUseProgram(0)

def postDrawTriangle():
    sce.post_draw = [triangle]
