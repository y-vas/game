#pragma once

#include <Kore/ThreadLocalImpl.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
	kinc_thread_local_impl_t impl;
} kinc_thread_local_t;

void kinc_thread_local_init(kinc_thread_local_t *local);
void kinc_thread_local_destroy(kinc_thread_local_t *local);
void *kinc_thread_local_get(kinc_thread_local_t *local);
void kinc_thread_local_set(kinc_thread_local_t *local, void *data);

#ifdef __cplusplus
}
#endif
