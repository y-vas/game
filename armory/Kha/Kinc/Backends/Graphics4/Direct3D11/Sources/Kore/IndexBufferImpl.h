#pragma once

struct ID3D11Buffer;

typedef struct {
	struct ID3D11Buffer *ib;
	int *indices;
	int count;
} kinc_g4_index_buffer_impl_t;

//**static Graphics4::IndexBuffer* _current;
