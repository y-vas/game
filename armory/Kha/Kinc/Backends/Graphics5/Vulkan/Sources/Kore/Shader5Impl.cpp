#include "pch.h"

#include <kinc/graphics5/shader.h>

void kinc_g5_shader_init(kinc_g5_shader_t *shader, void *source, size_t length, kinc_g5_shader_type_t type) {
	shader->impl.length = length;
	shader->impl.id = 0;
	shader->impl.source = new char[length + 1];
	for (int i = 0; i < length; ++i) {
		shader->impl.source[i] = ((char *)source)[i];
	}
	shader->impl.source[length] = 0;
}

void kinc_g5_shader_destroy(kinc_g5_shader_t *shader) {
	delete[] shader->impl.source;
	shader->impl.source = NULL;
}
