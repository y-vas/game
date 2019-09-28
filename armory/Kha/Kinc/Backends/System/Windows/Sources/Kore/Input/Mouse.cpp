#include "../pch.h"

#include <Kore/System.h>
#include <Kore/Window.h>
#include <Kore/Windows.h>

#include <kinc/input/mouse.h>

#include <Windows.h>

using namespace Kore;

void kinc_internal_mouse_lock(int window) {
	kinc_mouse_hide();
	HWND handle = kinc_windows_window_handle(window);
	SetCapture(handle);
	RECT rect;
	GetWindowRect(handle, &rect);
	ClipCursor(&rect);
}

void kinc_internal_mouse_unlock(int window) {
	kinc_mouse_show();
	ReleaseCapture();
	ClipCursor(nullptr);
}

bool kinc_mouse_can_lock(int window) {
	return true;
}

void kinc_mouse_show() {
	// Work around the internal counter of ShowCursor
	while (ShowCursor(true) < 0) {}
}

void kinc_mouse_hide() {
	// Work around the internal counter of ShowCursor
	while (ShowCursor(false) >= 0) {}
}

void kinc_mouse_set_position(int window, int x, int y) {
	POINT point;
	point.x = x;
	point.y = y;
	ClientToScreen(kinc_windows_window_handle(window), &point);
	SetCursorPos(point.x, point.y);
}

void kinc_mouse_get_position(int window, int *x, int *y) {
	POINT point;
	GetCursorPos(&point);
	ScreenToClient(kinc_windows_window_handle(window), &point);
	*x = point.x;
	*y = point.y;
}
