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

#ifndef TERRAIN_H
# define TERRAIN_H

#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "globals.h"
#include "bool.h"
#include "const.h"
#include "vertexz.h"
#include "rand.h"
#include "mathext.h"
#include "angles.h"
#include "vector.h"
#include "interface.h"
#include "drawprimitives.h"
#include "inputcallback.h"

void init(void);

void display(void);

void reshape (int w, int h);

void keyboard (unsigned char key, int x, int y);

void mouse(int button, int state, int x, int y);

void mouseWheel(int button, int direction, int x, int y);

void mouseMove(int x, int y);

int main(int argc, char** argv);

#endif
