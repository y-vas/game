#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform sampler2D gbuffer0;
uniform sampler2D tex;
uniform vec2 dirInv;

in vec2 texCoord;
out vec4 fragColor;

void main()
{
    float roughness = textureLod(gbuffer0, texCoord, 0.0).z;
    if (roughness >= 0.800000011920928955078125)
    {
        vec3 _37 = textureLod(tex, texCoord, 0.0).xyz;
        fragColor = vec4(_37.x, _37.y, _37.z, fragColor.w);
        return;
    }
    vec3 _50 = textureLod(tex, texCoord + (dirInv * 2.5), 0.0).xyz;
    fragColor = vec4(_50.x, _50.y, _50.z, fragColor.w);
    vec3 _63 = fragColor.xyz + textureLod(tex, texCoord + (dirInv * 1.5), 0.0).xyz;
    fragColor = vec4(_63.x, _63.y, _63.z, fragColor.w);
    vec3 _72 = fragColor.xyz + textureLod(tex, texCoord, 0.0).xyz;
    fragColor = vec4(_72.x, _72.y, _72.z, fragColor.w);
    vec3 _84 = fragColor.xyz + textureLod(tex, texCoord - (dirInv * 1.5), 0.0).xyz;
    fragColor = vec4(_84.x, _84.y, _84.z, fragColor.w);
    vec3 _96 = fragColor.xyz + textureLod(tex, texCoord - (dirInv * 2.5), 0.0).xyz;
    fragColor = vec4(_96.x, _96.y, _96.z, fragColor.w);
    vec3 _103 = fragColor.xyz / vec3(5.0);
    fragColor = vec4(_103.x, _103.y, _103.z, fragColor.w);
}

