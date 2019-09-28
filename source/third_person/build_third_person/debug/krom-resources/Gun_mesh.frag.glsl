#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform sampler2D ImageTexture;

in vec3 wnormal;
in vec2 texCoord;
out vec4 fragColor[2];

vec2 octahedronWrap(vec2 v)
{
    return (vec2(1.0) - abs(v.yx)) * vec2((v.x >= 0.0) ? 1.0 : (-1.0), (v.y >= 0.0) ? 1.0 : (-1.0));
}

float packFloatInt16(float f, uint i)
{
    return (0.06248569488525390625 * f) + (0.06250095367431640625 * float(i));
}

float packFloat2(float f1, float f2)
{
    return floor(f1 * 255.0) + min(f2, 0.9900000095367431640625);
}

void main()
{
    vec3 n = normalize(wnormal);
    vec4 ImageTexture_texread_store = texture(ImageTexture, texCoord);
    vec3 ImageTexture_Color_res = ImageTexture_texread_store.xyz;
    vec3 basecol = vec3(0.19944994151592254638671875, 0.1791395246982574462890625, 0.930111110210418701171875);
    float roughness = ImageTexture_Color_res.x;
    float metallic = 0.0;
    float occlusion = 1.0;
    float specular = 1.0;
    n /= vec3((abs(n.x) + abs(n.y)) + abs(n.z));
    vec2 _112;
    if (n.z >= 0.0)
    {
        _112 = n.xy;
    }
    else
    {
        _112 = octahedronWrap(n.xy);
    }
    n = vec3(_112.x, _112.y, n.z);
    fragColor[0] = vec4(n.xy, roughness, packFloatInt16(metallic, 0u));
    fragColor[1] = vec4(basecol, packFloat2(occlusion, specular));
}

