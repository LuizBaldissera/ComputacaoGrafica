import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    vertices = (
        (1, -1, -1), (1, 1, -1),
        (-1, 1, -1), (-1, -1, -1),
        (1, -1, 1), (1, 1, 1),
        (-1, -1, 1), (-1, 1, 1)
    )
    faces = (
        (0, 1, 2, 3),  
        (4, 5, 1, 0),  
        (6, 7, 5, 4),  
        (2, 7, 6, 3),  
        (1, 5, 7, 2), 
        (4, 0, 3, 6)   
    )
    colors = (
        (1, 0, 0),  
        (0, 1, 0),  
        (0, 0, 1),  
        (1, 1, 0),  
        (1, 0, 1),  
        (0, 1, 1)   
    )

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
   
def draw_triangle():
    glColor3f(1, 1, 0)
    glBegin(GL_TRIANGLES)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glEnd()

def draw_pyramid():
    glColor3f(1, 0, 1)
    vertices = [
        [0, 1, 0], [-1, -1, 1],
        [1, -1, 1], [1, -1, -1],
        [-1, -1, -1]
    ]
    faces = [
        (0,1,2), (0,2,3), (0,3,4), (0,4,1),
        (1,2,3), (1,3,4)
    ]
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def show_menu():
    print("Escolha uma opção:")
    print("1 - Cubo")
    print("2 - Triângulo")
    print("3 - Cubo + Triângulo")
    print("4 - Pirâmide")
    print("5 - Cubo + Triângulo + Pirâmide")
    print("6 - Controle individual")
    return int(input("Digite a opção desejada: "))

def main():
    option = show_menu()
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    init()

    # Estados de posição e rotação
    pos = {'x': 0, 'y': 0, 'z': -10}
    rot = {'x': 0, 'y': 0}

    # Posições individuais para opção 6
    cube_pos = [0, 0]
    tri_pos = [0, 0]
    pyr_pos = [0, 0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: running = False
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE: running = False

                # Controles globais (opções 1–5 ou globais da opção 6)
                if option != 6 or key in [K_q, K_e, K_r, K_f, K_z, K_x]:
                    if key == K_w: pos['y'] += 0.2
                    if key == K_s: pos['y'] -= 0.2
                    if key == K_a: pos['x'] -= 0.2
                    if key == K_d: pos['x'] += 0.2
                    if key == K_q: rot['x'] += 10
                    if key == K_e: rot['x'] -= 10
                    if key == K_r: rot['y'] += 10
                    if key == K_f: rot['y'] -= 10
                    if key == K_z: pos['z'] += 0.2
                    if key == K_x: pos['z'] -= 0.2

                # Opção 6 - controles independentes
                if option == 6:
                    # Cubo: IJKL
                    if key == K_i: cube_pos[1] += 0.2
                    if key == K_k: cube_pos[1] -= 0.2
                    if key == K_j: cube_pos[0] -= 0.2
                    if key == K_l: cube_pos[0] += 0.2
                    # Triângulo: GBVN
                    if key == K_g: tri_pos[1] += 0.2
                    if key == K_b: tri_pos[1] -= 0.2
                    if key == K_v: tri_pos[0] -= 0.2
                    if key == K_n: tri_pos[0] += 0.2
                    # Pirâmide: setas
                    if key == K_UP: pyr_pos[1] += 0.2
                    if key == K_DOWN: pyr_pos[1] -= 0.2
                    if key == K_LEFT: pyr_pos[0] -= 0.2
                    if key == K_RIGHT: pyr_pos[0] += 0.2

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(pos['x'], pos['y'], pos['z'])
        glRotatef(rot['x'], 1, 0, 0)
        glRotatef(rot['y'], 0, 1, 0)

        if option == 1:
            draw_cube()
        elif option == 2:
            draw_triangle()
        elif option == 3:
            glPushMatrix()
            glTranslatef(-2, 0, 0)
            draw_cube()
            glPopMatrix()
            glPushMatrix()
            glTranslatef(2, 0, 0)
            draw_triangle()
            glPopMatrix()
        elif option == 4:
            draw_pyramid()
        elif option == 5:
            glPushMatrix()
            glTranslatef(-3, 0, 0)
            draw_cube()
            glPopMatrix()
            glPushMatrix()
            draw_triangle()
            glPopMatrix()
            glPushMatrix()
            glTranslatef(3, 0, 0)
            draw_pyramid()
            glPopMatrix()
        elif option == 6:
            # Controle individual
            glPushMatrix()
            glTranslatef(cube_pos[0]-4, cube_pos[1], 0)
            draw_cube()
            glPopMatrix()
            glPushMatrix()
            glTranslatef(tri_pos[0], tri_pos[1], 0)
            draw_triangle()
            glPopMatrix()
            glPushMatrix()
            glTranslatef(pyr_pos[0]+4, pyr_pos[1], 0)
            draw_pyramid()
            glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
