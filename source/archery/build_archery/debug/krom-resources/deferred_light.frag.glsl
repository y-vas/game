#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform vec4 casData[12];
uniform vec4 shirr[7];
uniform sampler2D gbuffer0;
uniform sampler2D gbuffer1;
uniform sampler2D gbufferD;
uniform vec3 eye;
uniform vec3 eyeLook;
uniform vec2 cameraProj;
uniform sampler2D senvmapBrdf;
uniform int envmapNumMipmaps;
uniform sampler2D senvmapRadiance;
uniform float envmapStrength;
uniform sampler3D voxels;
uniform sampler2D ssaotex;
uniform vec3 sunDir;
uniform sampler2DShadow shadowMap;
uniform float shadowsBias;
uniform vec3 sunCol;

in vec2 texCoord;
in vec3 viewRay;
out vec4 fragColor;

vec3 _632;

vec2 octahedronWrap(vec2 v)
{
    return (vec2(1.0) - abs(v.yx)) * vec2((v.x >= 0.0) ? 1.0 : (-1.0), (v.y >= 0.0) ? 1.0 : (-1.0));
}

void unpackFloatInt16(float val, out float f, inout uint i)
{
    i = uint(int((val / 0.06250095367431640625) + 1.525902189314365386962890625e-05));
    f = clamp((((-0.06250095367431640625) * float(i)) + val) / 0.06248569488525390625, 0.0, 1.0);
}

vec2 unpackFloat2(float f)
{
    return vec2(floor(f) / 255.0, fract(f));
}

vec3 surfaceAlbedo(vec3 baseColor, float metalness)
{
    return mix(baseColor, vec3(0.0), vec3(metalness));
}

vec3 surfaceF0(vec3 baseColor, float metalness)
{
    return mix(vec3(0.039999999105930328369140625), baseColor, vec3(metalness));
}

vec3 getPos(vec3 eye_1, vec3 eyeLook_1, vec3 viewRay_1, float depth, vec2 cameraProj_1)
{
    float linearDepth = cameraProj_1.y / (((depth * 0.5) + 0.5) - cameraProj_1.x);
    float viewZDist = dot(eyeLook_1, viewRay_1);
    vec3 wposition = eye_1 + (viewRay_1 * (linearDepth / viewZDist));
    return wposition;
}

vec3 shIrradiance(vec3 nor)
{
    vec3 cl00 = vec3(shirr[0].x, shirr[0].y, shirr[0].z);
    vec3 cl1m1 = vec3(shirr[0].w, shirr[1].x, shirr[1].y);
    vec3 cl10 = vec3(shirr[1].z, shirr[1].w, shirr[2].x);
    vec3 cl11 = vec3(shirr[2].y, shirr[2].z, shirr[2].w);
    vec3 cl2m2 = vec3(shirr[3].x, shirr[3].y, shirr[3].z);
    vec3 cl2m1 = vec3(shirr[3].w, shirr[4].x, shirr[4].y);
    vec3 cl20 = vec3(shirr[4].z, shirr[4].w, shirr[5].x);
    vec3 cl21 = vec3(shirr[5].y, shirr[5].z, shirr[5].w);
    vec3 cl22 = vec3(shirr[6].x, shirr[6].y, shirr[6].z);
    return ((((((((((cl22 * 0.429042994976043701171875) * ((nor.y * nor.y) - ((-nor.z) * (-nor.z)))) + (((cl20 * 0.743125021457672119140625) * nor.x) * nor.x)) + (cl00 * 0.88622701168060302734375)) - (cl20 * 0.2477079927921295166015625)) + (((cl2m2 * 0.85808598995208740234375) * nor.y) * (-nor.z))) + (((cl21 * 0.85808598995208740234375) * nor.y) * nor.x)) + (((cl2m1 * 0.85808598995208740234375) * (-nor.z)) * nor.x)) + ((cl11 * 1.02332794666290283203125) * nor.y)) + ((cl1m1 * 1.02332794666290283203125) * (-nor.z))) + ((cl10 * 1.02332794666290283203125) * nor.x);
}

float getMipFromRoughness(float roughness, float numMipmaps)
{
    return roughness * numMipmaps;
}

vec2 envMapEquirect(vec3 normal)
{
    float phi = acos(normal.z);
    float theta = atan(-normal.y, normal.x) + 3.1415927410125732421875;
    return vec2(theta / 6.283185482025146484375, phi / 3.1415927410125732421875);
}

vec3 tangent(vec3 n)
{
    vec3 t1 = cross(n, vec3(0.0, 0.0, 1.0));
    vec3 t2 = cross(n, vec3(0.0, 1.0, 0.0));
    if (length(t1) > length(t2))
    {
        return normalize(t1);
    }
    else
    {
        return normalize(t2);
    }
}

