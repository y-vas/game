#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform mat4 P;
uniform sampler2D gbufferD;
uniform vec2 cameraProj;
uniform sampler2D gbuffer0;
uniform sampler2D gbuffer1;
uniform mat3 V3;
uniform sampler2D tex;

in vec3 viewRay;
in vec2 texCoord;
out vec4 fragColor;
float depth;
vec3 hitCoord;

vec2 octahedronWrap(vec2 v)
{
    return (vec2(1.0) - abs(v.yx)) * vec2((v.x >= 0.0) ? 1.0 : (-1.0), (v.y >= 0.0) ? 1.0 : (-1.0));
}

vec3 getPosView(vec3 viewRay_1, float depth_1, vec2 cameraProj_1)
{
    float linearDepth = cameraProj_1.y / (cameraProj_1.x - depth_1);
    return viewRay_1 * linearDepth;
}

float rand(vec2 co)
{
    return fract(sin(dot(co, vec2(12.98980045318603515625, 78.233001708984375))) * 43758.546875);
}

vec2 getProjectedCoord(vec3 hit)
{
    vec4 projectedCoord = P * vec4(hit, 1.0);
    vec2 _98 = projectedCoord.xy / vec2(projectedCoord.w);
    projectedCoord = vec4(_98.x, _98.y, projectedCoord.z, projectedCoord.w);
    vec2 _106 = (projectedCoord.xy * 0.5) + vec2(0.5);
    projectedCoord = vec4(_106.x, _106.y, projectedCoord.z, projectedCoord.w);
    return projectedCoord.xy;
}

float getDeltaDepth(vec3 hit)
{
    depth = (textureLod(gbufferD, getProjectedCoord(hit), 0.0).x * 2.0) - 1.0;
    vec3 viewPos = getPosView(viewRay, depth, cameraProj);
    return viewPos.z - hit.z;
}

vec4 binarySearch(inout vec3 dir)
{
    vec3 start = hitCoord;
    float ddepth;
    for (int i = 0; i < 7; i++)
    {
        dir *= 0.5;
        hitCoord -= dir;
        vec3 _164 = hitCoord;
        float _165 = getDeltaDepth(_164);
        ddepth = _165;
        if (ddepth < 0.0)
        {
            hitCoord += dir;
        }
    }
    if (abs(ddepth) > 0.00999999977648258209228515625)
    {
        return vec4(0.0);
    }
    return vec4(getProjectedCoord(hitCoord), 0.0, 1.0);
}

vec4 rayCast(inout vec3 dir)
{
    dir *= 0.039999999105930328369140625;
    for (int i = 0; i < 18; i++)
    {
        hitCoord += dir;
        vec3 _206 = hitCoord;
        float _207 = getDeltaDepth(_206);
        if (_207 > 0.0)
        {
            vec3 param = dir;
            vec4 _213 = binarySearch(param);
            return _213;
        }
    }
    return vec4(0.0);
}

void main()
{
    vec4 g0 = textureLod(gbuffer0, texCoord, 0.0);
    float roughness = g0.z;
    if (roughness == 1.0)
    {
        fragColor = vec4(vec3(0.0).x, vec3(0.0).y, vec3(0.0).z, fragColor.w);
        return;
    }
    float spec = fract(textureLod(gbuffer1, texCoord, 0.0).w);
    if (spec == 0.0)
    {
        fragColor = vec4(vec3(0.0).x, vec3(0.0).y, vec3(0.0).z, fragColor.w);
        return;
    }
    float d = (textureLod(gbufferD, texCoord, 0.0).x * 2.0) - 1.0;
    if (d == 1.0)
    {
        fragColor = vec4(vec3(0.0).x, vec3(0.0).y, vec3(0.0).z, fragColor.w);
        return;
    }
    vec2 enc = g0.xy;
    vec3 n;
    n.z = (1.0 - abs(enc.x)) - abs(enc.y);
    vec2 _284;
    if (n.z >= 0.0)
    {
        _284 = enc;
    }
    else
    {
        _284 = octahedronWrap(enc);
    }
    n = vec3(_284.x, _284.y, n.z);
    n = normalize(n);
    vec3 viewNormal = V3 * n;
    vec3 viewPos = getPosView(viewRay, d, cameraProj);
    vec3 reflected = normalize(reflect(viewPos, viewNormal));
    hitCoord = viewPos;
    vec3 dir = (reflected * (1.0 - ((rand(texCoord) * 0.60000002384185791015625) * roughness))) * 2.0;
    vec3 param = dir;
    vec4 _328 = rayCast(param);
    vec4 coords = _328;
    vec2 deltaCoords = abs(vec2(0.5) - coords.xy);
    float screenEdgeFactor = clamp(1.0 - (deltaCoords.x + deltaCoords.y), 0.0, 1.0);
    float reflectivity = 1.0 - roughness;
    float intensity = (((pow(reflectivity, 5.0) * screenEdgeFactor) * clamp(-reflected.z, 0.0, 1.0)) * clamp((5.0 - length(viewPos - hitCoord)) * 0.20000000298023223876953125, 0.0, 1.0)) * coords.w;
    intensity = clamp(intensity, 0.0, 1.0);
    vec3 reflCol = textureLod(tex, coords.xy, 0.0).xyz;
    reflCol = clamp(reflCol, vec3(0.0), vec3(1.0));
    vec3 _385 = (reflCol * intensity) * 0.5;
    fragColor = vec4(_385.x, _385.y, _385.z, fragColor.w);
}

