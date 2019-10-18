#include "pch.h"

#include "Direct3D12.h"
#include "VertexBuffer5Impl.h"

#include <Kinc/Graphics5/VertexBuffer.h>

#include <Kinc/Graphics4/Graphics.h>
#include <Kore/SystemMicrosoft.h>

kinc_g5_vertex_buffer_t *_current_vertex_buffer = nullptr;

void kinc_g5_vertex_buffer_init(kinc_g5_vertex_buffer_t *buffer, int count, kinc_g5_vertex_structure_t *structure, bool gpuMemory, int instanceDataStepRate) {
	buffer->impl.myCount = count;
	buffer->impl.lastStart = -1;
	buffer->impl.lastCount = -1;

	static_assert(sizeof(D3D12VertexBufferView) == sizeof(D3D12_VERTEX_BUFFER_VIEW), "Something is wrong with D3D12IVertexBufferView");

	buffer->impl.myStride = 0;
	for (int i = 0; i < structure->size; ++i) {
		switch (structure->elements[i].data) {
		case KINC_G4_VERTEX_DATA_FLOAT1:
			buffer->impl.myStride += 1 * 4;
			break;
		case KINC_G4_VERTEX_DATA_FLOAT2:
			buffer->impl.myStride += 2 * 4;
			break;
		case KINC_G4_VERTEX_DATA_FLOAT3:
			buffer->impl.myStride += 3 * 4;
			break;
		case KINC_G4_VERTEX_DATA_FLOAT4:
			buffer->impl.myStride += 4 * 4;
			break;
		case KINC_G4_VERTEX_DATA_COLOR:
			buffer->impl.myStride += 1 * 4;
			break;
		case KINC_G4_VERTEX_DATA_SHORT2_NORM:
			buffer->impl.myStride += 2 * 2;
			break;
		case KINC_G4_VERTEX_DATA_SHORT4_NORM:
			buffer->impl.myStride += 4 * 2;
			break;
		}
	}

	int uploadBufferSize = buffer->impl.myStride * buffer->impl.myCount;

	device->CreateCommittedResource(&CD3DX12_HEAP_PROPERTIES(D3D12_HEAP_TYPE_UPLOAD), D3D12_HEAP_FLAG_NONE, &CD3DX12_RESOURCE_DESC::Buffer(uploadBufferSize),
	                                D3D12_RESOURCE_STATE_GENERIC_READ, nullptr, IID_GRAPHICS_PPV_ARGS(&buffer->impl.uploadBuffer));

	// device_->CreateCommittedResource(&CD3DX12_HEAP_PROPERTIES (D3D12_HEAP_TYPE_DEFAULT), D3D12_HEAP_FLAG_NONE,
	// &CD3DX12_RESOURCE_DESC::Buffer(uploadBufferSize),
	//	D3D12_RESOURCE_STATE_COPY_DEST, nullptr, IID_PPV_ARGS(&vertexBuffer));

	buffer->impl.view.BufferLocation = buffer->impl.uploadBuffer->GetGPUVirtualAddress();
	buffer->impl.view.SizeInBytes = uploadBufferSize;
	buffer->impl.view.StrideInBytes = buffer->impl.myStride;
}

void kinc_g5_vertex_buffer_destroy(kinc_g5_vertex_buffer_t *buffer) {
	// vb->Release();
	// delete[] vertices;
}

float *kinc_g5_vertex_buffer_lock_all(kinc_g5_vertex_buffer_t *buffer) {
	return kinc_g5_vertex_buffer_lock(buffer, 0, kinc_g5_vertex_buffer_count(buffer));
}

float *kinc_g5_vertex_buffer_lock(kinc_g5_vertex_buffer_t *buffer, int start, int count) {
	buffer->impl.lastStart = start;
	buffer->impl.lastCount = count;
	void* p;
	D3D12_RANGE range;
	range.Begin = start * buffer->impl.myStride;
	range.End = range.Begin + count * buffer->impl.myStride;
	buffer->impl.uploadBuffer->Map(0, &range, &p);
	byte* bytes = (byte*)p;
	bytes += start * buffer->impl.myStride;
	return (float*)bytes;
}

void kinc_g5_vertex_buffer_unlock_all(kinc_g5_vertex_buffer_t *buffer) {
	D3D12_RANGE range;
	range.Begin = buffer->impl.lastStart * buffer->impl.myStride;
	range.End = range.Begin + buffer->impl.lastCount * buffer->impl.myStride;
	buffer->impl.uploadBuffer->Unmap(0, &range);

	// view.BufferLocation = uploadBuffer->GetGPUVirtualAddress() + myStart * myStride;

	// commandList->CopyBufferRegion(vertexBuffer, 0, uploadBuffer, 0, count() * stride());
	// CD3DX12_RESOURCE_BARRIER barriers[1] = { CD3DX12_RESOURCE_BARRIER::Transition(vertexBuffer, D3D12_RESOURCE_STATE_COPY_DEST,
	// D3D12_RESOURCE_STATE_VERTEX_AND_CONSTANT_BUFFER) };
	// commandList->ResourceBarrier(1, barriers);
}

void kinc_g5_vertex_buffer_unlock(kinc_g5_vertex_buffer_t *buffer, int count) {
	D3D12_RANGE range;
	range.Begin = buffer->impl.lastStart * buffer->impl.myStride;
	range.End = range.Begin + count * buffer->impl.myStride;
	buffer->impl.uploadBuffer->Unmap(0, &range);

	// view.BufferLocation = uploadBuffer->GetGPUVirtualAddress() + myStart * myStride;

	// commandList->CopyBufferRegion(vertexBuffer, 0, uploadBuffer, 0, count() * stride());
	// CD3DX12_RESOURCE_BARRIER barriers[1] = { CD3DX12_RESOURCE_BARRIER::Transition(vertexBuffer, D3D12_RESOURCE_STATE_COPY_DEST,
	// D3D12_RESOURCE_STATE_VERTEX_AND_CONSTANT_BUFFER) };
	// commandList->ResourceBarrier(1, barriers);
}

int kinc_g5_internal_vertex_buffer_set(kinc_g5_vertex_buffer_t *buffer, int offset) {
	// UINT stride = myStride;
	// UINT offset = 0;
	// context->IASetVertexBuffers(0, 1, &vb, &stride, &offset);
	_current_vertex_buffer = buffer;
	return 0;
}

int kinc_g5_vertex_buffer_count(kinc_g5_vertex_buffer_t *buffer) {
	return buffer->impl.myCount;
}

int kinc_g5_vertex_buffer_stride(kinc_g5_vertex_buffer_t *buffer) {
	return buffer->impl.myStride;
}
