#include "pch.h"

#include "Direct3D11.h"

#include <kinc/graphics4/texture.h>
#include <kinc/graphics4/textureunit.h>

#include <Kore/Math/Random.h>
#include <Kore/SystemMicrosoft.h>

#include <assert.h>

using namespace Kore;

static kinc_g4_texture_t *setTextures[16] = {nullptr, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr,
	                                    nullptr, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr};

static DXGI_FORMAT convertFormat(kinc_image_format_t format) {
	switch (format) {
	case KINC_IMAGE_FORMAT_RGBA128:
		return DXGI_FORMAT_R32G32B32A32_FLOAT;
	case KINC_IMAGE_FORMAT_RGBA64:
		return DXGI_FORMAT_R16G16B16A16_FLOAT;
	case KINC_IMAGE_FORMAT_RGB24:
		return DXGI_FORMAT_R8G8B8A8_UNORM;
	case KINC_IMAGE_FORMAT_A32:
		return DXGI_FORMAT_R32_FLOAT;
	case KINC_IMAGE_FORMAT_A16:
		return DXGI_FORMAT_R16_FLOAT;
	case KINC_IMAGE_FORMAT_GREY8:
		return DXGI_FORMAT_R8_UNORM;
	case KINC_IMAGE_FORMAT_BGRA32:
		return DXGI_FORMAT_B8G8R8A8_UNORM;
	case KINC_IMAGE_FORMAT_RGBA32:
		return DXGI_FORMAT_R8G8B8A8_UNORM;
	default:
		assert(false);
		return DXGI_FORMAT_R8G8B8A8_UNORM;
	}
}

static int formatByteSize(kinc_image_format_t format) {
	switch (format) {
	case KINC_IMAGE_FORMAT_RGBA128:
		return 16;
	case KINC_IMAGE_FORMAT_RGBA64:
		return 8;
	case KINC_IMAGE_FORMAT_RGB24:
		return 4;
	case KINC_IMAGE_FORMAT_A32:
		return 4;
	case KINC_IMAGE_FORMAT_A16:
		return 2;
	case KINC_IMAGE_FORMAT_GREY8:
		return 1;
	case KINC_IMAGE_FORMAT_BGRA32:
	case KINC_IMAGE_FORMAT_RGBA32:
		return 4;
	default:
		assert(false);
		return 4;
	}
}

static bool isHdr(kinc_image_format_t format) {
	return format == KINC_IMAGE_FORMAT_RGBA128 || format == KINC_IMAGE_FORMAT_RGBA64 || format == KINC_IMAGE_FORMAT_A32 || format == KINC_IMAGE_FORMAT_A16;
}

void kinc_g4_texture_init_from_image(kinc_g4_texture_t *texture, kinc_image_t *image) {
	memset(&texture->impl, 0, sizeof(texture->impl));
	texture->impl.stage = 0;
	texture->tex_width = image->width;
	texture->tex_height = image->height;
	texture->format = image->format;
	texture->impl.rowPitch = 0;

	D3D11_TEXTURE2D_DESC desc;
	desc.Width = image->width;
	desc.Height = image->height;
	desc.MipLevels = desc.ArraySize = 1;
	desc.Format = convertFormat(image->format);
	desc.SampleDesc.Count = 1;
	desc.SampleDesc.Quality = 0;
	desc.Usage = D3D11_USAGE_DEFAULT;
	desc.BindFlags = D3D11_BIND_SHADER_RESOURCE;
	desc.CPUAccessFlags = 0; // D3D11_CPU_ACCESS_WRITE;
	desc.MiscFlags = 0;

	D3D11_SUBRESOURCE_DATA data;
	data.pSysMem = image->data;
	data.SysMemPitch = image->width * formatByteSize(image->format);
	data.SysMemSlicePitch = 0;

	kinc_microsoft_affirm(device->CreateTexture2D(&desc, &data, &texture->impl.texture));
	kinc_microsoft_affirm(device->CreateShaderResourceView(texture->impl.texture, nullptr, &texture->impl.view));
}

