#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform sampler2D gbufferD;
uniform sampler2D gbuffer0;
uniform vec3 eyeLook;
uniform vec2 cameraProj;
uniform vec2 screenSize;
uniform vec3 eye;
uniform mat4 invVP;

in vec2 texCoord;
out float fragColor;
in vec3 viewRay;

vec2 octahedronWrap(vec2 v)
{
    return (vec2(1.0) - abs(v.yx)) * vec2((v.x >= 0.0) ? 1.0 : (-1.0), (v.y >= 0.0) ? 1.0 : (-1.0));
}

vec3 getPosNoEye(vec3 eyeLook_1, vec3 viewRay_1, float depth, vec2 cameraProj_1)
{
    float linearDepth = cameraProj_1.y / (((depth * 0.5) + 0.5) - cameraProj_1.x);
    float viewZDist = dot(eyeLook_1, viewRay_1);
    vec3 wposition = viewRay_1 * (linearDepth / viewZDist);
    return wposition;
}

vec3 getPos2NoEye(vec3 eye_1, mat4 invVP_1, float depth, vec2 coord)
{
    vec4 pos = vec4((coord * 2.0) - vec2(1.0), depth, 1.0);
    pos = invVP_1 * pos;
    vec3 _87 = pos.xyz / vec3(pos.w);
    pos = vec4(_87.x, _87.y, _87.z, pos.w);
    return pos.xyz - eye_1;
}

void main()
{
    float depth = (textureLod(gbufferD, texCoord, 0.0).x * 2.0) - 1.0;
    if (depth == 1.0)
    {
        fragColor = 1.0;
        return;
    }
    vec2 enc = textureLod(gbuffer0, texCoord, 0.0).xy;
    vec3 n;
    n.z = (1.0 - abs(enc.x)) - abs(enc.y);
    vec2 _136;
    if (n.z >= 0.0)
    {
        _136 = enc;
    }
    else
    {
        _136 = octahedronWrap(enc);
    }
    n = vec3(_136.x, _136.y, n.z);
    n = normalize(n);
    vec3 vray = normalize(viewRay);
    vec3 currentPos = getPosNoEye(eyeLook, vray, depth, cameraProj);
    float currentDistance = length(currentPos);
    float currentDistanceA = (currentDistance * 20.0) * 1.0;
    float currentDistanceB = currentDistance * 0.0005000000237487256526947021484375;
    ivec2 px = ivec2(texCoord * screenSize);
    float phi = float(((3 * px.x) ^ (px.y + (px.x * px.y))) * 10);
    fragColor = 0.0;
    for (int i = 0; i < 8; i++)
    {
        float theta = (0.785398185253143310546875 * (float(i) + 0.5)) + phi;
        vec2 k = vec2(cos(theta), sin(theta)) / vec2(currentDistanceA);
        depth = (textureLod(gbufferD, texCoord + k, 0.0).x * 2.0) - 1.0;
        vec3 pos = getPos2NoEye(eye, invVP, depth, texCoord + k) - currentPos;
        fragColor += (max(0.0, dot(pos, n) - currentDistanceB) / (dot(pos, pos) + 0.014999999664723873138427734375));
    }
    fragColor *= 0.037500001490116119384765625;
    fragColor = 1.0 - fragColor;
}

