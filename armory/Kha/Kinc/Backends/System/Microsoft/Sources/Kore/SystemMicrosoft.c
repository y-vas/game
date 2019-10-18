#include "pch.h"

#include "SystemMicrosoft.h"

#include <kinc/error.h>

#include <Windows.h>

#include <intrin.h>

#include <stdio.h>

#define S_OK ((HRESULT)0L)

static void winerror(HRESULT result) {
	LPVOID buffer = NULL;
	DWORD dw = GetLastError();

	__debugbreak();

#if defined(KORE_WINDOWS) || defined(KORE_WINDOWSAPP)
	if (dw != 0) {
		FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, NULL, dw,
		               MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPSTR)&buffer, 0, NULL);

		kinc_error_message("Error: %s", buffer);
	}
	else {
#endif
		kinc_error_message("Unknown Windows error, return value was 0x%x.", result);
#if defined(KORE_WINDOWS) || defined(KORE_WINDOWSAPP)
	}
#endif
}

void kinc_microsoft_affirm(HRESULT result) {
	if (result != S_OK) {
		winerror(result);
	}
}

void kinc_microsoft_affirm_message(HRESULT result, const char *format, ...) {
	va_list args;
	va_start(args, format);
	kinc_affirm_args(result == S_OK, format, args);
	va_end(args);
}

void kinc_microsoft_format(const char *format, va_list args, wchar_t *buffer) {
	wchar_t formatw[4096];
	MultiByteToWideChar(CP_UTF8, 0, format, -1, formatw, 4096);

	size_t bufferIndex = 0;
	buffer[bufferIndex] = 0;
	printf("");
	for (int i = 0; formatw[i] != 0; ++i) {
		if (formatw[i] == L'%') {
			++i;
			switch (formatw[i]) {
			case L's':
			case L'S': {
				char* arg = va_arg(args, char*);
				wchar_t argw[1024];
				MultiByteToWideChar(CP_UTF8, 0, arg, -1, argw, 1024);
				wcscat(buffer, argw);
				bufferIndex += wcslen(argw);
				break;
			}
			case L'd':
			case L'i':
			case L'u':
			case L'o':
			case L'x': {
				int arg = va_arg(args, int);
				wchar_t argformat[3];
				argformat[0] = L'%';
				argformat[1] = formatw[i];
				argformat[2] = 0;
				bufferIndex += swprintf(&buffer[bufferIndex], 4096 - bufferIndex - 1, argformat, arg);
				break;
			}
			case 'f':
			case 'e':
			case 'g':
			case 'a': {
				double arg = va_arg(args, double);
				wchar_t argformat[3];
				argformat[0] = L'%';
				argformat[1] = formatw[i];
				argformat[2] = 0;
				bufferIndex += swprintf(&buffer[bufferIndex], 4096 - bufferIndex - 1, argformat, arg);
				break;
			}
			case 'c': {
				char arg = va_arg(args, char);
				wchar_t argformat[3];
				argformat[0] = L'%';
				argformat[1] = formatw[i];
				argformat[2] = 0;
				bufferIndex += swprintf(&buffer[bufferIndex], 4096 - bufferIndex - 1, argformat, arg);
				break;
			}
			case 'p':
			case 'n': {
				void* arg = va_arg(args, void*);
				wchar_t argformat[3];
				argformat[0] = L'%';
				argformat[1] = formatw[i];
				argformat[2] = 0;
				bufferIndex += swprintf(&buffer[bufferIndex], 4096 - bufferIndex - 1, argformat, arg);
				break;
			}
			case '%': {
				bufferIndex += swprintf(&buffer[bufferIndex], 4096 - bufferIndex - 1, L"%%");
				break;
			}
			}
		}
		else {
			buffer[bufferIndex++] = formatw[i];
			buffer[bufferIndex] = 0;
		}
	}
}
