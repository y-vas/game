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

#ifndef INTERFACE_H
# define INTERFACE_H

#include "bool.h"
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

bool getVisibleOnScreen(float coord[3], GLdouble screen[3]);

void drawInterfaceArrowBold(float innerAngle, float width, float length, float color[3]);

void drawInterfaceArrowThin(float innerAngle, float width, float length, float color[3]);

void drawInterfacePreciseAimSquare(float width, float color[3]);

void drawInterfaceDirectionArrow(float angle, unsigned int type, float color[3]);

void drawInterfaceObjectDirectionArrow(float coord[3], unsigned int arrowType, float color[3], bool preciseAim, bool seeThrough);

void drawInterfaceObjectDirectionArrow(float coord[3], unsigned int arrowType, float color[3], bool preciseAim, bool seeThrough);

#endif
