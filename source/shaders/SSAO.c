uniform sampler2D bgl_DepthTexture;
uniform sampler2D bgl_RenderedTexture;
uniform float bgl_RenderedTextureWidth;
uniform float bgl_RenderedTextureHeight;

#define PI    3.14159265

float width = bgl_RenderedTextureWidth; //texture width
float height = bgl_RenderedTextureHeight; //texture height

vec2 texCoord = gl_TexCoord[0].st;

//--------------------------------------------------------------------------------------------------------------------
//make sure that these two values are the same for your camera, otherwise distances will be wrong.

float znear = 0.5; //Z-near
float zfar = 1000.0; //Z-far

//user variables
int samples = 30; //ao sample count

float radius = 2.0; //ao radius
float aoclamp = 0.7; //depth clamp - reduces haloing at screen edges
bool noise = true; //use noise instead of pattern for sample dithering
float noiseamount = 0.0002; //dithering amount

float diffarea = 0.4; //self-shadowing reduction
float gdisplace = 0.4; //gauss bell center
float aowidth = 8.0; //gauss bell width

bool mist = true; //use mist?
float miststart = 0.5; //mist start
float mistend = zfar/2; //mist end

bool onlyAO = false; //use only ambient occlusion pass?
float lumInfluence = 0.1; //how much luminance affects occlusion

//--------------------------------------------------------------------------------------------------------------------

vec2 rand(vec2 coord) //generating noise/pattern texture for dithering
{
	float noiseX = ((fract(1.0-coord.s*(width/2.0))*0.25)+(fract(coord.t*(height/2.0))*0.75))*2.0-1.0;
	float noiseY = ((fract(1.0-coord.s*(width/2.0))*0.75)+(fract(coord.t*(height/2.0))*0.25))*2.0-1.0;

	if (noise)
	{
		noiseX = clamp(fract(sin(dot(coord ,vec2(12.9898,78.233))) * 43758.5453),0.0,1.0)*2.0-1.0;
		noiseY = clamp(fract(sin(dot(coord ,vec2(12.9898,78.233)*2.0)) * 43758.5453),0.0,1.0)*2.0-1.0;
	}
	return vec2(noiseX,noiseY)*noiseamount;
}

float doMist()
{
	float zdepth = texture2D(bgl_DepthTexture,texCoord.xy).x;
	float depth = -zfar * znear / (zdepth * (zfar - znear) - zfar);
	return clamp((depth-miststart)/mistend,0.0,1.0);
}

float readDepth(in vec2 coord)
{
	coord.x = clamp(coord.x,0.001,0.999);
    coord.y = clamp(coord.y,0.001,0.999);
	return (2.0 * znear) / (zfar + znear - texture2D(bgl_DepthTexture, coord ).x * (zfar-znear));
}

float compareDepths(in float depth1, in float depth2,inout int far)
{
	float garea = aowidth; //gauss bell width
	float diff = (depth1 - depth2)*100.0; //depth difference (0-100)
	//reduce left bell width to avoid self-shadowing
	if (diff<gdisplace)
	{
	garea = diffarea;
	}else{
	far = 1;
	}

	float gauss = pow(2.7182,-2.0*(diff-gdisplace)*(diff-gdisplace)/(garea*garea));
	return gauss;
}

float calAO(float depth,float dw, float dh)
{
	//float dd = (1.0-depth)*radius;
	float dd = radius;
	float temp = 0.0;
	float temp2 = 0.0;
	float coordw = gl_TexCoord[0].x + dw*dd;
	float coordh = gl_TexCoord[0].y + dh*dd;
	float coordw2 = gl_TexCoord[0].x - dw*dd;
	float coordh2 = gl_TexCoord[0].y - dh*dd;

	vec2 coord = vec2(coordw , coordh);
	vec2 coord2 = vec2(coordw2, coordh2);

	int far = 0;
	temp = compareDepths(depth, readDepth(coord),far);
	//DEPTH EXTRAPOLATION:
	if (far > 0)
	{
		temp2 = compareDepths(readDepth(coord2),depth,far);
		temp += (1.0-temp)*temp2;
	}

	return temp;
}

void main(void)
{
	vec2 noise = rand(texCoord);
	float depth = readDepth(texCoord);

	float w = (1.0 / width)/clamp(depth,aoclamp,1.0)+(noise.x*(1.0-noise.x));
	float h = (1.0 / height)/clamp(depth,aoclamp,1.0)+(noise.y*(1.0-noise.y));

	float pw;
	float ph;

	float ao;

	float dl = PI*(3.0-sqrt(5.0));
	float dz = 1.0/float(samples);
	float l = 0.0;
	float z = 1.0 - dz/2.0;

	for (int i = 0; i <= samples; i ++)
	{
		float r = sqrt(1.0-z);

		pw = cos(l)*r;
		ph = sin(l)*r;
		ao += calAO(depth,pw*w,ph*h);
		z = z - dz;
		l = l + dl;
	}

	ao /= float(samples);
	ao = 1.0-ao;

	if (mist) {ao = mix(ao, 1.0,doMist()); }

	vec3 color = texture2D(bgl_RenderedTexture,texCoord).rgb;

	vec3 lumcoeff = vec3(0.299,0.587,0.114);
	float lum = dot(color.rgb, lumcoeff);
	vec3 luminance = vec3(lum, lum, lum);

	vec3 final = vec3(color*mix(vec3(ao),vec3(1.0),luminance*lumInfluence));//mix(color*ao, white, luminance)

	if (onlyAO) {final = vec3(mix(vec3(ao),vec3(1.0),luminance*lumInfluence));}//ambient occlusion only

	gl_FragColor = vec4(final,1.0);

}
