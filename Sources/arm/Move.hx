package arm;

import iron.math.Vec4;
import iron.system.Input;
import armory.trait.physics.RigidBody;
import iron.object.CameraObject;
import iron.object.Object;

class Move extends iron.Trait {

	@prop
	var speed:Float = 0.1;
	var keyboard:Keyboard;
	var rb:RigidBody;
	var cam:CameraObject;
	var rotationSpeed:Float = 2.0;

// ------ new ---------------------------------------------------------------
	public function new() {
		super();

// ------- starter ----------------------------------------------------------
		notifyOnInit(function() {
			rb = object.getTrait(RigidBody);
			keyboard = Input.getKeyboard();
			cam = iron.Scene.getCamera("player_camera");
		});

// ------- runing -----------------------------------------------------------
		notifyOnUpdate(function() {
			var move = new Vec4(0, 0, 0);
			fix_camera(rb, cam);

			if (keyboard.down("d")) {
				move.x += speed;
			}
			if (keyboard.down("a")) {
				move.x -= speed;
			}
			if (keyboard.down("w")) {
				move.y += speed;
			}
			if (keyboard.down("s")) {
				move.y -= speed;
			}
			if (keyboard.down("q")) {
				move.z += speed;
			}
			if (keyboard.down("e")) {
				move.z -= speed;
			}
			if (!move.equals(new Vec4(0, 0, 0))) {
				moveObject(move);
			}
		});

// ------- ending ---------------------------------------------------------
		// notifyOnRemove(function() {
		//
		// });

	}

// ------- fix_camera ------------------------------------------------------
	function fix_camera(o:Object, cam:CameraObject ) : Void {
		var pos = o.transform.loc;

		pos.x += 5;
		pos.y += 5;
		pos.z += 5;

		cam.transform.loc = pos;
		cam.buildMatrix();
	}

// ------- moveObject ------------------------------------------------------
	function moveObject( vec:Vec4 ){
		if (rb != null) {

			#if arm_physics
			rb.setLinearVelocity(0, 0, 0);
			rb.setAngularVelocity(0, 0, 0);
			rb.transform.translate(vec.x, vec.y, vec.z);
			rb.syncTransform();
			#end

		} else {
			object.transform.translate(vec.x, vec.y, vec.z);
		}
	}


}
