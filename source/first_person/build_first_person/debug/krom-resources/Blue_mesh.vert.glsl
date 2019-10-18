#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform float texUnpack;
uniform mat3 N;
uniform mat4 WVP;

in vec4 pos;
out vec2 texCoord;
in vec2 tex;
out vec3 wnormal;
in vec2 nor;

void main()
{
    vec4 spos = vec4(pos.xyz, 1.0);
    texCoord = tex * texUnpack;
    wnormal = normalize(N * vec3(nor, pos.w));
    gl_Position = WVP * spos;
}

