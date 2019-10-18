#pragma once

#ifdef KORE_WINDOWS
#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <Windows.h>
#endif

#ifdef __cplusplus
extern "C" {
#endif

struct kinc_g4_render_target;

typedef struct {
#ifdef KORE_WINDOWS
	HDC deviceContext;
	HGLRC glContext;
#endif
	int framebuffer;
	unsigned vertexArray;
	struct kinc_g4_render_target *renderTarget;
} Kinc_Internal_OpenGLWindow;

extern Kinc_Internal_OpenGLWindow Kinc_Internal_windows[10];

void Kinc_Internal_initWindowsGLContext(int window, int depthBufferBits, int stencilBufferBits);
void Kinc_Internal_blitWindowContent(int window);
void Kinc_Internal_setWindowRenderTarget(int window);

#ifdef __cplusplus
}
#endif
