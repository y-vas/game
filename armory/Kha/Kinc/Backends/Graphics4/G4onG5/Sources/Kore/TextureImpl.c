#include "pch.h"

#include <kinc/graphics4/graphics.h>
#include <kinc/graphics4/texture.h>
#include <kinc/graphics5/texture.h>
#include <kinc/io/filereader.h>

#include "TextureImpl.h"

void kinc_g4_texture_init_from_image(kinc_g4_texture_t *texture, kinc_image_t *image) {
	texture->impl._uploaded = false;
	kinc_g5_texture_init_from_image(&texture->impl._texture, image);
	texture->tex_width = texture->impl._texture.texWidth;
	texture->tex_height = texture->impl._texture.texHeight;
}

void kinc_g4_texture_init(kinc_g4_texture_t *texture, int width, int height, kinc_image_format_t format) {
	texture->impl._uploaded = false;
	kinc_g5_texture_init(&texture->impl._texture, width, height, format);
	texture->tex_width = texture->impl._texture.texWidth;
	texture->tex_height = texture->impl._texture.texHeight;
}

void kinc_g4_texture_init3d(kinc_g4_texture_t *texture, int width, int height, int depth, kinc_image_format_t format) {}

void kinc_g4_texture_init_from_bytes(kinc_g4_texture_t *texture, void *data, int size, const char *format) {
	
}

void kinc_g4_texture_init_from_bytes3d(kinc_g4_texture_t *texture, void *data, int width, int height, int depth, int format, bool readable) {}

void kinc_g4_texture_destroy(kinc_g4_texture_t *texture) {
	//kinc_g4_internal_texture_unset(texture);
	kinc_g5_texture_destroy(&texture->impl._texture);
}

void kinc_g4_internal_texture_unset(kinc_g4_texture_t *texture) {
	// TODO
}

void kinc_g4_internal_texture_unmipmap(kinc_g4_texture_t *texture) {
	// TODO
}

uint8_t* kinc_g4_texture_lock(kinc_g4_texture_t *texture) {
	return kinc_g5_texture_lock(&texture->impl._texture);
}

void kinc_g4_texture_unlock(kinc_g4_texture_t *texture) {
	kinc_g5_texture_unlock(&texture->impl._texture);
}

void kinc_g4_texture_clear(kinc_g4_texture_t *texture, int x, int y, int z, int width, int height, int depth, unsigned color) {
	kinc_g5_texture_clear(&texture->impl._texture, x, y, z, width, height, depth, color);
}

int kinc_g4_texture_stride(kinc_g4_texture_t *texture) {
	return kinc_g5_texture_stride(&texture->impl._texture);
}

void kinc_g4_texture_generate_mipmaps(kinc_g4_texture_t *texture, int levels) {
	kinc_g5_texture_generate_mipmaps(&texture->impl._texture, levels);
}

void kinc_g4_texture_set_mipmap(kinc_g4_texture_t *texture, kinc_image_t *mipmap, int level) {
	//kinc_g5_texture_set_mipmap(&texture->impl._texture, &mipmap->impl._texture, level);
}
