#include "pch.h"

#include "soundstream.h"

#define STB_VORBIS_HEADER_ONLY
#include "stb_vorbis.c"

#include <Kore/IO/FileReader.h>

#include <string.h>
#include <stdlib.h>

static kinc_a1_sound_stream_t streams[256];
static int nextStream = 0;
static uint8_t *buffer;
static int bufferIndex;

void initSoundStreams() {
	buffer = (uint8_t*)malloc(1024 * 10);
}

kinc_a1_sound_stream_t *kinc_a1_sound_stream_create(const char *filename, bool looping) {
	kinc_a1_sound_stream_t *stream = &streams[nextStream];
	stream->decoded = false;
	stream->myLooping = looping;
	stream->myVolume = 1;
	stream->rateDecodedHack = false;
	stream->end = false;
	Kore::FileReader file(filename);
	stream->buffer = &buffer[bufferIndex];
	bufferIndex += file.size();
	uint8_t *filecontent = (uint8_t*)file.readAll();
	memcpy(stream->buffer, filecontent, file.size());
	stream->vorbis = stb_vorbis_open_memory(buffer, file.size(), nullptr, nullptr);
	if (stream->vorbis != NULL) {
		stb_vorbis_info info = stb_vorbis_get_info(stream->vorbis);
		stream->chans = info.channels;
		stream->rate = info.sample_rate;
	}
	else {
		stream->chans = 2;
		stream->rate = 22050;
	}
	++nextStream;
	return stream;
}

int kinc_a1_sound_stream_channels(kinc_a1_sound_stream_t *stream) {
	return stream->chans;
}

int kinc_a1_sound_stream_sample_rate(kinc_a1_sound_stream_t *stream) {
	return stream->rate;
}

bool kinc_a1_sound_stream_looping(kinc_a1_sound_stream_t *stream) {
	return stream->myLooping;
}

void kinc_a1_sound_stream_set_looping(kinc_a1_sound_stream_t *stream, bool loop) {
	stream->myLooping = loop;
}

float kinc_a1_sound_stream_volume(kinc_a1_sound_stream_t *stream) {
	return stream->myVolume;
}

void kinc_a1_sound_stream_set_volume(kinc_a1_sound_stream_t *stream, float value) {
	stream->myVolume = value;
}

bool kinc_a1_sound_stream_ended(kinc_a1_sound_stream_t *stream) {
	return stream->end;
}

float kinc_a1_sound_stream_length(kinc_a1_sound_stream_t *stream) {
	if (stream->vorbis == nullptr) return 0;
	return stb_vorbis_stream_length_in_seconds(stream->vorbis);
}

float kinc_a1_sound_stream_position(kinc_a1_sound_stream_t *stream) {
	if (stream->vorbis == nullptr) return 0;
	return stb_vorbis_get_sample_offset(stream->vorbis) / stb_vorbis_stream_length_in_samples(stream->vorbis) * kinc_a1_sound_stream_length(stream);
}

void kinc_a1_sound_stream_reset(kinc_a1_sound_stream_t *stream) {
	if (stream->vorbis != nullptr) stb_vorbis_seek_start(stream->vorbis);
	stream->end = false;
	stream->rateDecodedHack = false;
	stream->decoded = false;
}

float kinc_a1_sound_stream_next_sample(kinc_a1_sound_stream_t *stream) {
	if (stream->vorbis == nullptr) return 0;
	if (stream->rate == 22050) {
		if (stream->rateDecodedHack) {
			if (stream->decoded) {
				stream->decoded = false;
				return stream->samples[0];
			}
			else {
				stream->rateDecodedHack = false;
				stream->decoded = true;
				return stream->samples[1];
			}
		}
	}
	if (stream->decoded) {
		stream->decoded = false;
		if (stream->chans == 1) {
			return stream->samples[0];
		}
		else {
			return stream->samples[1];
		}
	}
	else {
		int read = stb_vorbis_get_samples_float_interleaved(stream->vorbis, stream->chans, &stream->samples[0], stream->chans);
		if (read == 0) {
			if (kinc_a1_sound_stream_looping(stream)) {
				stb_vorbis_seek_start(stream->vorbis);
				stb_vorbis_get_samples_float_interleaved(stream->vorbis, stream->chans, &stream->samples[0], stream->chans);
			}
			else {
				stream->end = true;
				return 0.0f;
			}
		}
		stream->decoded = true;
		stream->rateDecodedHack = true;
		return stream->samples[0];
	}
}
