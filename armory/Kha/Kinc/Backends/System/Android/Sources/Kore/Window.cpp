#include "pch.h"

#include <kinc/display.h>
#include <kinc/graphics4/graphics.h>
#include <kinc/window.h>
#include <kinc/bridge.h>

/*namespace {
	Window window;
}

Window* Window::get(int window) {
	if (window > 0) {
		return nullptr;
	}
	return &::window;
}*/

int kinc_count_windows(void) {
	return 1;
}

int kinc_window_x(int window_index) {
	return 0;
}

int kinc_window_y(int window_index) {
	return 0;
}

int glWidth();

int kinc_window_width(int window_index) {
	return glWidth();
}

int glHeight();

int kinc_window_height(int window_index) {
	return glHeight();
}

void kinc_window_resize(int window_index, int width, int height) {
	
}

void kinc_window_move(int window_index, int x, int y) {
	
}

void kinc_window_change_framebuffer(int window_index, kinc_framebuffer_options_t *frame) {
	kinc_bridge_g4_internal_change_framebuffer(0, frame);
}

void kinc_window_change_features(int window_index, int features) {
	
}

void kinc_window_change_mode(int window_index, kinc_window_mode_t mode) {
	
}

void kinc_window_destroy(int window_index) {
	
}

void kinc_window_show(int window_index) {
	
}

void kinc_window_hide(int window_index) {
	
}

void kinc_window_set_title(int window_index, const char *title) {
	
}

int kinc_window_create(kinc_window_options_t *win, kinc_framebuffer_options_t *frame) {
	return 0;
}

void kinc_window_set_resize_callback(int window_index, void (*callback)(int x, int y, void *data), void *data) {

}

void kinc_window_set_ppi_changed_callback(int window_index, void (*callback)(int ppi, void *data), void *data) {

}

kinc_window_mode_t kinc_window_get_mode(int window_index) {
	return KINC_WINDOW_MODE_FULLSCREEN;
}

int kinc_window_display(int window) {
	return 0;
}
