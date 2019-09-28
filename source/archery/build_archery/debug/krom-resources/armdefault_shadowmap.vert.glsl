#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform mat4 LWVP;

in vec4 pos;

void main()
{
    vec4 spos = vec4(pos.xyz, 1.0);
    gl_Position = LWVP * spos;
}

