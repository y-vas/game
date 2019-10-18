#include "pch.h"

#include <kinc/audio2/audio.h>

#include <Kore/Error.h>
#include <Kore/Log.h>
#include <Kore/SystemMicrosoft.h>
#include <Kore/Threads/Thread.h>

#include <AudioClient.h>
#include <Windows.h>
#include <initguid.h>
#include <mfapi.h>
#include <mmdeviceapi.h>
#include <wrl/implements.h>

using namespace Kore;

#ifndef KORE_WINDOWS
using namespace ::Microsoft::WRL;
using namespace Windows::Media::Devices;
using namespace Windows::Storage::Streams;
#endif

// based on the implementation in soloud and Microsoft sample code
namespace {
	void (*a2_callback)(kinc_a2_buffer_t *buffer, int samples) = nullptr;
	kinc_a2_buffer_t a2_buffer;

	IMMDeviceEnumerator* deviceEnumerator;
	IMMDevice* device;
	IAudioClient* audioClient;
	IAudioRenderClient* renderClient;
	HANDLE bufferEndEvent;
	HANDLE audioProcessingDoneEvent;
	UINT32 bufferFrames;
	WAVEFORMATEX requestedFormat;
	WAVEFORMATEX* closestFormat;
	WAVEFORMATEX* format;

	void copyS16Sample(s16* buffer) {
		float value = *(float*)&a2_buffer.data[a2_buffer.read_location];
		a2_buffer.read_location += 4;
		if (a2_buffer.read_location >= a2_buffer.data_size) a2_buffer.read_location = 0;
		*buffer = (s16)(value * 32767);
	}

	void copyFloatSample(float* buffer) {
		float value = *(float*)&a2_buffer.data[a2_buffer.read_location];
		a2_buffer.read_location += 4;
		if (a2_buffer.read_location >= a2_buffer.data_size) a2_buffer.read_location = 0;
		*buffer = value;
	}

	void submitBuffer(unsigned frames) {
		BYTE* buffer = nullptr;
		if (FAILED(renderClient->GetBuffer(frames, &buffer))) {
			return;
		}

		if (a2_callback != nullptr) {
			a2_callback(&a2_buffer, frames * 2);
			memset(buffer, 0, frames * format->nBlockAlign);
			if (format->wFormatTag == WAVE_FORMAT_PCM) {
				for (UINT32 i = 0; i < frames; ++i) {
					copyS16Sample((s16*)&buffer[i * format->nBlockAlign]);
					copyS16Sample((s16*)&buffer[i * format->nBlockAlign + 2]);
				}
			}
			else {
				for (UINT32 i = 0; i < frames; ++i) {
					copyFloatSample((float*)&buffer[i * format->nBlockAlign]);
					copyFloatSample((float*)&buffer[i * format->nBlockAlign + 4]);
				}
			}
		}
		else {
			memset(buffer, 0, frames * format->nBlockAlign);
		}

		renderClient->ReleaseBuffer(frames, 0);
	}

	void audioThread(LPVOID) {
		submitBuffer(bufferFrames);
		audioClient->Start();
		while (WAIT_OBJECT_0 != WaitForSingleObject(audioProcessingDoneEvent, 0)) {
			WaitForSingleObject(bufferEndEvent, INFINITE);
			UINT32 padding = 0;
			if (FAILED(audioClient->GetCurrentPadding(&padding))) {
				continue;
			}
			UINT32 frames = bufferFrames - padding;
			submitBuffer(frames);
		}
	}

