#version 330
#ifdef GL_ARB_shading_language_420pack
#extension GL_ARB_shading_language_420pack : require
#endif
#extension GL_ARB_shader_image_load_store : require

layout(r8) uniform writeonly image3D voxels;

in vec3 voxposition;

void main()
{
    bool _18 = abs(voxposition.z) > 0.5;
    bool _28;
    if (!_18)
    {
        _28 = abs(voxposition.x) > 1.0;
    }
    else
    {
        _28 = _18;
    }
    bool _37;
    if (!_28)
    {
        _37 = abs(voxposition.y) > 1.0;
    }
    else
    {
        _37 = _28;
    }
    if (_37)
    {
        return;
    }
    imageStore(voxels, ivec3(vec3(128.0, 128.0, 64.0) * ((voxposition * 0.5) + vec3(0.5))), vec4(1.0));
}

