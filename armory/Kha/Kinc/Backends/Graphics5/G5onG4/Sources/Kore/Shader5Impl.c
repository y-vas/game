#include "pch.h"

#include <kinc/graphics4/shader.h>
#include <kinc/graphics5/shader.h>

void kinc_g5_shader_init(kinc_g5_shader_t *shader, void *source, size_t length, kinc_g5_shader_type_t type) {
	kinc_g4_shader_init(&shader->impl.shader, source, length, (kinc_g4_shader_type_t)type);
}