void kinc_g4_texture_init_from_image3d(kinc_g4_texture_t *texture, kinc_image_t *image) {
	memset(&texture->impl, 0, sizeof(texture->impl));
	texture->impl.stage = 0;
	texture->tex_width = image->width;
	texture->tex_height = image->height;
	texture->tex_depth = image->depth;
	texture->format = image->format;
	texture->impl.rowPitch = 0;

	D3D11_TEXTURE3D_DESC desc;
	desc.Width = image->width;
	desc.Height = image->height;
	desc.Depth = image->depth;
	desc.MipLevels = 1;
	desc.Usage = D3D11_USAGE_DEFAULT;
	desc.MiscFlags = 0;
	desc.Format = convertFormat(image->format);
	desc.BindFlags = D3D11_BIND_SHADER_RESOURCE;
	desc.Usage = D3D11_USAGE_DEFAULT;
	desc.CPUAccessFlags = 0;

	D3D11_SUBRESOURCE_DATA data;
	data.pSysMem = image->data;
	data.SysMemPitch = image->width * formatByteSize(image->format);
	data.SysMemSlicePitch = image->width * image->height * formatByteSize(image->format);

	kinc_microsoft_affirm(device->CreateTexture3D(&desc, &data, &texture->impl.texture3D));
	kinc_microsoft_affirm(device->CreateShaderResourceView(texture->impl.texture3D, nullptr, &texture->impl.view));
}

void kinc_g4_texture_init(kinc_g4_texture_t *texture, int width, int height, kinc_image_format_t format) {
	memset(&texture->impl, 0, sizeof(texture->impl));
	texture->impl.stage = 0;
	texture->tex_width = width;
	texture->tex_height = height;
	texture->format = format;

	D3D11_TEXTURE2D_DESC desc;
	desc.Width = width;
	desc.Height = height;
	desc.MipLevels = desc.ArraySize = 1;
	desc.SampleDesc.Count = 1;
	desc.SampleDesc.Quality = 0;
	desc.Usage = D3D11_USAGE_DEFAULT;
	desc.MiscFlags = 0;

	if (format == KINC_IMAGE_FORMAT_RGBA128) { // for compute
		desc.Format = DXGI_FORMAT_R32G32B32A32_FLOAT;
		desc.BindFlags = D3D11_BIND_UNORDERED_ACCESS | D3D11_BIND_SHADER_RESOURCE;
		desc.CPUAccessFlags = 0;
	}
	else {
		desc.Format = format == KINC_IMAGE_FORMAT_RGBA32 ? DXGI_FORMAT_R8G8B8A8_UNORM : DXGI_FORMAT_R8_UNORM;
		desc.BindFlags = D3D11_BIND_SHADER_RESOURCE;
		desc.Usage = D3D11_USAGE_DYNAMIC;
		desc.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;
	}

	kinc_microsoft_affirm(device->CreateTexture2D(&desc, nullptr, &texture->impl.texture));
	kinc_microsoft_affirm(device->CreateShaderResourceView(texture->impl.texture, nullptr, &texture->impl.view));

	if (format == KINC_IMAGE_FORMAT_RGBA128) {
		D3D11_UNORDERED_ACCESS_VIEW_DESC du;
		du.Format = desc.Format;
		du.Texture2D.MipSlice = 0;
		du.ViewDimension = D3D11_UAV_DIMENSION::D3D11_UAV_DIMENSION_TEXTURE2D;
		kinc_microsoft_affirm(device->CreateUnorderedAccessView(texture->impl.texture, &du, &texture->impl.computeView));
	}
}

