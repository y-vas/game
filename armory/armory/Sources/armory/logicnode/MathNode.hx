package armory.logicnode;

class MathNode extends LogicNode {

	public var property0:String;
	public var property1:String; // Clamp

	public function new(tree:LogicTree) {
		super(tree);
	}

	override function get(from:Int):Dynamic {

		var v1:Float = inputs[0].get();
		var v2:Float = inputs[1].get();
		var f = 0.0;
		switch (property0) {
		case "Add":
			f = v1 + v2;
		case "Multiply":
			f = v1 * v2;
		case "Sine":
			f = Math.sin(v1);
		case "Cosine":
			f = Math.cos(v1);
		case "Max":
			f = Math.max(v1, v2);
		case "Min":
			f = Math.min(v1, v2);
		case "Abs":
			f = Math.abs(v1);
		case "Subtract":
			f = v1 - v2;
		case "Divide":
			f = v1 / v2;
		case "Tangent":
			f = Math.tan(v1);
		case "Arcsine":
			f = Math.asin(v1);
		case "Arccosine":
			f = Math.acos(v1);
		case "Arctangent":
			f = Math.atan(v1);
		case "Power":
			f = Math.pow(v1, v2);
		case "Logarithm":
			f = Math.log(v1);
		case "Round":
			f = Math.round(v1);
		case "Less Than":
			f = v1 < v2 ? 1.0 : 0.0;
		case "Greater Than":
			f = v1 > v2 ? 1.0 : 0.0;
		case "Modulo":
			f = v1 % v2;
		case "Arctan2":
			f = Math.atan2(v1, v2);
		case "Floor":
			f = Math.floor(v1);
		case "Ceil":
			f = Math.ceil(v1);
		case "Fract":
			f = f - Std.int(f);
		case "Square Root":
			f = Math.sqrt(v1);
		}

		if (property1 == "true") f = f < 0.0 ? 0.0 : (f > 1.0 ? 1.0 : f);

		return f;
	}
}
