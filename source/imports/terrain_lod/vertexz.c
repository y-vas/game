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

#ifndef VERTEXZTYPE
# define VERTEXZTYPE

#include "vertexz.h"
#include "globals.h"
#include "math.h"
#include "rand.h"
#include "const.h"
#include <stdio.h>
#include "terrain.h"

vertexZ *vertexZNew(float z) {
	vertexZ *v = (vertexZ *) malloc(sizeof(vertexZ));
	v->z = z;
	
	v->x = 0.0;
	v->y = 0.0;
	v->width = 0.0;
	v->height = 0.0;
	
	v->next = NULL;
	v->prev = NULL;
	v->top = NULL;
	v->bottom = NULL;
	
	v->parent = NULL;
	v->childBL = NULL;
	v->childBR = NULL;
	v->childTL = NULL;
	v->childTR = NULL;
	
	return v;
}

vertList *vertListNew(vertexZ *obj) {
	vertList *v = (vertList *) malloc(sizeof(vertList));
	
	v->v = obj;
	v->next = NULL;
	
	return v;
}

vertList *addList(vertList *list, vertexZ *el) {
	if (list == NULL) {
		// ERROR
		return vertListNew(el);
	}
	if (list->v == NULL) {
		list->v = el;
		return list;
	}
	else {
		vertList *new = vertListNew(el);
		new->next = list;
		return new;
	}
}

void vertListDestroy(vertList *list) {
	vertList *cNode = list;
	while (cNode != NULL) {
		vertList *next = cNode->next;
		free(cNode);
		cNode = next;
	}
}

void initGroundMap() {
	int j, i;
	// Init the first
	global.groundF = vertexZNew(0);
	vertexZ *actual = global.groundF;
	vertexZ *firstOfLine = actual;
	
	actual->x = actual->y = 0.0;
	actual->width = actual->height = global.vertex_width;
	
	// Creating the map
	for (j = 0 ; j < global.gHeight; j++) {
		for (i = 0 ; i < global.gWidth; i++) {
			if (i < global.gWidth - 1) {
				// Creating the right el
				vertexZ *next = vertexZNew(0.0);
				actual->next = next;
				next->prev = actual;
				
				// [FIXIT] set x, y, width and height in vertexZNew
				/*actual->x = i;
				actual->y = j;
				actual->width = 1.0;
				actual->height = 1.0;*/
				
				next->x = global.vertex_width*(i+1.0);
				next->y = global.vertex_width*(j);
				next->width = global.vertex_width*(1.0);
				next->height = global.vertex_width*(1.0);
			}
			if (j > 0 && i > 0) {
				// Linking the top el
				vertexZ *top = actual->prev->top->next;
				actual->top = top;
				top->bottom = actual;
			}
			if (i == global.gWidth - 1 && j < global.gHeight - 1) {
				// Last el of the line
				// creating the first el of the next line
				// -- Avoid creating a new el from the first el on the last line
				vertexZ *newLineEl = vertexZNew(0);
				firstOfLine->bottom = newLineEl;
				newLineEl->top = firstOfLine;
				
				// jumping to the new line
				actual = newLineEl;
				firstOfLine = actual;
				
				newLineEl->x = global.vertex_width*(0.0);
				newLineEl->y = global.vertex_width*(j+1.0);
				newLineEl->width = global.vertex_width*(1.0);
				newLineEl->height = global.vertex_width*(1.0);
			}
			else {
				actual = actual->next;
			}
		}
	}
	
	// Create quadtree (detail level)
	divideVertexToParent(global.groundF, global.gWidth, global.gHeight, 5);
	
	vertexZ *topVert = global.groundF;
	for (i = 0; topVert != NULL; i++) {
		global.topF = topVert;
		topVert = topVert->parent;
	}
}

