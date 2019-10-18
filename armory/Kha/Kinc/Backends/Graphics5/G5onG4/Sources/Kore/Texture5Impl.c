#include "pch.h"

#include "Texture5Impl.h"

#include <kinc/graphics5/texture.h>

void kinc_g5_texture_init(kinc_g5_texture_t *texture, int width, int height, kinc_image_format_t format) {}
void kinc_g5_texture_init3d(kinc_g5_texture_t *texture, int width, int height, int depth, kinc_image_format_t format) {}
void kinc_g5_texture_init_from_image(kinc_g5_texture_t *texture, kinc_image_t *image) {}
void kinc_g5_texture_init_from_encoded_data(kinc_g5_texture_t *texture, void *data, int size, const char *format, bool readable) {}
void kinc_g5_texture_init_from_data(kinc_g5_texture_t *texture, void *data, int width, int height, int format, bool readable) {}
void kinc_g5_texture_destroy(kinc_g5_texture_t *texture) {}

// void Texture5Impl::unmipmap() {
//	mipmap = false;
//}

// void Graphics5::Texture::_set(TextureUnit unit) {}

// void Texture5Impl::unset() {}

uint8_t *kinc_g5_texture_lock(kinc_g5_texture_t *texture) {
	return NULL;
}

void kinc_g5_texture_unlock(kinc_g5_texture_t *texture) {}

void kinc_g5_texture_clear(kinc_g5_texture_t *texture, int x, int y, int z, int width, int height, int depth, unsigned color) {}

int kinc_g5_texture_stride(kinc_g5_texture_t *texture) {
	return 32;
}

void kinc_g5_texture_generate_mipmaps(kinc_g5_texture_t *texture, int levels) {}

void kinc_g5_texture_set_mipmap(kinc_g5_texture_t *texture, kinc_g5_texture_t *mipmap, int level) {}
