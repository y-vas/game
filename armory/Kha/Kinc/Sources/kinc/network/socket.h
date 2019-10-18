#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#ifdef KORE_WINDOWS
#if defined(_WIN64)
typedef unsigned __int64 UINT_PTR, *PUINT_PTR;
#else
#if !defined _W64
#define _W64
#endif
typedef _W64 unsigned int UINT_PTR, *PUINT_PTR;
#endif
typedef UINT_PTR SOCKET;
#endif

typedef struct {
#ifdef KORE_WINDOWS
	SOCKET handle;
#else
	int handle;
#endif
} kinc_socket_t;

void kinc_socket_init(kinc_socket_t *socket);
void kinc_socket_destroy(kinc_socket_t *socket);
void kinc_socket_open(kinc_socket_t *socket, int port);
void kinc_socket_set_broadcast_enabled(kinc_socket_t *socket, bool enabled);
void kinc_socket_send(kinc_socket_t *socket, unsigned address, int port, const unsigned char *data, int size);
void kinc_socket_send_url(kinc_socket_t *socket, const char *url, int port, const unsigned char *data, int size);
int kinc_socket_receive(kinc_socket_t *socket, unsigned char *data, int maxSize, unsigned *fromAddress, unsigned *fromPort);
unsigned kinc_url_to_int(const char *url, int port);

#ifdef __cplusplus
}
#endif
