package kha.compute;

import kha.graphics4.VertexData;

class ShaderStorageBuffer {
	public var _buffer: Pointer;
	private var data: Array<Int>;
	private var myCount: Int;
	
	public function new(indexCount: Int, type: VertexData) {
		
	}
  
	private function init(indexCount: Int, type: VertexData) {
		
	}
	
	public function delete(): Void {
		
	}
	
	public function lock(): Array<Int> {
		return data;
	}
	
	public function unlock(): Void {
		
	}
	
	public function count(): Int {
		return myCount;
	}
}