vertexZ *vertexMoveTo(vertexZ *v, int x, int y) {
	int i = x, j = y;
	if (v == NULL) return NULL;
	
	while(i != 0) {
		if (i > 0) { v = v->next; i--; }
		else if (i < 0) { v = v->prev; i++; }
		if (v == NULL) return NULL;
	}
	
	while(j != 0) {
		if (j > 0) { v = v->top; j--; }
		else if (j < 0) { v = v->bottom; j++; }
		if (v == NULL) return NULL;
	}
	
	return v;
}

void divideVertexToParent(vertexZ *v, float width, float height, unsigned int depth) {
	vertexZ *cur = v;
	vertexZ *firstParent = NULL;
	vertexZ *lastParent = NULL;
	vertexZ *firstOfLineParent = NULL;
	unsigned int i, j;
	
	for (i = 0; i < height; i += 2) {
		vertexZ *firstOfLine = cur;
		
		for (j = 0; j < width; j += 2) {
			if (cur == NULL) { printf("ERROR 1 [%i][%i]\n", i, j); return; }
			
			vertexZ *curParent = divideFourVertex(cur);
			
			if (i == 0 && j == 0) {
				firstParent = curParent;
				firstOfLineParent = curParent;
			}
			
			if (j > 0) {
				// Set prev
				curParent->prev = lastParent;
				lastParent->next = curParent;
			}
			else {
				if (i > 0) {
					// Set top-bottom relation
					firstOfLineParent->bottom = curParent;
					curParent->top = firstOfLineParent;
				}
				
				firstOfLineParent = curParent;
			}
			
			if (j > 0 && i > 0) {
				// Set top
				vertexZ *cTop = lastParent->top->next;
				curParent->top = cTop;
				cTop->bottom = curParent;
			}
			
			// Switch last parent
			lastParent = curParent;
			cur = vertexMoveTo(cur, 2, 0);
		}
		
		cur = vertexMoveTo(firstOfLine, 0, -2);
	}
	
	if ((width > 1.0 || height > 1.0) && depth > 0)
		divideVertexToParent(firstParent, width / 2.0, height / 2.0, depth - 1);
}

vertexZ *divideFourVertex(vertexZ *v) {
	unsigned int i, num = 0;
	float zAv = 0.0;
	vertexZ *vertices[4] = {
		v, // TL
		vertexMoveTo(v, 1, 0), // TR
		vertexMoveTo(v, 0, -1), // BL
		vertexMoveTo(v, 1, -1) // BR
	};
	
	vertexZ *parent = vertexZNew(0.0);
	
	parent->childTL = vertices[0];
	parent->childTR = vertices[1];
	parent->childBL = vertices[2];
	parent->childBR = vertices[3];
	
	parent->x = parent->childTL->x;
	parent->y = parent->childTL->y;
	parent->width = parent->childTL->width * 2.0;
	parent->height = parent->childTL->height * 2.0;
	
	spreadChildrenZToParents(parent);
	
	return parent;
}

void spreadChildrenZToParents(vertexZ *parent) {
	float zAv = 0.0;
	unsigned int i, num = 0;
	vertexZ *vertices[4] = {
		parent->childTL,
		parent->childTR,
		parent->childBL,
		parent->childBR
	};
	
	for (i = 0; i < 4; i++) {
		if (vertices[i] == NULL) continue;
		
		vertices[i]->parent = parent;
		zAv += vertices[i]->z;
		num++;
	}
	
	if (num == 0) return;
	parent->z = zAv / (float)num;
}

void clearGround() {
	// Clear all the Z vertex
	vertexZ *actual = global.groundF;
	vertexZ *firstOnLine = global.groundF;
	int i = 0, j = 0;
	
	while (actual != NULL) {
		vertexZ *next = actual->next;
		vertexZ *bottom = actual->bottom;
		if (bottom == NULL) {
			// Finished
			break;
		}
		else if (next == NULL) {
			// Jumping to the next line
			firstOnLine = actual = firstOnLine->bottom;
			j++;
			i = 0;
		}
		else {
			// Resetting Z to 0
			actual->z = 0;
			next->z = 0;
			bottom->z = 0;
			next->bottom->z = 0;
			
			i++;
			actual = actual->next;
		}
	}
}

