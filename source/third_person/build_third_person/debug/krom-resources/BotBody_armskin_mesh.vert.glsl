#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif

uniform vec4 skinBones[130];
uniform float posUnpack;
uniform mat3 N;
uniform mat4 WVP;

in vec4 pos;
in vec4 bone;
in vec4 weight;
out vec3 wnormal;
in vec2 nor;

void getSkinningDualQuat(ivec4 bone_1, inout vec4 weight_1, inout vec4 A, inout vec4 B)
{
    ivec4 bonei = bone_1 * ivec4(2);
    mat4 matA = mat4(vec4(skinBones[bonei.x]), vec4(skinBones[bonei.y]), vec4(skinBones[bonei.z]), vec4(skinBones[bonei.w]));
    mat4 matB = mat4(vec4(skinBones[bonei.x + 1]), vec4(skinBones[bonei.y + 1]), vec4(skinBones[bonei.z + 1]), vec4(skinBones[bonei.w + 1]));
    vec3 _129 = weight_1.xyz * sign(matA[3] * matA).xyz;
    weight_1 = vec4(_129.x, _129.y, _129.z, weight_1.w);
    A = matA * weight_1;
    B = matB * weight_1;
    float invNormA = 1.0 / length(A);
    A *= invNormA;
    B *= invNormA;
}

void main()
{
    vec4 spos = vec4(pos.xyz, 1.0);
    vec4 param = weight;
    vec4 skinB;
    vec4 param_2 = skinB;
    vec4 param_1;
    getSkinningDualQuat(ivec4(bone * 32767.0), param, param_1, param_2);
    vec4 skinA = param_1;
    skinB = param_2;
    vec3 _179 = spos.xyz * posUnpack;
    spos = vec4(_179.x, _179.y, _179.z, spos.w);
    vec3 _200 = spos.xyz + (cross(skinA.xyz, cross(skinA.xyz, spos.xyz) + (spos.xyz * skinA.w)) * 2.0);
    spos = vec4(_200.x, _200.y, _200.z, spos.w);
    vec3 _223 = spos.xyz + ((((skinB.xyz * skinA.w) - (skinA.xyz * skinB.w)) + cross(skinA.xyz, skinB.xyz)) * 2.0);
    spos = vec4(_223.x, _223.y, _223.z, spos.w);
    vec3 _230 = spos.xyz / vec3(posUnpack);
    spos = vec4(_230.x, _230.y, _230.z, spos.w);
    wnormal = normalize(N * (vec3(nor, pos.w) + (cross(skinA.xyz, cross(skinA.xyz, vec3(nor, pos.w)) + (vec3(nor, pos.w) * skinA.w)) * 2.0)));
    gl_Position = WVP * spos;
}