float traceConeAO(sampler3D voxels_1, vec3 origin, inout vec3 dir, float aperture, float maxDist)
{
    dir = normalize(dir);
    float sampleCol = 0.0;
    float dist = 0.046875;
    float diam = dist * aperture;
    while ((sampleCol < 1.0) && (dist < maxDist))
    {
        vec3 samplePos = (dir * dist) + origin;
        float mip = max(log2(diam * 64.0), 0.0);
        float mipSample = textureLod(voxels_1, (samplePos * 0.5) + vec3(0.5), mip).x;
        sampleCol += ((1.0 - sampleCol) * mipSample);
        dist += max(diam / 2.0, 0.03125);
        diam = dist * aperture;
    }
    return sampleCol;
}

float traceAO(vec3 origin, vec3 normal, sampler3D voxels_1)
{
    vec3 o1 = normalize(tangent(normal));
    vec3 o2 = normalize(cross(o1, normal));
    vec3 c1 = (o1 + o2) * 0.5;
    vec3 c2 = (o1 - o2) * 0.5;
    vec3 param = normal;
    float _709 = traceConeAO(voxels_1, origin, param, 0.557851731777191162109375, 3.4641015529632568359375);
    float col = _709;
    vec3 param_1 = mix(normal, o1, vec3(0.5));
    float _714 = traceConeAO(voxels_1, origin, param_1, 0.557851731777191162109375, 3.4641015529632568359375);
    col += _714;
    vec3 param_2 = mix(normal, -c2, vec3(0.5));
    float _722 = traceConeAO(voxels_1, origin, param_2, 0.557851731777191162109375, 3.4641015529632568359375);
    col += _722;
    return (col / 3.0) * 0.89999997615814208984375;
}

vec3 lambertDiffuseBRDF(vec3 albedo, float nl)
{
    return albedo * max(0.0, nl);
}

float d_ggx(float nh, float a)
{
    float a2 = a * a;
    float denom = pow(((nh * nh) * (a2 - 1.0)) + 1.0, 2.0);
    return (a2 * 0.3183098733425140380859375) / denom;
}

float v_smithschlick(float nl, float nv, float a)
{
    return 1.0 / (((nl * (1.0 - a)) + a) * ((nv * (1.0 - a)) + a));
}

vec3 f_schlick(vec3 f0, float vh)
{
    return f0 + ((vec3(1.0) - f0) * exp2((((-5.554729938507080078125) * vh) - 6.9831600189208984375) * vh));
}

vec3 specularBRDF(vec3 f0, float roughness, float nl, float nh, float nv, float vh)
{
    float a = roughness * roughness;
    return (f_schlick(f0, vh) * (d_ggx(nh, a) * clamp(v_smithschlick(nl, nv, a), 0.0, 1.0))) / vec3(4.0);
}

mat4 getCascadeMat(float d, inout int casi, inout int casIndex)
{
    vec4 comp = vec4(float(d > casData[8].x), float(d > casData[8].y), float(d > casData[8].z), float(d > casData[8].w));
    casi = int(min(dot(vec4(1.0, 1.0, 0.0, 0.0), comp), 2.0));
    casIndex = casi * 4;
    return mat4(vec4(casData[casIndex]), vec4(casData[casIndex + 1]), vec4(casData[casIndex + 2]), vec4(casData[casIndex + 3]));
}

float PCF(sampler2DShadow shadowMap_1, vec2 uv, float compare, vec2 smSize)
{
    vec3 _289 = vec3(uv + (vec2(-1.0) / smSize), compare);
    float result = texture(shadowMap_1, vec3(_289.xy, _289.z));
    vec3 _298 = vec3(uv + (vec2(-1.0, 0.0) / smSize), compare);
    result += texture(shadowMap_1, vec3(_298.xy, _298.z));
    vec3 _309 = vec3(uv + (vec2(-1.0, 1.0) / smSize), compare);
    result += texture(shadowMap_1, vec3(_309.xy, _309.z));
    vec3 _320 = vec3(uv + (vec2(0.0, -1.0) / smSize), compare);
    result += texture(shadowMap_1, vec3(_320.xy, _320.z));
    vec3 _328 = vec3(uv, compare);
    result += texture(shadowMap_1, vec3(_328.xy, _328.z));
    vec3 _339 = vec3(uv + (vec2(0.0, 1.0) / smSize), compare);
    result += texture(shadowMap_1, vec3(_339.xy, _339.z));
    vec3 _350 = vec3(uv + (vec2(1.0, -1.0) / smSize), compare);
    result += texture(shadowMap_1, vec3(_350.xy, _350.z));
    vec3 _361 = vec3(uv + (vec2(1.0, 0.0) / smSize), compare);
    result += texture(shadowMap_1, vec3(_361.xy, _361.z));
    vec3 _372 = vec3(uv + (vec2(1.0) / smSize), compare);
    result += texture(shadowMap_1, vec3(_372.xy, _372.z));
    return result / 9.0;
}

