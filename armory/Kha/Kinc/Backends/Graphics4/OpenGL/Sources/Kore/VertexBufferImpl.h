#pragma once

#include <kinc/graphics4/vertexstructure.h>

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
	float *data;
	int myCount;
	int myStride;
	unsigned bufferId;
	unsigned usage;
	int sectionStart;
	int sectionSize;
	//#if defined KORE_ANDROID || defined KORE_HTML5 || defined KORE_TIZEN
	kinc_g4_vertex_structure_t structure;
	//#endif
	int instanceDataStepRate;
#ifndef NDEBUG
	bool initialized;
#endif
} kinc_g4_vertex_buffer_impl_t;

#ifdef __cplusplus
}
#endif
