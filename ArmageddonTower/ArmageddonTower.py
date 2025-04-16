import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 2, -15
rot_x, rot_y = 0, 0

def load_texture(filename):
    img = Image.open(filename)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()
    width, height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return tex_id

def draw_textured_cube(tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    
    # Faces do cubo
    for face in cube_faces:
        for i, vertex in enumerate(face):
            glTexCoord2fv(cube_texcoords[i])
            glVertex3fv(cube_vertices[vertex])
    
    glEnd()

def draw_textured_floor(tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-20, -1, -20)
    glTexCoord2f(10, 0); glVertex3f( 20, -1, -20)
    glTexCoord2f(10, 10); glVertex3f( 20, -1,  20)
    glTexCoord2f(0, 10); glVertex3f(-20, -1,  20)
    glEnd()

def draw_textured_walls(tex_id):
    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Traseira
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-20, -1, -20)
    glTexCoord2f(10, 0); glVertex3f(20, -1, -20)
    glTexCoord2f(10, 10); glVertex3f(20, 20, -20)
    glTexCoord2f(0, 10); glVertex3f(-20, 20, -20)
    glEnd()

    # Esquerda
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-20, -1, -20)
    glTexCoord2f(10, 0); glVertex3f(-20, -1, 20)
    glTexCoord2f(10, 10); glVertex3f(-20, 20, 20)
    glTexCoord2f(0, 10); glVertex3f(-20, 20, -20)
    glEnd()

    # Direita
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(20, -1, -20)
    glTexCoord2f(10, 0); glVertex3f(20, -1, 20)
    glTexCoord2f(10, 10); glVertex3f(20, 20, 20)
    glTexCoord2f(0, 10); glVertex3f(20, 20, -20)
    glEnd()

def init_opengl(display):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.8, 0.3, 0.3, 1.0))  # Luz avermelhada
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 10, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1))

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 80)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

cube_vertices = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
]

cube_faces = [
    (0, 1, 2, 3), (4, 5, 6, 7),
    (0, 1, 5, 4), (2, 3, 7, 6),
    (1, 2, 6, 5), (0, 3, 7, 4)
]

cube_texcoords = [(0, 0), (1, 0), (1, 1), (0, 1)]

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    init_opengl(display)
    tex_cubos = [
    load_texture("sherek.jpg"),
    load_texture("urro.jpg"),
    load_texture("ez.jpg"),
    load_texture("felipe.jpg"),
    load_texture("togordo.jpg"),
    load_texture("tadala.jpg"),
    load_texture("messi.jpg"),
    load_texture("beicola.jpg"),
    load_texture("dolly.jpg"),
    load_texture("pdidi.jpg")
    ]
    tex_piso = load_texture("chao.jpg")
    tex_parede = load_texture("ceu.jpg")

    clock = pygame.time.Clock()
    global camera_x, camera_y, camera_z, rot_x, rot_y

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_w]: camera_z += 0.2
        if keys[K_s]: camera_z -= 0.2
        if keys[K_a]: camera_x += 0.2
        if keys[K_d]: camera_x -= 0.2
        if keys[K_r]: rot_x -= 1
        if keys[K_f]: rot_x += 1
        if keys[K_q]: rot_y -= 1
        if keys[K_e]: rot_y += 1

        glLoadIdentity()
        gluLookAt(camera_x, camera_y, camera_z,
                  camera_x, camera_y, camera_z + 1,
                  0, 1, 0)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_textured_floor(tex_piso)
        draw_textured_walls(tex_parede)

        for i in range(10):
            glPushMatrix()
            glTranslatef(0, i * 2, 0)
            draw_textured_cube(tex_cubos[i])
            glPopMatrix()


        pygame.display.flip()

    pygame.quit()

main()
