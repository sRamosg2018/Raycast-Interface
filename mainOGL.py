import sys
import numpy
import interface

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

WIDTH = 1600
HEIGHT = 900

PI = math.pi
P2 = PI / 2  # 90º
P3 = 3 * PI / 2  # 270º

gridX = 8
gridY = 8

grid = interface.interface()
grid_length = len(grid)

RADIAN = math.radians(1)

tiles_to_color = set()


class Point:

    def __init__(self, px, py):
        self.px = px
        self.py = py
        self.angle = 1
        self.pdx = math.cos(self.angle) * 5
        self.pdy = math.sin(self.angle) * 5


class Raygun:

    def __init__(self):
        # INTEGER
        self.mx = 0  # Muro
        self.my = 0
        self.mp = 0
        self.dof = 0  # Depth of field
        # FLOATS
        self.rx = 0
        self.ry = 0
        self.rangle = 1
        self.xo = 0
        self.yo = 0
        self.finalDistance = 0

    def draw_rays(self):
        # Horizontal variables
        hdist = sys.maxsize  # horizontal distance
        hx = point.px
        hy = point.py

        # Vetical variables
        vdist = sys.maxsize  # vertical distance
        vx = point.px
        vy = point.py

        # draw horizontal rays
        self.rangle = point.angle - RADIAN * 30  # Ángulo con el que se inicializan los rayos. Point.angle es el "personaje", se le resta 30 radianes, pero se emiten 60. Por lo cual lado izquierda y derecho tienen 30 de vision
        if self.rangle < 0:
            self.rangle += 2 * PI
        if self.rangle > 2 * PI:
            self.rangle -= 2 * PI

        for i in range(0, 60):  # Number of rays

            self.dof = 0

            arctan = -1 / math.tan(self.rangle)
            if self.rangle > PI:
                self.ry = ((int(point.py) // 64) * 64) - 1  # Looking up
                self.rx = (point.py - self.ry) * arctan + point.px
                self.yo = -64
                self.xo = -self.yo * arctan
            if self.rangle < PI:  # Looking down
                self.ry = ((int(point.py) // 64) * 64) + 64
                self.rx = (point.py - self.ry) * arctan + point.px
                self.yo = 64
                self.xo = -self.yo * arctan
            if self.rangle == 0 or self.rangle == PI:
                self.rx = point.px
                self.ry = point.py
                self.dof = 8

            while self.dof < 8:

                self.mx = int(self.rx) // 64
                self.my = int(self.ry) // 64
                self.mp = self.my * gridX + self.mx

                # print(self.mp)
                if 0 < self.mp < gridX * gridY and grid[self.mp] == 1:  # se choca contra un muro
                    self.dof = 8
                    hx = self.rx
                    hy = self.ry
                    hdist = math.dist([point.px, point.py], [hx, hy])

                else:  # sigue avanzando al siguiente cuadrado
                    self.rx += self.xo
                    self.ry += self.yo
                    self.dof += 1

            # draw vertical rays

            self.dof = 0
            nTan = -math.tan(self.rangle)
            if P2 < self.rangle < P3:
                self.rx = ((int(point.px) // 64) * 64) - 1  # Looking upd
                self.ry = (point.px - self.rx) * nTan + point.py
                self.xo = -64
                self.yo = -self.xo * nTan
            if self.rangle < P2 or self.rangle > P3:  # Looking down

                self.rx = ((int(point.px) // 64) * 64) + 64
                self.ry = (point.px - self.rx) * nTan + point.py
                self.xo = 64
                self.yo = -self.xo * nTan
            if self.rangle == 0 or self.rangle == PI:
                self.rx = point.px
                self.ry = point.py
                self.dof = 8

            while self.dof < 8:

                self.mx = int(self.rx) // 64
                self.my = int(self.ry) // 64
                self.mp = self.my * gridX + self.mx

                # print(self.mp)
                if 0 < self.mp < gridX * gridY and grid[self.mp] == 1:  # se choca con un muro
                    self.dof = 8
                    vx = self.rx
                    vy = self.ry
                    vdist = math.dist([point.px, point.py], [vx, vy])

                else:  # contrinua avanzando
                    self.rx += self.xo
                    self.ry += self.yo
                    self.dof += 1

            if vdist < hdist:
                self.rx = vx
                self.ry = vy
                self.finalDistance = vdist
            else:
                self.rx = hx
                self.ry = hy
                self.finalDistance = hdist

            glColor(1, 0, 0)
            glLineWidth(1)
            glBegin(GL_LINES)
            glVertex2i(int(point.px), int(point.py))
            glVertex2i(int(self.rx), int(self.ry))
            glEnd()

            # print(int(self.rx), int(self.ry))

            if (int(self.rx / 64) + gridX * int(self.ry / 64)) not in tiles_to_color:
                tiles_to_color.add((int(self.rx / 64) + gridX * int(self.ry / 64)))
                glutPostRedisplay()

            # 3D WALLS
            line = int((grid_length * 320) / self.finalDistance)
            if line > 320:
                line = 320

            offset = int(160 - line / 2)

            glLineWidth(8)
            glBegin(GL_LINES)
            glVertex2i(i * 8 + 700,
                       0 + offset)  # Coordernada X: El 700 hace referencia al numero de unidades desplazadas hacia la derecha, para comenzar la "pantalla del 3D" ahí
            glVertex2i(i * 8 + 700,
                       line + offset)  # Coordenada Y: Es la distancia vertical entre un punto y otro, es decir, es el alto de la "pantalla del 3D"
            glEnd()
            # glutPostRedisplay()
            self.rangle += RADIAN
            if self.rangle < 0:
                self.rangle += 2 * PI
            if self.rangle > 2 * PI:
                self.rangle -= 2 * PI


def drawMap():
    print(tiles_to_color)

    # Pintar la casillas que estan siendo apuntados por los rayos
    for y in range(0, gridY):
        for x in range(0, gridX):

            # Si choca entonces se colorea de amarillo
            if (x + gridX * y) in tiles_to_color:
                glColor3f(1, 1, 0)
                tiles_to_color.remove((x + gridX * y))

            # En otro caso se mantiene de color blanco
            elif grid[(x + gridX * y)] == 1:
                glColor3f(1, 1, 1)
            # Si no es un muro se mantiene negro
            else:
                glColor3f(0, 0, 0)
            xo = x * grid_length  # grid_length = 64
            yo = y * grid_length  # grid_length = 64

            # Dibujar con plantilla

            glBegin(GL_QUADS)  # "Comienza a recibir vertices para formar un cuadrilatero"
            glVertex2i(xo + 1, yo + 1)
            glVertex2i(xo + 1, yo + grid_length - 1)
            glVertex2i(xo + grid_length - 1, yo + grid_length - 1)
            glVertex2i(xo + grid_length - 1, yo + 1)
            glEnd()  # Termina de recibir vertices


def buttons(key, x, y):
    key = chr(key[0])

    # print(key)
    if key == 'a':
        point.angle -= 0.1
        if point.angle < 0:
            point.angle += 2 * PI
        point.pdx = math.cos(point.angle) * 5
        point.pdy = math.sin(point.angle) * 5

    if key == 'd':
        point.angle += 0.1
        if point.angle > 2 * PI:
            point.angle -= 2 * PI
        point.pdx = math.cos(point.angle) * 5
        point.pdy = math.sin(point.angle) * 5
    if key == 'w':
        # print(point.px, point.py)
        # print(point.pdx, point.pdy)
        point.px += int(point.pdx)
        point.py += int(point.pdy)
    if key == 's':
        # print(point.px, point.py)
        # print(point.pdx, point.pdy)
        point.px -= int(point.pdx)
        point.py -= int(point.pdy)
    # glutPostRedisplay()


def drawPlayer():
    raygun.draw_rays()
    glColor3f(1, 1, 0)
    glPointSize(8)
    glBegin(GL_POINTS)
    glVertex2i(int(point.px), int(point.py))
    glEnd()

    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex2i(int(point.px), int(point.py))
    glVertex2i(int(point.px + point.pdx * 5), int(point.py + point.pdy * 5))
    glEnd()


def init():
    glClearColor(0.3, 0.3, 0.3, 0)
    gluOrtho2D(0, WIDTH, HEIGHT, 0)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawMap()
    drawPlayer()
    glutSwapBuffers()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("RAYCASTER")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


if "__main__" == __name__:
    point = Point(300, 300)
    raygun = Raygun()
    main()