float randMapDropFunctionNDegree(float depth, float x, float radius, float n) {
	return depth * pow( (1 - (x / radius)) , n );
}

float randMapDropFunctionSinus(float depth, float x, float radius) {
	return depth * 0.5 * ( cos(x * PI / radius) + 1 );
}

float randMapDropFunctionGauss(float depth, float x, float radius) {
	return depth * pow( EN, - pow(x * 2.5 / radius, 2.0) );
}

float randMapDropFunction(float depth, float x, float radius) {
	return randMapDropFunctionSinus(depth, x, radius);
	/* Other available functions
	return randMapDropFunctionGauss(depth, x, radius);
	return randMapDropFunctionNDegree(depth, x, radius, 5);
	*/
}

int randMapDropRadiusRandom(int x, int max) {
	int t = (int) round( max * pow( EN, - pow((float) x * 2.0 / 100.0, 2.0) ) );
	return t;
}

void randMapDrop() {
	int x = randL(0, global.gWidth-1), depth = randL(3, 25) /*- 15*/,
		y = randL(0, global.gHeight-1), radius = randL(13, (int) round( (float) min(global.gWidth,global.gHeight) * 0.8) ), 
		i = 0, j = 0, n = 0, m = 0;
	vertexZ *actual = global.groundF;
	
	if (depth == 0) { printf("Depth error\n"); return; }
	
	printf("Adding singularity: (%i,%i) d=%i r=%i\n", x,y,depth,radius);
	
	// Go to the master vertex
	while (x != 0) {
		actual = actual->next;
		x--;
	}
	while (y != 0) {
		actual = actual->bottom;
		y--;
	}
	
	vertList *vertices = vertListNew(NULL);
	
	// Vertex spreading algorithm
	for (n = 0; n < 2; n++) {
		// Top- and Bottom-direction spreading loop (top takes care of the 0th line)
		
		vertexZ *masterLine = actual;
		
		if (n == 1) masterLine = actual->bottom;
		if (masterLine == NULL) continue;
		
		for (i = 0; i <= radius; i++) {
			// ith line of vertexes
			
			if (masterLine == NULL) break;
			
			// Determine the half-width of spread for this line
			int lineWidth = (int) floor( pow( pow(radius, 2.0) - pow(i, 2.0), 0.5 ) );
			
			for (m = 0; m < 2; m++) {
				// vertex right- and left-halfline (right takes care of the 0th vertex)
				
				vertexZ *vertexLine = masterLine;
				
				if (m == 1) vertexLine = vertexLine->prev;
				if (vertexLine == NULL) continue;
				
				for (j = 0; j < lineWidth; j++) {
					// Loop for the j vertexes of the half-line part
					
					if (vertexLine == NULL) break;
					
					float vertexDistance = pow( pow(i, 2.0) + pow(j, 2.0) , 0.5);
					vertexLine->z += randMapDropFunction(depth, vertexDistance, radius);
					
					vertices = addList(vertices, vertexLine);
					
					if (m == 0)
						vertexLine = vertexLine->next;
					else
						vertexLine = vertexLine->prev;
				}
			}
			
			if (n == 0)
				masterLine = masterLine->top;
			else
				masterLine = masterLine->bottom;
		}
	}
	
	// [FIXIT] Need some optimisations
	// -- Remove duplicates PARENTS (listUnique...)
	// [FIXIT] WARNING: MEMORY LEAK ! (Seems fixed)
	spreadVertexParents(vertices);
	vertListDestroy(vertices);
}

void spreadVertexParents(vertList *list) {
	vertList *parents = vertListNew(NULL),
		*cur = list;
	
	while(cur->next != NULL) {
		vertexZ *cParent = cur->v->parent;
		if (cParent == NULL) return;
		
		parents = addList(parents, cParent);
		cur = cur->next;
		
		spreadChildrenZToParents(parents->v);
	}
	
	//parents = listUnique(parents);
	spreadVertexParents(parents);
	vertListDestroy(parents);
}

