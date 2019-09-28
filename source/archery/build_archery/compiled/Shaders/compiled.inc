#ifndef _COMPILED_GLSL_
#define _COMPILED_GLSL_
#define _Irr
#define _EnvSky
#define _Rad
#define _EnvStr
#define _Deferred
#define _ShadowMap
#define _CSM
#define _VoxelCones3
#define _VoxelAOvar
#define _Sun
#define _Brdf
#define _SMAA
#define _SSAO
#define _CToneFilmic
const float PI = 3.1415926535;
const float PI2 = PI * 2.0;
const vec2 shadowmapSize = vec2(2048, 2048);
const float shadowmapCubePcfSize = 0.001;
const int shadowmapCascades = 2;
const float ssaoRadius = 1.0;
const float ssaoStrength = 1.0;
const float ssaoScale = 20.0;
const float bloomThreshold = 1.0;
const float bloomStrength = 3.5;
const float bloomRadius = 3.0;
const float ssrRayStep = 0.04;
const float ssrMinRayStep = 0.05;
const float ssrSearchDist = 5.0;
const float ssrFalloffExp = 5.0;
const float ssrJitter = 0.6;
const int compoChromaticType = 0;
const ivec3 voxelgiResolution = ivec3(64, 64, 32);
const vec3 voxelgiHalfExtents = vec3(8, 8, 4);
const float voxelgiOcc = 1.0;
const float voxelgiStep = 1.0;
const float voxelgiRange = 2.0;
const float voxelgiOffset = 1.0;
const float voxelgiAperture = 1.0;
const int skinMaxBones = 65;

#endif // _COMPILED_GLSL_
