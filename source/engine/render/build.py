from bgl import *

class PostDraw():
	def __init__(self, vertices, faces, properties ,vertex_shader = "", fragment_shader = ""):
		self.VERTICES = vertices
		self.FACES = faces
		self.PROGRAM = glCreateProgram();
		self.PROPERETIES = properties;

		if len(vertex_shader) == 0:
			vertex_shader = self.__default_vertex_shader();

		if len(fragment_shader) == 0:
			fragment_shader = self.__default_fragment_shader();

		shaderVert = self.__compile_shader(GL_VERTEX_SHADER,vertex_shader)
		shaderFrag = self.__compile_shader(GL_FRAGMENT_SHADER,fragment_shader)

		glAttachShader(self.PROGRAM, shaderVert)
		glAttachShader(self.PROGRAM, shaderFrag)

		glLinkProgram(self.PROGRAM)

		glDeleteShader(shaderVert);
		glDeleteShader(shaderFrag);


	def __object(self):

		glUseProgram(self.PROGRAM);

		for k,v in self.PROPERETIES.items():
			glUniform1f(glGetUniformLocation(self.PROGRAM, k), v);
			pass

		for face in self.FACES:
			glBegin(GL_POLYGON)
			for v in face:
				vert = self.VERTICES[v]
				glVertex3f (vert.x, vert.y, vert.z);
				
			glEnd();

		glUseProgram(0)

		# whatch BACKFACE CULLING

		glEnable(GL_CULL_FACE);
		glCullFace(GL_BACK);
		glFrontFace(GL_CCW);
		# glEnable(GL_RASTERIZER_DISCARD)

	def __compile_shader(self, shader_type, shader_source):
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
	    start[0] = 0
	    glGetShaderInfoLog(shader, success[0]+1,start, log)
	    py_log = log[:]
	    py_log_str = ""
	    for c in py_log:
	        py_log_str += str(chr(c))
	    print(str(py_log_str));
	    return shader

	def use(self,scene):
		scene.post_draw = [self.__object]

	def __default_fragment_shader(self):
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
		return FragmentShader;

	def __default_vertex_shader(self):
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
		return VertexShader;
