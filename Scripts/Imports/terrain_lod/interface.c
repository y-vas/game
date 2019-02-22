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

#ifndef INTERFACE
# define INTERFACE

#include "interface.h"
#include "math.h"
#include "mathext.h"
#include "globals.h"
#include "const.h"
#include "angles.h"
#include "vector.h"
#include "drawprimitives.h"

bool getVisibleOnScreen(float coord[3], GLdouble screen[3]) {
	GLdouble screenX, screenY, screenZ;
	
	// Calculte the object position on the screen
	gluProject(coord[0], coord[1], coord[2], 
		global.world_modelview, global.world_projection, global.world_viewport, 
		&screen[0], &screen[1], &screen[2]);
	
	// Check visibility of the object
	if (0 <= screen[0] && screen[0] <= (float) global.winWidth &&
		0 <= screen[1] && screen[1] <= (float) global.winHeight &&
		screen[2] <= 1.0)
			return true;
	else
			return false;
}

void drawInterfaceArrowBold(float innerAngle, float width, float length, float color[3]) {
	// Draw an thin arrow made of 2 rectangles
	float angle = asin(width / length), lengthY = cos( angle ) * length;
	
	// Left part
	glPushMatrix();
	glBegin(GL_POLYGON);
		glColor3fv(color);
		glVertex2f(0.0, 0.0);
		glVertex2f(width,  lengthY);
		glVertex2f(0.0, lengthY - width/tan( angToRad(innerAngle) ));
	glEnd();
	glPopMatrix();

	// Right part
	glPushMatrix();
	glScalef(-1.0, 1.0, 1.0);
	glBegin(GL_POLYGON);
		glColor3fv(color);
		glVertex2f(0.0, 0.0);
		glVertex2f(width,  lengthY);
		glVertex2f(0.0, lengthY - width/tan( angToRad(innerAngle) ));
	glEnd();
	glPopMatrix();
}


void drawInterfaceArrowThin(float innerAngle, float width, float length, float color[3]) {
	// Draw an thin arrow made of 2 rectangles
	
	// Left part
	glPushMatrix();
	glRotatef(-innerAngle, 0.0, 0.0, 1.0);
	glBegin(GL_POLYGON);
		glColor3fv(color);
		glVertex2f(0.0, 0.0);
		glVertex2f(0.0, length);
		glVertex2f(-width, length);
		glVertex2f(-width, 0.0);
	glEnd();
	glPopMatrix();

	// Right part
	glPushMatrix();
	glRotatef(innerAngle, 0.0, 0.0, 1.0);
	glTranslatef(width, 0.0, 0.0);
	glBegin(GL_POLYGON);
		glColor3fv(color);
		glVertex2f(0.0, 0.0);
		glVertex2f(0.0, length);
		glVertex2f(-width, length);
		glVertex2f(-width, 0.0);
	glEnd();
	glPopMatrix();
}

void drawInterfaceDirectionArrow(float angle, unsigned int type, float color[3]) {
	// -- unit direction arrows
	float arrTopMax = 0.05 * global.winHeight, arrBotMax = arrTopMax, 
		arrRadius = min(global.winHeight, global.winWidth)*0.9/2.0;
	
	// Draw the arrow
	glPushMatrix();
	glTranslatef(global.winWidth / 2.0 + arrRadius*cos(angToRad(angle - 90.0)), 
		global.winHeight / 2.0 +  arrRadius*sin(angToRad(angle - 90.0)), 0.0);
	glRotatef(angle, 0.0, 0.0, 1.0);
	
	switch (type) {
		case 1: drawInterfaceArrowBold(65.0, 25.0, 60.0, color); break;
		default: drawInterfaceArrowThin(45.0, 6.0, 60.0, color); break;
	}

	glPopMatrix();
}

void drawInterfacePreciseAimSquare(float width, float color[3]) {
	glBegin(GL_LINE_LOOP);
		glColor3fv(color);
		glVertex2f(0.0, -width);
		glVertex2f(-width, 0.0);
		glVertex2f(0.0, width);
		glVertex2f(width, 0.0);
	glEnd();
}