/* List Fusion duplicate algorithm (NOT WORKING)
vertList *listUnique(vertList *list) {
	printf("listUnique: %p\n", list);
	if (list == NULL || list->next == NULL) {
		printf("\tNULL\n");
		return list;
	}
	
	vertList *left = NULL, *right = NULL;
	listPart(list, &left, &right);
	return listUniqueSmall(listUnique(left), listUnique(right));
}

void listPart(vertList *list, vertList **left, vertList **right) {
	printf("listPart: %p (%p ; %p)\n", list, *left, *right);
	do {
		if (list != NULL) {
			printf("\t: %p (%p ; %p)\n", list, *left, *right);
			*left = addList(*left, list->v);
			list = list->next;
		}
		if (list != NULL) {
			printf("\t: %p (%p ; %p)\n", list, *left, *right);
			*right = addList(*right, list->v);
			list = list->next;
		}
	} while(list != NULL);
	printf("\tfinished\n");
}

vertList *listUniqueSmall(vertList *left, vertList *right) {
	printf("listUniqueSmall: (%p ; %p)\n", left, right);
	if (left == NULL) {printf("left null\n"); return right;}
	if (right == NULL) {printf("right null\n"); return left;}
	
	if (left->v == right->v) {
		printf("\t: return %p\n", left);
		return left;
	}
	else {
		printf("\t: return all listUniqueSmall (%p ; %p) %p\n", left, right->next, left->v);
		return addList(listUniqueSmall(left, right->next), left->v);
	}
}
*/

void randWalkMap() {
	int x = randL(0, global.gWidth-1), depth = randL(0, 4) - 2,
		y = randL(0, global.gHeight-1), iter = randL(15, 40), knownsSize = 0;
	vertexZ *actual = global.groundF;
	vertexZ *knowns[iter];
	
	printf("Adding walk: (%i,%i) d=%i i=%i\n", x,y,depth,iter);
	while (x != 0) {
		actual = actual->next;
		x--;
	}
	while (y != 0) {
		actual = actual->bottom;
		y--;
	}
	
	if (depth == 0) depth = 1;
	
	while (iter > 0) {
		int n = randL(0, 3), searchI;
		vertexZ *neighbour[4] = { actual->next, actual->prev, actual->top, actual->bottom };
		vertexZ *target = neighbour[n];
		bool skip = false;
		
		// Checking for NULL
		if (target == NULL) continue;
		
		// Skipping known
		for (searchI = 0; searchI < knownsSize; searchI++) {
			if (knowns[searchI] == target) {
				skip = true;
				break;
			}
		}
		if (skip == true) {
			// Random new start
			actual = knowns[randL(0, knownsSize - 1)];
			continue;
		}
		
		target->z += depth;
		
		knowns[knownsSize] = target;
		knownsSize++;
		actual = target;
		iter--;
	}
}

void drawChildrenTerrain(vertexZ *v, unsigned int depth) {
	unsigned int i;
	vertexZ *children[] = {
		v->childTL,
		v->childTR,
		v->childBL,
		v->childBR
	};
	vertexZ *around[] = {
		vertexMoveTo(v->childTR, 1, 0),
		vertexMoveTo(v->childBR, 1, 0),
		vertexMoveTo(v->childBR, 1, -1),
		vertexMoveTo(v->childBR, 0, -1),
		vertexMoveTo(v->childBL, 0, -1),
	};
	
	if (depth > 1) {
		for (i = 0; i < 4; i++) {
			if (children[i] == NULL) continue;
			drawChildrenTerrain(children[i], depth - 1);
		}
	}
	else {
		for (i = 0; i < 4; i++) {
			if (children[i] == NULL) return;
		}
		
		drawVertices(children[0], children[1], children[2], children[3], 0);
		
		if (around[1] != NULL && around[0] != NULL)
			drawVertices(children[1], around[0], children[3], around[1], 1);
		if (around[3] != NULL && around[1] != NULL)
			drawVertices(children[3], around[1], around[3], around[2], 0);
		if (around[4] != NULL && around[3] != NULL)
			drawVertices(children[2], children[3], around[4], around[3], 1);
	}
}