void kinc_g4_texture_init3d(kinc_g4_texture_t *texture, int width, int height, int depth, kinc_image_format_t format) {
	memset(&texture->impl, 0, sizeof(texture->impl));
	texture->impl.stage = 0;
	texture->tex_width = width;
	texture->tex_height = height;
	texture->tex_depth = depth;
	texture->format = format;
	texture->impl.hasMipmaps = true;

	D3D11_TEXTURE3D_DESC desc;
	desc.Width = width;
	desc.Height = height;
	desc.Depth = depth;
	desc.MipLevels = 0;
	desc.Usage = D3D11_USAGE_DEFAULT;
	desc.MiscFlags = D3D11_RESOURCE_MISC_GENERATE_MIPS;
	desc.Format = format == KINC_IMAGE_FORMAT_RGBA32 ? DXGI_FORMAT_R8G8B8A8_UNORM : DXGI_FORMAT_R8_UNORM;
	desc.BindFlags = D3D11_BIND_SHADER_RESOURCE | D3D11_BIND_RENDER_TARGET | D3D11_BIND_UNORDERED_ACCESS;
	desc.Usage = D3D11_USAGE_DEFAULT;
	desc.CPUAccessFlags = 0;

	kinc_microsoft_affirm(device->CreateTexture3D(&desc, nullptr, &texture->impl.texture3D));
	kinc_microsoft_affirm(device->CreateShaderResourceView(texture->impl.texture3D, nullptr, &texture->impl.view));
}

//TextureImpl::TextureImpl() : hasMipmaps(false), renderView(nullptr), computeView(nullptr) {}

void kinc_internal_texture_unset(kinc_g4_texture_t *texture);

void kinc_g4_texture_destroy(kinc_g4_texture_t *texture) {
	kinc_internal_texture_unset(texture);
	if (texture->impl.view != nullptr) {
		texture->impl.view->Release();
	}
	if (texture->impl.texture != nullptr) {
		texture->impl.texture->Release();
	}
	if (texture->impl.texture3D != NULL) {
		texture->impl.texture3D->Release();
	}
	if (texture->impl.computeView != nullptr) {
		texture->impl.computeView->Release();
	}
}

void kinc_internal_texture_unmipmap(kinc_g4_texture_t *texture) {
	texture->impl.hasMipmaps = false;
}

void kinc_internal_texture_set(kinc_g4_texture_t *texture, kinc_g4_texture_unit_t unit) {
	if (unit.impl.unit < 0) return;
	if (unit.impl.vertex) {
		context->VSSetShaderResources(unit.impl.unit, 1, &texture->impl.view);
	}
	else {
		context->PSSetShaderResources(unit.impl.unit, 1, &texture->impl.view);
	}
	texture->impl.stage = unit.impl.unit;
	setTextures[texture->impl.stage] = texture;
}

void kinc_internal_texture_set_image(kinc_g4_texture_t *texture, kinc_g4_texture_unit_t unit) {
	if (unit.impl.unit < 0) return;
	if (texture->impl.computeView == nullptr) {
		D3D11_UNORDERED_ACCESS_VIEW_DESC du;
		du.Format = texture->format == KINC_IMAGE_FORMAT_RGBA32 ? DXGI_FORMAT_R8G8B8A8_UNORM : DXGI_FORMAT_R8_UNORM;
		du.Texture3D.MipSlice = 0;
		du.Texture3D.FirstWSlice = 0;
		du.Texture3D.WSize = -1;
		du.ViewDimension = D3D11_UAV_DIMENSION::D3D11_UAV_DIMENSION_TEXTURE3D;
		kinc_microsoft_affirm(device->CreateUnorderedAccessView(texture->impl.texture3D, &du, &texture->impl.computeView));
	}
	context->OMSetRenderTargetsAndUnorderedAccessViews(0, nullptr, nullptr, unit.impl.unit, 1, &texture->impl.computeView, nullptr);
}

void kinc_internal_texture_unset(kinc_g4_texture_t *texture) {
	if (setTextures[texture->impl.stage] == texture) {

		setTextures[texture->impl.stage] = NULL;
	}
}

u8 *kinc_g4_texture_lock(kinc_g4_texture_t *texture) {
	D3D11_MAPPED_SUBRESOURCE mappedResource;
	context->Map(texture->impl.texture, 0, D3D11_MAP_WRITE_DISCARD, 0, &mappedResource);
	texture->impl.rowPitch = mappedResource.RowPitch;
	return (u8*)mappedResource.pData;
}

