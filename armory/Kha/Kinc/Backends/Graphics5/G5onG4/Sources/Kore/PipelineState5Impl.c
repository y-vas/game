#include "pch.h"

#include <kinc/graphics5/pipeline.h>
#include <kinc/graphics5/constantlocation.h>

void kinc_g5_pipeline_init(kinc_g5_pipeline_t *pipe) {
	kinc_g4_pipeline_init(&pipe->impl.pipe);
}

kinc_g5_constant_location_t kinc_g5_pipeline_get_constant_location(kinc_g5_pipeline_t *pipe, const char* name) {
	kinc_g5_constant_location_t location;
	location.impl.location = kinc_g4_pipeline_get_constant_location(&pipe->impl.pipe, name);
	return location;
}

kinc_g5_texture_unit_t kinc_g5_pipeline_get_texture_unit(kinc_g5_pipeline_t *pipe, const char *name) {
	kinc_g5_texture_unit_t unit;
	unit.impl.unit = kinc_g4_pipeline_get_texture_unit(&pipe->impl.pipe, name);
	return unit;
}

void kinc_g5_pipeline_compile(kinc_g5_pipeline_t *pipe) {
	pipe->impl.pipe.input_layout[0] = pipe->inputLayout[0];
	pipe->impl.pipe.vertex_shader = &pipe->vertexShader->impl.shader;
	pipe->impl.pipe.fragment_shader = &pipe->fragmentShader->impl.shader;
	kinc_g4_pipeline_compile(&pipe->impl.pipe);
}
