#pragma once

#include <Kore/MutexImpl.h>

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
	kinc_mutex_impl_t impl;
} kinc_mutex_t;

void kinc_mutex_init(kinc_mutex_t *mutex);
void kinc_mutex_destroy(kinc_mutex_t *mutex);
void kinc_mutex_lock(kinc_mutex_t *mutex);
bool kinc_mutex_try_to_lock(kinc_mutex_t *mutex);
void kinc_mutex_unlock(kinc_mutex_t *mutex);

typedef struct {
	kinc_uber_mutex_impl_t impl;
} kinc_uber_mutex_t;

bool kinc_uber_mutex_init(kinc_uber_mutex_t *mutex, const char *name);
void kinc_uber_mutex_destroy(kinc_uber_mutex_t *mutex);
void kinc_uber_mutex_lock(kinc_uber_mutex_t *mutex);
void kinc_uber_mutex_unlock(kinc_uber_mutex_t *mutex);

#ifdef __cplusplus
}
#endif
