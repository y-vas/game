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

#ifndef ANGLES
# define ANGLES

#include "angles.h"
#include "const.h"
#include "globals.h"

float angToRad(float angle) {
	return angle * ANGTORAD;
}

float getCameraAngleY() {
	return global.cameraAngleY*0.05;
}

float getCameraAngleX() {
	return global.cameraAngleX*0.05;
}

float setCameraAngleY(float angle) {
	global.cameraAngleY = angle*20.0;
}

float setCameraAngleX(float angle) {
	global.cameraAngleX = angle*20.0;
}

#endif
