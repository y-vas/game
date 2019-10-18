package kha.audio2;

import kha.Sound;

class Audio {
	private static var buffer: Buffer;

	public static function _init() {
		var bufferSize = 1024 * 2;
		buffer = new Buffer(bufferSize * 4, 2, 44100);
	}

	public static function _callCallback(samples: Int): Void {
		if (buffer == null) return;
		if (audioCallback != null) {
			audioCallback(samples, buffer);
		}
		else {
			for (i in 0...samples) {
				buffer.data.set(buffer.writeLocation, 0);
				buffer.writeLocation += 1;
				if (buffer.writeLocation >= buffer.size) {
					buffer.writeLocation = 0;
				}
			}
		}
	}

	public static function _readSample(): FastFloat {
		if (buffer == null) return 0;
		var value: FastFloat = buffer.data.get(buffer.readLocation);
		++buffer.readLocation;
		if (buffer.readLocation >= buffer.size) {
			buffer.readLocation = 0;
		}
		return value;
	}

	public static var samplesPerSecond: Int;

	public static var audioCallback: Int->Buffer->Void;

	public static function stream(sound: Sound, loop: Bool = false): kha.audio1.AudioChannel {
		return null;
	}
}
