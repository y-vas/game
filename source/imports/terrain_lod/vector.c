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

#ifndef VECTOR
# define VECTOR

#include "vector.h"
#include "math.h"
#include "const.h"

void vector_create(float *a, float *b, float *c) {
	c[0] = b[0]-a[0];
	c[1] = b[1]-a[1];
	c[2] = b[2]-a[2];
}

void vector_inverse(float *v, float *out) {
	out[0] = -v[0];
	out[1] = -v[1];
	out[2] = -v[2];
}

float vector_length(float a[3]) {
	return pow( pow(a[0], 2.0) + pow(a[1], 2.0) + pow(a[2], 2.0), 0.5 );
}

void vector_normalise(float a[3]) {
	float length = vector_length(a);
	
	if (length == 0)
		return;
		
	a[0] /= length;
	a[1] /= length;
	a[2] /= length;
}

void vector_add(float a[3], float b[3], float out[3]) {
	out[0] = a[0]+b[0];
	out[1] = a[1]+b[1];
	out[2] = a[2]+b[2];
}

void cross_product(float a[3], float b[3], float out[3]) {
	out[0] = a[1]*b[2] - b[1]*a[2];
	out[1] = a[2]*b[0] - b[2]*a[0];
	out[2] = a[0]*b[1] - b[0]*a[1];
}

float dot_product(float a[3], float b[3]) {
	return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
}

float vector_angle(float a[3], float b[3]) {
	// Found the angle between vectorsa et b
	
	float dot = dot_product(a, b),
		lena = vector_length(a),
		lenb = vector_length(b);
	
	if (lena == 0.0 || lenb == 0.0) return 0.0;
		
	// Found one of the two possible angles (n, 2pi - n)
	float angleCos = acos( dot / (lena * lenb) );
	float angleCosBis = 2.0 * PI - angleCos;
	
	float cross[3];
	cross_product(a, b, cross);
	float lenSin = vector_length(cross) / (lena * lenb);
	
	if (lenSin >= 0.0)
		return angleCos;
	else
		return angleCosBis;
}

void vector_project(float a[3], float b[3], float out[3]) {
	// Calculate the vector out which is the projection of vector a on b
	
	float lenb = vector_length(b);
	if (lenb == 0.0) return ;
	
	float factor = dot_product(a,b) / (lenb*lenb);
	
	out[0] = factor * b[0];
	out[1] = factor * b[1];
	out[2] = factor * b[2];
}

#endif
