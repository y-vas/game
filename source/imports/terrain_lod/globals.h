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

#ifndef GLOBALSTYPE_H
# define GLOBALSTYPE_H

#include <GL/gl.h>
#include "bool.h"
#include "vertexz.h"
#include <stdlib.h>

// Global variables
struct __Globals {
	bool quadterrain;
	float vertex_width;
	
	int winPosX, winPosY, winWidth, winHeight,
		cameraAngleX, cameraAngleY, 
		mouseX, mouseY;
	float cameraX, cameraY, cameraDistance;
	bool mouseLeftOn, mouseRightOn;
	bool graphicWireMode;
	
	// 3D Modelview and Projection matrices
	GLdouble world_modelview[16], world_projection[16];
	GLint world_viewport[4];
	
	// Ground parameters
	int gWidth, gHeight,
		minVertRadius, maxVertRadius;
	
	// Little square targets
	unsigned int squaresNum;
	float squaresCoord[3][3];
	float squaresColor[3][3];
	unsigned int squaresArrowT[3];
	
	// Master vertexZ
	vertexZ *groundF;
	vertexZ *topF;
	// Master vertexQT
	//vertQT *quadF;
	
	bool verticescounter;
	unsigned int verticesCount;
};
typedef struct __Globals Globals;

void globalInit();

Globals global;

#endif