void drawVertices(vertexZ *a, vertexZ *b, vertexZ *c, vertexZ *d, unsigned int even) {
	float A[] = {a->x, a->y, a->z};
	float B[] = {b->x, b->y, b->z};
	float C[] = {c->x, c->y, c->z};
	float D[] = {d->x, d->y, d->z};
	
	if (even % 2 == 0) {
		drawTriangle(A, B, C);
		drawTriangle(B, D, C);
	}
	else {
		drawTriangle(A, B, D);
		drawTriangle(A, D, C);
	}
}

unsigned int detailOfTerrainCamera(float x, float y, float z) {
	float dX = x + global.cameraX,
		dY = y + global.cameraY, 
		dZ = z - global.cameraDistance, 
		distance = pow( pow(dX,2.0) + pow(dY,2.0) + pow(dZ,2.0) ,0.5);
	
	if (distance < 25.0) return 6;
	if (distance < 50.0) return 5;
	if (distance < 75.0) return 4;
	if (distance < 100.0) return 3;
	if (distance < 200.0) return 2;
	else return 1;
}

void drawTerrain() {
	if (global.quadterrain == true)
		drawTerrainQT();
	else
		drawTerrainStandard();
}

void drawTerrainQT() {
	// 4 different quality area
	vertexZ *cur = global.topF;
	vertexZ *masterLine = cur;
	//unsigned int nn = 0;
	while (cur != NULL) {
		unsigned int lvlDetail = detailOfTerrainCamera(
			cur->x + cur->width/4.0, 
			cur->y + cur->height/4.0, 
			cur->z);
		
		// Calculate basic frustum culling based on dot product
		float cameraView_vector[] = {
			sin(angToRad(getCameraAngleY())) * sin(angToRad(getCameraAngleX())), 
			cos(angToRad(getCameraAngleY())) * sin(angToRad(getCameraAngleX())), 
			cos(angToRad(getCameraAngleX()))
		};
		float cameraToArea_vector[] = {
			global.cameraX + cur->x + cur->width/2.0,
			global.cameraX + cur->y + cur->height/2.0,
			global.cameraDistance - cur->z,
		};
		float terrainSign = dot_product(cameraView_vector, cameraToArea_vector);
		
		if (lvlDetail > 0 && (terrainSign < 0.0 || vector_length(cameraToArea_vector) <= cur->width )) {
			drawChildrenTerrain(cur, lvlDetail);
		}
		
		cur = cur->next;
		if (cur == NULL) { cur = masterLine->bottom; masterLine = cur; }
		//nn++;
	}
}
void drawTerrainStandard() {
	int i = 0, j = 0, k = 0;
	vertexZ *actual = global.groundF;
	vertexZ *firstOnLine = actual;
	
	while (actual != NULL) {
		vertexZ *next = actual->next;
		vertexZ *bottom = actual->bottom;
		if (bottom == NULL) {
			// Finished
			break;
		}
		else if (next == NULL) {
			// Jumping to the next line
			firstOnLine = actual = firstOnLine->bottom;
		
			j++;
			i = 0;
		}
		else {
			// Drawing the 2 triangles
	   		vertexZ *nextbot = next->bottom;
	   		if (nextbot == NULL) {printf("error [%i][%i] %p %p %p\n",i,j,actual,next,bottom); break;}
	   		float a[3] = {i, j, actual->z};
	   		float b[3] = {i+1, j, next->z};
	   		float c[3] = {i, j+1, bottom->z};
	   		float d[3] = {i+1, j+1, nextbot->z};
	   		
	   		if (k == 0) {
	   			drawTriangle(a, b, c);
				drawTriangle(b, d, c);
			}
			else {
	   			drawTriangle(a, d, c);
				drawTriangle(a, b, d);
			}
		
			k = (k + 1) % 2;
			i++;
			actual = actual->next;
		}
	}
}

#endif
