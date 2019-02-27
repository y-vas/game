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

#ifndef VERTEXZTYPE_H
# define VERTEXZTYPE_H

struct __vertexZ {
	// Height
	float z;
	
	// Position
	float x, y, width, height;
	
	// chained list (in 3D)
	struct __vertexZ *next, *prev, 
		*top, *bottom,
		*parent,
		*childBL, *childBR, *childTL, *childTR;
};
typedef struct __vertexZ vertexZ;

struct __vertList {
	vertexZ *v;
	struct __vertList *next;
};
typedef struct __vertList vertList;

vertList *vertListNew(vertexZ *obj);

vertList *addList(vertList *list, vertexZ *el);

void vertListDestroy(vertList *list);

void spreadVertexParents(vertList *list);

vertList *listUnique(vertList *list);

void listPart(vertList *list, vertList **left, vertList **right);

vertList *listUniqueSmall(vertList *left, vertList *right);

vertexZ *vertexZNew(float z);

void initGroundMap();

vertexZ *vertexMoveTo(vertexZ *v, int x, int y);

void divideVertexToParent(vertexZ *v, float width, float height, unsigned int depth);

vertexZ *divideFourVertex(vertexZ *v);

void spreadChildrenZToParents(vertexZ *parent);

void clearGround();

float randMapDropFunctionNDegree(float depth, float x, float radius, float n);

float randMapDropFunctionSinus(float depth, float x, float radius);

float randMapDropFunctionGauss(float depth, float x, float radius);

float randMapDropFunction(float depth, float x, float radius);

int randMapDropRadiusRandom(int x, int max);

void randMapDrop();

void randWalkMap();

void drawTerrain();

void drawTerrainQT();

void drawTerrainStandard();

void drawChildrenTerrain(vertexZ *v, unsigned int depth);

void drawVertices(vertexZ *a, vertexZ *b, vertexZ *c, vertexZ *d, unsigned int even);

#endif