void kinc_g4_texture_unlock(kinc_g4_texture_t *texture) {
	context->Unmap(texture->impl.texture, 0);
}

void kinc_g4_texture_clear(kinc_g4_texture_t *texture, int x, int y, int z, int width, int height, int depth, uint color) {
	if (texture->impl.renderView == nullptr) {
		texture->tex_depth > 1 ? 
			kinc_microsoft_affirm(device->CreateRenderTargetView(texture->impl.texture3D, 0, &texture->impl.renderView))
		                       : kinc_microsoft_affirm(device->CreateRenderTargetView(texture->impl.texture, 0, &texture->impl.renderView));
	}
	static float clearColor[4];
	clearColor[0] = ((color & 0x00ff0000) >> 16) / 255.0f;
	clearColor[1] = ((color & 0x0000ff00) >> 8) / 255.0f;
	clearColor[2] = (color & 0x000000ff) / 255.0f;
	clearColor[3] = ((color & 0xff000000) >> 24) / 255.0f;
	context->ClearRenderTargetView(texture->impl.renderView, clearColor);
}

int kinc_g4_texture_stride(kinc_g4_texture_t *texture) {
	return texture->impl.rowPitch;
}

static void enableMipmaps(kinc_g4_texture_t *texture, int texWidth, int texHeight, int format) {
	D3D11_TEXTURE2D_DESC desc;
	desc.Width = texWidth;
	desc.Height = texHeight;
	desc.MipLevels = 0;
	desc.ArraySize = 1;
	desc.Format = convertFormat((kinc_image_format_t)format);
	desc.SampleDesc.Count = 1;
	desc.SampleDesc.Quality = 0;
	desc.Usage = D3D11_USAGE_DEFAULT;
	desc.BindFlags = D3D11_BIND_SHADER_RESOURCE | D3D11_BIND_RENDER_TARGET;
	desc.CPUAccessFlags = 0;
	desc.MiscFlags = D3D11_RESOURCE_MISC_GENERATE_MIPS;

	ID3D11Texture2D* mipMappedTexture;
	ID3D11ShaderResourceView* mipMappedView;
	kinc_microsoft_affirm(device->CreateTexture2D(&desc, nullptr, &mipMappedTexture));
	kinc_microsoft_affirm(device->CreateShaderResourceView(mipMappedTexture, nullptr, &mipMappedView));

	D3D11_BOX sourceRegion;
	sourceRegion.left = 0;
	sourceRegion.right = texWidth;
	sourceRegion.top = 0;
	sourceRegion.bottom = texHeight;
	sourceRegion.front = 0;
	sourceRegion.back = 1;
	context->CopySubresourceRegion(mipMappedTexture, 0, 0, 0, 0, texture->impl.texture, 0, &sourceRegion);

	if (texture->impl.texture != nullptr) {
		texture->impl.texture->Release();
	}
	texture->impl.texture = mipMappedTexture;

	if (texture->impl.view != nullptr) {
		texture->impl.view->Release();
	}
	texture->impl.view = mipMappedView;

	texture->impl.hasMipmaps = true;
}

void kinc_g4_texture_generate_mipmaps(kinc_g4_texture_t *texture, int levels) {
	if (!texture->impl.hasMipmaps) {
		enableMipmaps(texture, texture->tex_width, texture->tex_height, texture->format);
	}
	context->GenerateMips(texture->impl.view);
}

void kinc_g4_texture_set_mipmap(kinc_g4_texture_t *texture, kinc_image_t *mipmap, int level) {
	if (!texture->impl.hasMipmaps) {
		enableMipmaps(texture, texture->tex_width, texture->tex_height, texture->format);
	}
	D3D11_BOX dstRegion;
	dstRegion.left = 0;
	dstRegion.right = mipmap->width;
	dstRegion.top = 0;
	dstRegion.bottom = mipmap->height;
	dstRegion.front = 0;
	dstRegion.back = 1;
	context->UpdateSubresource(texture->impl.texture, level, &dstRegion, mipmap->data, mipmap->width * formatByteSize(mipmap->format), 0);
}
