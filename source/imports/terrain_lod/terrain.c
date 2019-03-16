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

#ifndef TERRAIN
# define TERRAIN

#include "terrain.h"

void init(void) {
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	glEnable(GL_DEPTH_TEST);
	//glShadeModel(GL_SMOOTH);
}

void display(void) {
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glColor3f (1.0, 1.0, 1.0);

	// Rotate camera viewpoint
	glPushMatrix();
	glRotatef ((GLfloat) getCameraAngleX(), 1.0, 0.0, 0.0);
	glRotatef ((GLfloat) getCameraAngleY(), 0.0, 0.0, 1.0);
	glTranslatef (global.cameraX, global.cameraY, -global.cameraDistance);

	// LIGHT - Draw cube at light
	glPushMatrix();

	glDisable (GL_LIGHTING);
	glTranslatef(0, 35, 105);
	glRotatef(15.0, 0.0, 0.0, 1.0);
	glColor3f (1.0, 0.0, 0.0);
	glutWireCube (1.0);
	glEnable (GL_LIGHTING);

	GLfloat light_ambient[] = { 0.3, 0.3, 0.3, 1.0 };
	GLfloat light_diffuse[] = { 0.7, 0.7, 0.7, 1.0 };
	GLfloat light_specular[] = { 1.0, 1.0, 1.0, 1.0 };
	GLfloat light_position[] = { 1.0, 0.0, 1.0, 0.0 };
	//GLfloat light_position[] = { 0.0, 0.0, 0.0, 1.0 };
	//GLfloat spot_direction[] = { 1.0, 0.0, -1.0 };

	glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
	glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
	glLightfv(GL_LIGHT0, GL_POSITION, light_position);
	//glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction);
	//glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 45.0);

	glPopMatrix();
	// End light
	
	// Little square targets
	glDisable (GL_LIGHTING);
	
	unsigned int i;
	for (i = 0; i < global.squaresNum; i++) {
		float squareCoord[] = {global.squaresCoord[i][0],
			global.squaresCoord[i][1], 
			global.squaresCoord[i][2]};
		float arrowColor[] = {global.squaresColor[i][0],
			global.squaresColor[i][1], 
			global.squaresColor[i][2]};
		
		
		glPushMatrix();
		glTranslatef(squareCoord[0], squareCoord[1], squareCoord[2]);
		glColor3fv(arrowColor);
		glutWireCube (1.0);
		glPopMatrix();
	}
	
	glEnable (GL_LIGHTING);

	// Save the matrices
	glGetDoublev(GL_MODELVIEW_MATRIX, global.world_modelview);
	glGetDoublev(GL_PROJECTION_MATRIX, global.world_projection);
	glGetIntegerv(GL_VIEWPORT, global.world_viewport);
	
	// Draw the objects (middle)
	drawTerrain();
	
	glPopMatrix();
	
	// Draw interface
	drawInterface();

	glutSwapBuffers();
	
	// Vertices counter
	if (global.verticescounter == true) {
		printf("Total vertices for this frame: %i\n", global.verticesCount);
		global.verticesCount = 0;
	}
}

void reshape (int w, int h) {
	glViewport (0, 0, (GLsizei) w, (GLsizei) h); 
	glMatrixMode (GL_PROJECTION);
	glLoadIdentity ();
	gluPerspective(60.0, (GLfloat) w/(GLfloat) h, 1.0, 500.0);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	global.winWidth = w;
	global.winHeight = h;
	gluLookAt (0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
}

void keyboard (unsigned char key, int x, int y) {
   switch (key) {
      // camera distance control
      case 'W':
         cameraMoveTop(1);
         glutPostRedisplay();
         break;
      case 'S':
         cameraMoveTop(-1);
         glutPostRedisplay();
         break;
      case 'a':
         cameraMoveLeft(-1);
         glutPostRedisplay();
         break;
      case 'd':
         cameraMoveLeft(1);
         glutPostRedisplay();
         break;
      case 'w':
         cameraMoveForward(1);
         glutPostRedisplay();
         break;
      case 's':
         cameraMoveForward(-1);
         glutPostRedisplay();
         break;
	  case 'm':
	  	// Clear
	  	clearGround();
	  	glutPostRedisplay();
	  	break;
      // Add random singularity
      case 'p':
      	 randMapDrop();
      	 glutPostRedisplay();
      	 break;
      case 'o':
      	 randWalkMap();
      	 glutPostRedisplay();
      	 break;
	  	// Clear
	  	clearGround();
	  	glutPostRedisplay();
	  	break;
	  case 'q':
	  	// Wire mode
	  	bool_switch(&global.graphicWireMode);
	  	glutPostRedisplay();
	  	break;
      default:
         break;
   }
}

void mouse(int button, int state, int x, int y) {
	if (button == GLUT_LEFT_BUTTON) {
		if (state == GLUT_DOWN) {
			centerMouse();
			global.mouseLeftOn = true;
		}
		if (state == GLUT_UP)
			global.mouseLeftOn = false;
	}
}

void mouseWheel(int button, int direction, int x, int y) {
	cameraMoveUp(direction);
	glutPostRedisplay();
}

void mouseMove(int x, int y) {
	if (global.mouseX == -1 && global.mouseY == -1) {
		global.mouseX = x;
		global.mouseY = y;
	}
	else if (global.mouseLeftOn == true) {
		int deltaX = x - global.mouseX;
		int deltaY = y - global.mouseY;
		global.cameraAngleY += deltaX;
		global.cameraAngleX += deltaY;
		
		if (getCameraAngleX() < -180.0) setCameraAngleX(-180.0);
		else if (getCameraAngleX() > 0.0) setCameraAngleX(0.0);
		// [FIXIT]
		//if (getCameraAngleY() < 0) setCameraAngleY(360.0 - getCameraAngleY());
		//else if (getCameraAngleY() > 360.0) setCameraAngleY(getCameraAngleY() - 360.0);
		
		centerMouse();
		glutPostRedisplay();
	}
}

int main(int argc, char** argv) {	
	globalInit();
	glutInit(&argc, argv);
	glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
	glutInitWindowSize (global.winWidth, global.winHeight); 
	glutInitWindowPosition (global.winPosX, global.winPosY);
	glutCreateWindow (argv[0]);
	init ();
	initGroundMap ();
	//initQuadTree ();
	glutDisplayFunc(display); 
	glutReshapeFunc(reshape);
	glutKeyboardFunc(keyboard);
	glutMouseFunc(mouse);
	glutMouseWheelFunc (mouseWheel);
	glutMotionFunc(mouseMove);
	glutMainLoop();
	
	return 0;
}

#endif
