#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform sampler2D texdepth;
uniform vec2 screenSizeInv;

in vec2 texCoord;
out float fragColor;

void main()
{
    float d0 = textureLod(texdepth, texCoord, 0.0).x;
    float d1 = textureLod(texdepth, texCoord + vec2(screenSizeInv.x, 0.0), 0.0).x;
    float d2 = textureLod(texdepth, texCoord + vec2(0.0, screenSizeInv.y), 0.0).x;
    float d3 = textureLod(texdepth, texCoord + vec2(screenSizeInv.x, screenSizeInv.y), 0.0).x;
    fragColor = max(max(d0, d1), max(d2, d3));
}

