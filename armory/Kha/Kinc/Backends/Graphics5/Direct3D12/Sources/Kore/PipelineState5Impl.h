#pragma once

#ifdef __cplusplus
extern "C" {
#endif

struct kinc_g5_shader;

struct ID3D12PipelineState;
struct ID3D12GraphicsCommandList;

typedef struct {
	struct ID3D12PipelineState *pso;
	// ID3D11InputLayout* inputLayout;
	// ID3D11Buffer* fragmentConstantBuffer;
	// ID3D11Buffer* vertexConstantBuffer;
	// ID3D11Buffer* geometryConstantBuffer;
	// ID3D11Buffer* tessEvalConstantBuffer;
	// ID3D11Buffer* tessControlConstantBuffer;

	//static void setConstants(ID3D12GraphicsCommandList *commandList, Graphics5::PipelineState *pipeline);
} PipelineState5Impl;

typedef struct {
	int vertexOffset;
	uint32_t vertexSize;
	int fragmentOffset;
	uint32_t fragmentSize;
	int geometryOffset;
	uint32_t geometrySize;
	int tessEvalOffset;
	uint32_t tessEvalSize;
	int tessControlOffset;
	uint32_t tessControlSize;
} ConstantLocation5Impl;

typedef struct {
	int nothing;
} AttributeLocation5Impl;

struct kinc_g5_pipeline;

void kinc_g5_internal_setConstants(struct ID3D12GraphicsCommandList *commandList, struct kinc_g5_pipeline *pipeline);

#ifdef __cplusplus
}
#endif
