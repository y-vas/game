#include "pch.h"

#include <Kinc/Graphics4/IndexBuffer.h>

#include <Kinc/Graphics5/CommandList.h>

extern kinc_g5_command_list_t commandList;

void kinc_g4_index_buffer_init(kinc_g4_index_buffer_t *buffer, int count) {
	kinc_g5_index_buffer_init(&buffer->impl._buffer, count, true);
}

void kinc_g4_index_buffer_destroy(kinc_g4_index_buffer_t *buffer) {}

int *kinc_g4_index_buffer_lock(kinc_g4_index_buffer_t *buffer) {
	return kinc_g5_index_buffer_lock(&buffer->impl._buffer);
}

void kinc_g4_index_buffer_unlock(kinc_g4_index_buffer_t *buffer) {
	kinc_g5_index_buffer_unlock(&buffer->impl._buffer);
	kinc_g5_command_list_upload_index_buffer(&commandList, &buffer->impl._buffer);
}

void kinc_g4_internal_index_buffer_set(kinc_g4_index_buffer_t *buffer) {
	kinc_g5_internal_index_buffer_set(&buffer->impl._buffer);
}

int kinc_g4_index_buffer_count(kinc_g4_index_buffer_t *buffer) {
	return kinc_g5_index_buffer_count(&buffer->impl._buffer);
}