	void initAudio() {
		const int sampleRate = 48000;

		bufferEndEvent = CreateEvent(0, FALSE, FALSE, 0);
		affirm(bufferEndEvent != 0);

		audioProcessingDoneEvent = CreateEvent(0, FALSE, FALSE, 0);
		affirm(audioProcessingDoneEvent != 0);

		format = &requestedFormat;
		ZeroMemory(&requestedFormat, sizeof(WAVEFORMATEX));
		requestedFormat.nChannels = 2;
		requestedFormat.nSamplesPerSec = sampleRate;
		requestedFormat.wFormatTag = WAVE_FORMAT_PCM;
		requestedFormat.wBitsPerSample = sizeof(short) * 8;
		requestedFormat.nBlockAlign = (requestedFormat.nChannels * requestedFormat.wBitsPerSample) / 8;
		requestedFormat.nAvgBytesPerSec = requestedFormat.nSamplesPerSec * requestedFormat.nBlockAlign;
		requestedFormat.cbSize = 0;

		HRESULT supported = audioClient->IsFormatSupported(AUDCLNT_SHAREMODE_SHARED, format, &closestFormat);
		if (supported == S_FALSE) {
			log(Warning, "Falling back to the system's preferred WASAPI mix format.", supported);
			if (closestFormat != nullptr) {
				format = closestFormat;
			}
			else {
				audioClient->GetMixFormat(&format);
			}
		}
		HRESULT result = audioClient->Initialize(AUDCLNT_SHAREMODE_SHARED, AUDCLNT_STREAMFLAGS_EVENTCALLBACK, 40 * 1000 * 10, 0, format, 0);
		if (result != S_OK) {
			log(Warning, "Could not initialize WASAPI audio, going silent (error code 0x%x).", result);
			return;
		}

		kinc_a2_samples_per_second = format->nSamplesPerSec;

		bufferFrames = 0;
		kinc_microsoft_affirm(audioClient->GetBufferSize(&bufferFrames));
		kinc_microsoft_affirm(audioClient->GetService(__uuidof(IAudioRenderClient), reinterpret_cast<void **>(&renderClient)));
		kinc_microsoft_affirm(audioClient->SetEventHandle(bufferEndEvent));

#ifdef KORE_WINDOWS
		createAndRunThread(audioThread, nullptr);
#else
		audioThread(nullptr);
#endif
	}

#ifndef KORE_WINDOWS
	class AudioRenderer : public RuntimeClass<RuntimeClassFlags<ClassicCom>, FtmBase, IActivateAudioInterfaceCompletionHandler> {
	public:
		STDMETHOD(ActivateCompleted)(IActivateAudioInterfaceAsyncOperation* operation) {
			IUnknown* audioInterface = nullptr;
			HRESULT hrActivateResult = S_OK;
			HRESULT hr = operation->GetActivateResult(&hrActivateResult, &audioInterface);
			if (SUCCEEDED(hr) && SUCCEEDED(hrActivateResult)) {
				audioInterface->QueryInterface(IID_PPV_ARGS(&audioClient));
				initAudio();
			}
			return S_OK;
		}
	};

	ComPtr<AudioRenderer> renderer;
#endif
} // namespace

template <class T> void SafeRelease(__deref_inout_opt T** ppT) {
	T* pTTemp = *ppT;
	*ppT = nullptr;
	if (pTTemp) {
		pTTemp->Release();
	}
}

#define SAFE_RELEASE(punk)                                                                                                                                     \
	if ((punk) != NULL) {                                                                                                                                      \
		(punk)->Release();                                                                                                                                     \
		(punk) = NULL;                                                                                                                                         \
	}

void kinc_a2_init() {
	a2_buffer.read_location = 0;
	a2_buffer.write_location = 0;
	a2_buffer.data_size = 128 * 1024;
	a2_buffer.data = new u8[a2_buffer.data_size];

#ifdef KORE_WINDOWS
	kinc_microsoft_affirm(CoInitializeEx(0, COINIT_MULTITHREADED));
	kinc_microsoft_affirm(
	    CoCreateInstance(__uuidof(MMDeviceEnumerator), 0, CLSCTX_ALL, __uuidof(IMMDeviceEnumerator), reinterpret_cast<void**>(&deviceEnumerator)));
	kinc_microsoft_affirm(deviceEnumerator->GetDefaultAudioEndpoint(eRender, eConsole, &device));
	kinc_microsoft_affirm(device->Activate(__uuidof(IAudioClient), CLSCTX_ALL, 0, reinterpret_cast<void **>(&audioClient)));
	initAudio();
#else
	renderer = Make<AudioRenderer>();

	IActivateAudioInterfaceAsyncOperation* asyncOp;
	Platform::String ^ deviceId = MediaDevice::GetDefaultAudioRenderId(Windows::Media::Devices::AudioDeviceRole::Default);
	kinc_microsoft_affirm(ActivateAudioInterfaceAsync(deviceId->Data(), __uuidof(IAudioClient2), nullptr, renderer.Get(), &asyncOp));
	SafeRelease(&asyncOp);
#endif
}

void kinc_a2_set_callback(void(*kinc_a2_audio_callback)(kinc_a2_buffer_t *buffer, int samples)) {
	a2_callback = kinc_a2_audio_callback;
}

void kinc_a2_update() {}

void kinc_a2_shutdown() {
	// Wait for last data in buffer to play before stopping.
	// Sleep((DWORD)(hnsActualDuration/REFTIMES_PER_MILLISEC/2));

	//	affirm(pAudioClient->Stop());  // Stop playing.

	//	CoTaskMemFree(pwfx);
	//	SAFE_RELEASE(pEnumerator)
	//	SAFE_RELEASE(pDevice)
	//	SAFE_RELEASE(pAudioClient)
	//	SAFE_RELEASE(pRenderClient)
}
