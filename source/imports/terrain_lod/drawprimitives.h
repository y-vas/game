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

#ifndef DRAWPRIMITIVES_H
# define DRAWPRIMITIVES_H

void drawCircle(float x, float y, float radius, float color[3], float width, unsigned int detail);

void drawTriangle(float a[3], float b[3], float c[3]);

void drawPolygon(float *a, float *b, float *c, float *d);

#endif