void drawInterfaceObjectDirectionArrow(float coord[3], unsigned int arrowType, float color[3], bool preciseAim, bool seeThrough) {
	// Directions-indicating arrows (HUD)
	float arrTopMax = 0.05 * global.winHeight, arrBotMax = arrTopMax, 
		arrRadius = min(global.winHeight, global.winWidth)*0.9/2.0, arrWidth = 6.0, 
		arrAngle = -25.0, arrInnerAngle = 45.0, arrLen = 60.0;
		
	// Calculate the projected vector of the object position
	// in the camera plane to find the angle
	float cameraToObject_vector[] = {coord[0] + global.cameraX, coord[1] + global.cameraY, coord[2] - global.cameraDistance};
	float cameraView_vector[] = {
		sin(angToRad(getCameraAngleY())) * sin(angToRad(getCameraAngleX())), 
		cos(angToRad(getCameraAngleY())) * sin(angToRad(getCameraAngleX())), 
		cos(angToRad(getCameraAngleX())) };
	float cameraUp_vector[] = {
		sin(angToRad(getCameraAngleY())) * sin(angToRad(getCameraAngleX()) + PI / 2.0), 
		cos(angToRad(getCameraAngleY())) * sin(angToRad(getCameraAngleX()) + PI / 2.0), 
		cos(angToRad(getCameraAngleX()) + PI / 2.0) };
	float cameraLeft_vector[3], 
		objectProjectedX_vector[3], objectProjectedY_vector[3],
		objectProjected_vector[3];
	
	float cameraViewObject_length = vector_length(cameraToObject_vector);
	float cameraViewObject_angle = PI - vector_angle(cameraToObject_vector, cameraView_vector);
	cross_product(cameraView_vector, cameraUp_vector, cameraLeft_vector);
	vector_normalise(cameraLeft_vector);
	
	// Project the vector in the camera plane
	vector_project(cameraToObject_vector, cameraUp_vector, objectProjectedX_vector);
	vector_project(cameraToObject_vector, cameraLeft_vector, objectProjectedY_vector);
	vector_add(objectProjectedX_vector, objectProjectedY_vector, objectProjected_vector);
	
	float cameraToObjectOrientation = dot_product(cameraLeft_vector, objectProjectedY_vector);
	arrAngle = vector_angle(objectProjected_vector, cameraUp_vector) * 180.0 / PI;
	
	// Calculate whether the angle is postive (clockwise), if not correct it
	if (cameraToObjectOrientation > 0.0)
		arrAngle = 360.0 - arrAngle;
	
	float objectProjected_len = vector_length(objectProjected_vector),
		targetAimed_maxlen = 1.5;
	
	// Calculte the object position on the screen
	GLdouble screenCoord[3];
	bool objInScreen = getVisibleOnScreen(coord, screenCoord);
	
	if (objInScreen == true && cameraViewObject_length >= 15.0 && seeThrough == true) {
		// See through when object is in camera view
		drawCircle(screenCoord[0], global.winHeight - screenCoord[1], 15.0, color, 2.0, 60);
	}
	if (objInScreen == false) {
		// Draw the arrow
		drawInterfaceDirectionArrow(arrAngle, arrowType, color);
	}
	if (objInScreen == true && objectProjected_len < targetAimed_maxlen && preciseAim == true) {
		// Draw a blue square (precise aim)
		float shapeW = objectProjected_len * 120.0 / targetAimed_maxlen;
		
		glPushMatrix();
		glTranslatef(global.winWidth / 2.0, global.winHeight / 2.0, 0.0);
		drawInterfacePreciseAimSquare(shapeW, color);
		glPopMatrix();
	}
}

void drawInterface() {
	glDisable(GL_DEPTH_TEST);
	glDisable (GL_LIGHTING);
	
	glMatrixMode(GL_PROJECTION);			// Select Projection
	glPushMatrix();							// Push The Matrix
	glLoadIdentity();						// Reset The Matrix
	glOrtho( 0, global.winWidth , global.winHeight , 0, -1, 1 );			// Select Ortho Mode
	glMatrixMode(GL_MODELVIEW);				// Select Modelview Matrix
	glPushMatrix();							// Push The Matrix
	glLoadIdentity();						// Reset The Matrix
	
	// Draw
	// -- Selection panel
	/*
	float selectTop = global.winHeight - minf(0.2*global.winHeight, 110.0), selectLeft = global.winWidth / 2.0 - global.winWidth * 0.2,
		selectRight = global.winWidth / 2.0 + global.winWidth * 0.2, selectBot = global.winHeight;
	
	glBegin(GL_POLYGON);
		glColor3f(1.0, 1.0, 1.0);
		glVertex2f(selectLeft, selectBot);
		glVertex2f(selectLeft, selectTop);
		glVertex2f(selectRight, selectTop);
		glVertex2f(selectRight, selectBot);
	glEnd();
	*/
	
	// Draw the arrow direction to a square at the middle of the map
	unsigned int i;
	for (i = 0; i < global.squaresNum; i++) {
		float squareCoord[] = {global.squaresCoord[i][0],
			global.squaresCoord[i][1], 
			global.squaresCoord[i][2]};
		float arrowColor[] = {global.squaresColor[i][0],
			global.squaresColor[i][1], 
			global.squaresColor[i][2]};
		drawInterfaceObjectDirectionArrow(squareCoord, global.squaresArrowT[i], arrowColor, false, true);
	}
	
	// Back to 3D
	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glMatrixMode(GL_MODELVIEW);
	glPopMatrix();
	
	glEnable(GL_DEPTH_TEST);
	glEnable (GL_LIGHTING);
}

#endif
