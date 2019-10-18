package armory.logicnode;

import iron.math.Vec4;

class VectorMathNode extends LogicNode {

	public var property0:String;
	var v = new Vec4();

	public function new(tree:LogicTree) {
		super(tree);
	}

	override function get(from:Int):Dynamic {
		var v1:Vec4 = inputs[0].get();
		var v2:Vec4 = inputs[1].get();
		if (v1 == null || v2 == null) return null;
		v.setFrom(v1);
		var f = 0.0;
		switch (property0) {
		case "Add":
			v.add(v2);
		case "Subtract":
			v.sub(v2);
		case "Average":
			v.add(v2);
			v.x *= 0.5;
			v.y *= 0.5;
			v.z *= 0.5;
		case "Dot Product":
			f = v.dot(v2);
			v.set(f, f, f);
		case "Cross Product":
			v.cross(v2);
		case "Normalize":
			v.normalize();
		case "Multiply":
			v.x *= v2.x;
			v.y *= v2.y;
			v.z *= v2.z;
		case "Length":
			f = v.length();
		case "Distance":
			f = v.distanceTo(v2);
		}

		if (from == 0) return v;
		else return f;
	}
}
