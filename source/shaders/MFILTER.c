uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

const int NUM_SAMPLES = 100;
const float density = 0.5;

void main(){
  vec2 deltaTexCoord = gl_TexCoord[3].st - vec2(0.8,0.5);
	vec2 texCoo = gl_TexCoord[0].st;
  vec4 texcolor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
  float gray = dot(texcolor.rgb, vec3(0.299, 0.587, 0.114));

	deltaTexCoord *= 1.0 / float(NUM_SAMPLES) * density;
	vec4 sample = vec4(3.0);
	float decay = 5.0;

  for(int i=0; i < NUM_SAMPLES ; i++){
  	texCoo -= deltaTexCoord;
    sample += texture2D(bgl_RenderedTexture, texCoo);
  }
  
  gl_FragColor = vec4(gray * vec3(0.8, 1.0, 1.2), texcolor.a)*sample/float(NUM_SAMPLES);
  gl_FragColor.a = 1.0;
}
