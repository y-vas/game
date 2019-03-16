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

#ifndef GLOBALSTYPE
# define GLOBALSTYPE

#include "globals.h"
#include "terrain.h"

void globalInit() {
	global.quadterrain = true;
	global.vertex_width = 0.5;
	
	global.winPosX = 100;
	global.winPosY = 100;
	global.winWidth = 500;
	global.winHeight = 500;
	
	global.cameraAngleX = -90.0*20.0;
	global.cameraAngleY = 45.0*20.0;
	
	global.gWidth = 1024;
	global.gHeight = 1024;
	global.minVertRadius = 0;
	global.maxVertRadius = 5;
	
	global.squaresNum = 3;
	global.squaresCoord[0][0] = global.gWidth * global.vertex_width / 2.0;
			global.squaresCoord[0][1] = global.gHeight * global.vertex_width / 2.0;
			global.squaresCoord[0][2] = 2.0;
	global.squaresColor[0][0] = 0.25;
			global.squaresColor[0][1] = 0.3;
			global.squaresColor[0][2] = 0.9;
	global.squaresArrowT[0] = 0;
	
	global.squaresCoord[1][0] = 6.0;
			global.squaresCoord[1][1] = 5.0;
			global.squaresCoord[1][2] = 0.0;
	global.squaresColor[1][0] = 0.9;
			global.squaresColor[1][1] = 0.25;
			global.squaresColor[1][2] = 0.3;
	global.squaresArrowT[1] = 1;
			
	global.squaresCoord[2][0] = 65.0;
			global.squaresCoord[2][1] = 55.0;
			global.squaresCoord[2][2] = -15.0;
	global.squaresColor[2][0] = 1.0;
			global.squaresColor[2][1] = 1.0;
			global.squaresColor[2][2] = 0.2;
	global.squaresArrowT[2] = 2;
	
	global.mouseX = -1;
	global.mouseY = -1;
	global.cameraX = 3.0;
	global.cameraY = 3.0;
	global.cameraDistance = 5.0;
	global.mouseLeftOn = false;
	global.mouseRightOn = false;
	global.graphicWireMode = false;
	
	global.groundF = NULL;
	global.topF = NULL;
	//global.quadF = NULL;
	
	global.verticescounter = true;
	global.verticesCount = 0;
}

#endif
