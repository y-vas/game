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

#ifndef VECTOR_H
# define VECTOR_H

void vector_create(float *a, float *b, float *c);

void vector_inverse(float *v, float *out);

float vector_length(float a[3]);

void vector_normalise(float a[3]);

void vector_add(float a[3], float b[3], float out[3]);

void cross_product(float a[3], float b[3], float out[3]);

float dot_product(float a[3], float b[3]);

float vector_angle(float a[3], float b[3]);

void vector_project(float a[3], float b[3], float out[3]);

#endif