float shadowTestCascade(sampler2DShadow shadowMap_1, vec3 eye_1, vec3 p, float shadowsBias_1)
{
    float d = distance(eye_1, p);
    int param;
    int param_1;
    mat4 _467 = getCascadeMat(d, param, param_1);
    int casi = param;
    int casIndex = param_1;
    mat4 LWVP = _467;
    vec4 lPos = LWVP * vec4(p, 1.0);
    vec3 _482 = lPos.xyz / vec3(lPos.w);
    lPos = vec4(_482.x, _482.y, _482.z, lPos.w);
    float visibility = 1.0;
    if (lPos.w > 0.0)
    {
        visibility = PCF(shadowMap_1, lPos.xy, lPos.z - shadowsBias_1, vec2(4096.0, 2048.0));
    }
    float nextSplit = casData[8][casi];
    float _508;
    if (casi == 0)
    {
        _508 = nextSplit;
    }
    else
    {
        _508 = nextSplit - (casData[8][casi - 1]);
    }
    float splitSize = _508;
    float splitDist = (nextSplit - d) / splitSize;
    if ((splitDist <= 0.1500000059604644775390625) && (casi != 1))
    {
        int casIndex2 = casIndex + 4;
        mat4 LWVP2 = mat4(vec4(casData[casIndex2]), vec4(casData[casIndex2 + 1]), vec4(casData[casIndex2 + 2]), vec4(casData[casIndex2 + 3]));
        vec4 lPos2 = LWVP2 * vec4(p, 1.0);
        vec3 _586 = lPos2.xyz / vec3(lPos2.w);
        lPos2 = vec4(_586.x, _586.y, _586.z, lPos2.w);
        float visibility2 = 1.0;
        if (lPos2.w > 0.0)
        {
            visibility2 = PCF(shadowMap_1, lPos2.xy, lPos2.z - shadowsBias_1, vec2(4096.0, 2048.0));
        }
        float lerpAmt = smoothstep(0.0, 0.1500000059604644775390625, splitDist);
        return mix(visibility2, visibility, lerpAmt);
    }
    return visibility;
}

void main()
{
    vec4 g0 = textureLod(gbuffer0, texCoord, 0.0);
    vec3 n;
    n.z = (1.0 - abs(g0.x)) - abs(g0.y);
    vec2 _907;
    if (n.z >= 0.0)
    {
        _907 = g0.xy;
    }
    else
    {
        _907 = octahedronWrap(g0.xy);
    }
    n = vec3(_907.x, _907.y, n.z);
    n = normalize(n);
    float roughness = g0.z;
    float param;
    uint param_1;
    unpackFloatInt16(g0.w, param, param_1);
    float metallic = param;
    uint matid = param_1;
    vec4 g1 = textureLod(gbuffer1, texCoord, 0.0);
    vec2 occspec = unpackFloat2(g1.w);
    vec3 albedo = surfaceAlbedo(g1.xyz, metallic);
    vec3 f0 = surfaceF0(g1.xyz, metallic);
    float depth = (textureLod(gbufferD, texCoord, 0.0).x * 2.0) - 1.0;
    vec3 p = getPos(eye, eyeLook, normalize(viewRay), depth, cameraProj);
    vec3 v = normalize(eye - p);
    float dotNV = max(dot(n, v), 0.0);
    vec2 envBRDF = textureLod(senvmapBrdf, vec2(roughness, 1.0 - dotNV), 0.0).xy;
    vec3 envl = shIrradiance(n);
    vec3 reflectionWorld = reflect(-v, n);
    float lod = getMipFromRoughness(roughness, float(envmapNumMipmaps));
    vec3 prefilteredColor = textureLod(senvmapRadiance, envMapEquirect(reflectionWorld), lod).xyz;
    envl *= albedo;
    envl += (((prefilteredColor * ((f0 * envBRDF.x) + vec3(envBRDF.y))) * 1.5) * occspec.y);
    envl *= (envmapStrength * occspec.x);
    vec3 voxpos = p / vec3(8.0, 8.0, 4.0);
    envl *= (1.0 - traceAO(voxpos, n, voxels));
    fragColor = vec4(envl.x, envl.y, envl.z, fragColor.w);
    vec3 _1068 = fragColor.xyz * textureLod(ssaotex, texCoord, 0.0).x;
    fragColor = vec4(_1068.x, _1068.y, _1068.z, fragColor.w);
    vec3 sh = normalize(v + sunDir);
    float sdotNH = dot(n, sh);
    float sdotVH = dot(v, sh);
    float sdotNL = dot(n, sunDir);
    float svisibility = 1.0;
    vec3 sdirect = lambertDiffuseBRDF(albedo, sdotNL) + (specularBRDF(f0, roughness, sdotNL, sdotNH, dotNV, sdotVH) * occspec.y);
    svisibility = shadowTestCascade(shadowMap, eye, p + ((n * shadowsBias) * 10.0), shadowsBias);
    vec3 _1125 = fragColor.xyz + ((sdirect * svisibility) * sunCol);
    fragColor = vec4(_1125.x, _1125.y, _1125.z, fragColor.w);
    fragColor.w = 1.0;
}

