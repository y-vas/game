#pragma once

#ifdef __cplusplus
extern "C" {
#endif

struct ID3D12Resource;
struct ID3D12DescriptorHeap;
struct ID3D12GraphicsCommandList;

typedef struct {
	int unit;
} TextureUnit5Impl;

typedef struct {
	bool mipmap;
	int stage;
	int stride;
	struct ID3D12Resource *image;
	struct ID3D12Resource *uploadImage;
	struct ID3D12DescriptorHeap *srvDescriptorHeap;
} Texture5Impl;

struct kinc_g5_texture;

void kinc_g5_internal_set_textures(struct ID3D12GraphicsCommandList *commandList);
void kinc_g5_internal_texture_set(struct kinc_g5_texture *texture, int unit);

#ifdef __cplusplus
}
#endif
