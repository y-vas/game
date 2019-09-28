package kha.arrays;

abstract Int16Array(js.lib.Int16Array) {
	public inline function new(elements: Int) {
		this = new js.lib.Int16Array(elements);
	}
	
	public var length(get, never): Int;

	inline function get_length(): Int {
		return this.length;
	}
	
	public inline function set(index: Int, value: Int): Int {
		return this[index] = value;
	}
	
	public inline function get(index: Int): Int {
		return this[index];
	}
	
	public inline function data(): js.lib.Int16Array {
		return this;
	}

	@:arrayAccess
	public inline function arrayRead(index: Int): Int {
		return this[index];
	}

	@:arrayAccess
	public inline function arrayWrite(index: Int, value: Int): Int {
		return this[index] = value;
	}

	public inline function subarray(start: Int, ?end: Int): Int16Array {
		return cast this.subarray(start, end);
	}
}
