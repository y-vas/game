/*

    Terrain LOD
    Copyright (C) 2010  Axel "Jamesb" ANGEL

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
*/

#ifndef INPUTCALLBACK
# define INPUTCALLBACK

#include "inputcallback.h"

#include <GL/glut.h>
#include "math.h"
#include "const.h"
#include "angles.h"
#include "globals.h"
#include "angles.h"

void cameraMoveForward(float speed) {
	global.cameraX += speed * sin(angToRad(getCameraAngleY()))*sin(angToRad(getCameraAngleX()));
	global.cameraY += speed * cos(angToRad(getCameraAngleY()))*sin(angToRad(getCameraAngleX()));
	global.cameraDistance -= speed * cos(angToRad(getCameraAngleX()));
}

void cameraMoveLeft(float speed) {
	global.cameraX -= speed * cos(angToRad(2.0 * PI - getCameraAngleY()));
	global.cameraY -= speed * sin(angToRad(2.0 * PI - getCameraAngleY()));
}

void cameraMoveTop(float speed) {
     global.cameraX -= speed * sin(angToRad(getCameraAngleY()))*cos(angToRad(getCameraAngleX()));
     global.cameraY -= speed * cos(angToRad(getCameraAngleY()))*cos(angToRad(getCameraAngleX()));
     global.cameraDistance -= speed * sin(angToRad(getCameraAngleX()));
}

void cameraMoveUp(float speed) {
	// Independant from axis, goes up
	global.cameraDistance += speed * 1;
}

void centerMouse() {
	glutWarpPointer((float) global.winWidth / 2.0, (float) global.winHeight / 2.0);
	
	global.mouseX = global.winWidth / 2.0;
	global.mouseY = global.winHeight / 2.0;
}

#endif
