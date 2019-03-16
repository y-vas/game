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

#ifndef DRAWPRIMITIVES
# define DRAWPRIMITIVES

#include "drawprimitives.h"
#include "math.h"
#include "angles.h"
#include <GL/gl.h>
#include "globals.h"

void drawCircle(float x, float y, float radius, float color[3], float width, unsigned int detail) {
	unsigned int i = 0;
	
	glLineWidth(width);
	glBegin(GL_LINE_LOOP);
		glColor3fv(color);
		//glVertex2f(x, global.winWidth - y);
		for (i = 0; i < 360; i += detail) {
			glVertex2f( x + sin(angToRad(i))*radius, y - cos(angToRad(i))*radius );
		}
	glEnd();
	glLineWidth(1.0);
}

void drawTriangle(float a[3], float b[3], float c[3]) {
	// Calculate normal
	float normal[3];
	float vectA[] = { b[0]-a[0], b[1]-a[1], b[2]-a[2] };
	float vectB[] = { c[0]-a[0], c[1]-a[1], c[2]-a[2] };
	cross_product(vectA, vectB, normal);
	vector_normalise(normal);
	
	// Draw
	if (global.graphicWireMode == true)
	glBegin(GL_LINE_LOOP);
	else
	glBegin(GL_TRIANGLES);
		glNormal3fv(normal);
		glVertex3fv(a);
		glVertex3fv(b);
		glVertex3fv(c);
	glEnd();
	
	// Counter
	if (global.verticescounter == true)
		global.verticesCount += 1;
}

void drawPolygon(float *a, float *b, float *c, float *d) {
	// Calculate the 4 normals
	float normalA[3], normalB[3], normalC[3], normalD[3],
		vectAB[3], vectAD[3]/*,
		vectBC[3], vectBA[3],
		vectCB[3], vectCD[3],
		vectDC[3], vectDA[3]*/;
		
	vector_create(a, b, vectAB);
	vector_create(a, d, vectAD);
	/*vector_create(b, c, vectBC);
	vector_inverse(vectAB, vectBA);
	vector_inverse(vectBC, vectCB);
	vector_create(c, d, vectCD);
	vector_inverse(vectCD, vectDC);
	vector_inverse(vectAD, vectDA);*/
	
	cross_product(vectAB, vectAD, normalA);
	/*cross_product(vectAB, vectBC, normalB);
	cross_product(vectCD, vectCB, normalC);
	cross_product(vectDA, vectDC, normalD);*/
	
	vector_normalise(normalA);
	/*vector_normalise(normalB);
	vector_normalise(normalC);
	vector_normalise(normalD);*/
	
	// Draw
	if (global.graphicWireMode == true)
		glBegin(GL_LINE_LOOP);
	else
		glBegin(GL_POLYGON);
			glNormal3fv(normalA);
			glVertex3fv(a);
			//glNormal3fv(normalB);
			glVertex3fv(b);
			//glNormal3fv(normalC);
			glVertex3fv(c);
			//glNormal3fv(normalD);
			glVertex3fv(d);
		glEnd();
}

#endif
