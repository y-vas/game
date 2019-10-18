#include "pch.h"

#include <kinc/threads/mutex.h>

#include <Windows.h>

#include <assert.h>

void kinc_mutex_init(kinc_mutex_t *mutex) {
	assert(sizeof(RTL_CRITICAL_SECTION) == sizeof(kinc_microsoft_critical_section_t));
	InitializeCriticalSection((LPCRITICAL_SECTION)&mutex->impl.criticalSection);
}

void kinc_mutex_destroy(kinc_mutex_t *mutex) {
	DeleteCriticalSection((LPCRITICAL_SECTION)&mutex->impl.criticalSection);
}

void kinc_mutex_lock(kinc_mutex_t *mutex) {
	EnterCriticalSection((LPCRITICAL_SECTION)&mutex->impl.criticalSection);
}

bool kinc_mutex_try_to_lock(kinc_mutex_t *mutex) {
	return TryEnterCriticalSection((LPCRITICAL_SECTION)&mutex->impl.criticalSection);
}

void kinc_mutex_unlock(kinc_mutex_t *mutex) {
	LeaveCriticalSection((LPCRITICAL_SECTION)&mutex->impl.criticalSection);
}

bool kinc_uber_mutex_init(kinc_uber_mutex_t *mutex, const char *name) {
#if defined(KORE_WINDOWS) || defined(KORE_WINDOWSAPP)
	mutex->impl.id = (void*)CreateMutexA(NULL, FALSE, name);
	HRESULT res = GetLastError();
	if (res && res != ERROR_ALREADY_EXISTS) {
		mutex->impl.id = NULL;
		assert(false);
		return false;
	}
	return true;
#else
	return false;
#endif
}

void kinc_uber_mutex_destroy(kinc_uber_mutex_t *mutex) {
#if defined(KORE_WINDOWS) || defined(KORE_WINDOWSAPP)
	if (mutex->impl.id) {
		CloseHandle((HANDLE)mutex->impl.id);
		mutex->impl.id = NULL;
	}
#endif
}

void kinc_uber_mutex_lock(kinc_uber_mutex_t *mutex) {
#if defined(KORE_WINDOWS) || defined(KORE_WINDOWSAPP)
	bool succ = WaitForSingleObject((HANDLE)mutex->impl.id, INFINITE) == WAIT_FAILED ? false : true;
	assert(succ);
#endif
}

void kinc_uber_mutex_unlock(kinc_uber_mutex_t *mutex) {
#if defined(KORE_WINDOWS) || defined(KORE_WINDOWSAPP)
	bool succ = ReleaseMutex((HANDLE)mutex->impl.id) == FALSE ? false : true;
	assert(succ);
#endif
}
