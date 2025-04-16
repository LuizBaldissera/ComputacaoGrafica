# Importação das bibliotecas necessárias
import pygame                            # Responsável por criar a janela e capturar entrada do teclado
from pygame.locals import *              # Importa constantes úteis do pygame (como teclas)
from OpenGL.GL import *                  # Comandos do OpenGL para renderização (ex: glBegin, glVertex, glEnable)
from OpenGL.GLU import *                 # Comandos utilitários do OpenGL (ex: gluPerspective, gluLookAt)
from PIL import Image                    # Usada para abrir e processar imagens para texturas

# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 0, -10  # Define a posição inicial da câmera (afastada no eixo Z)
rot_x, rot_y = 0, 0                       # Ângulos de rotação da câmera (x para inclinar, y para girar)

# Função que carrega uma imagem e a transforma em textura OpenGL
def load_texture(filename):
    img = Image.open(filename)                           # Abre a imagem com Pillow
    img = img.transpose(Image.FLIP_TOP_BOTTOM)           # Inverte verticalmente (OpenGL considera origem no canto inferior)
    img_data = img.convert("RGBA").tobytes()             # Converte a imagem para bytes RGBA
    width, height = img.size                             # Obtém tamanho da imagem

    tex_id = glGenTextures(1)                            # Gera um novo ID de textura
    glBindTexture(GL_TEXTURE_2D, tex_id)                 # Ativa o ID gerado para as próximas operações
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)  # Cria a textura no OpenGL

    # Define como a textura será tratada:
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)      # Repetir horizontalmente
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)      # Repetir verticalmente
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Suavizar ao ampliar
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Suavizar ao reduzir

    return tex_id  # Retorna o ID da textura para uso posterior




# Função que desenha um cubo com textura aplicada, face por face
def draw_textured_cube():
    glBegin(GL_QUADS)  # Inicia desenho de quadriláteros

    #Explicação:
    # glTexCoord2f(0, 0)
    #→ Indica a coordenada da textura (posição do pixel da imagem que será aplicada no vértice).
    #→ Neste caso, 0,0 representa o canto inferior esquerdo da imagem.
    #--------------------------------
    #glVertex3fv(cube_vertices[0])
    #→ Indica a posição do vértice no espaço 3D onde essa parte da textura será aplicada.

    # FACE TRASEIRA (fundo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[2])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[3])  # superior esquerdo

    # FACE FRONTAL (frente do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # superior esquerdo

    # FACE INFERIOR (base)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[5])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # frontal esquerda

    # FACE SUPERIOR (tampa)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[3])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # frontal esquerda

    # FACE DIREITA (lado direito do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[1])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[5])  # inferior frontal

    # FACE ESQUERDA (lado esquerdo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[3])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[7])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # inferior frontal

    glEnd()  # Finaliza o desenho

def draw_textured_cube_at(x, y, z, tex_id):
    glPushMatrix()                     # Salva o estado atual
    glTranslatef(x, y, z)              # Move o cubo para nova posição
    glBindTexture(GL_TEXTURE_2D, tex_id)
    draw_textured_cube()              # Desenha o cubo com textura
    glPopMatrix()                      # Restaura estado

def draw_textured_floor(tex_id, size=10):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    
    # Mapeamento maior para repetir a textura (opcional)
    glTexCoord2f(0, 0); glVertex3f(-size, -1, -size)
    glTexCoord2f(5, 0); glVertex3f( size, -1, -size)
    glTexCoord2f(5, 5); glVertex3f( size, -1,  size)
    glTexCoord2f(0, 5); glVertex3f(-size, -1,  size)
    
    glEnd()

def draw_textured_wall(tex_id, size=10):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    
    glTexCoord2f(0, 0); glVertex3f(-size, -1, -size)
    glTexCoord2f(5, 0); glVertex3f( size, -1, -size)
    glTexCoord2f(5, 5); glVertex3f( size,  5, -size)
    glTexCoord2f(0, 5); glVertex3f(-size,  5, -size)
    
    glEnd()


# Lista de coordenadas 3D dos vértices do cubo
# Cada vértice é representado por uma tupla (x, y, z)
# Observação: o cubo tem 8 vértices no total
cube_vertices = [
    (-1, -1, -1),  # 0 - canto inferior esquerdo traseiro
    ( 1, -1, -1),  # 1 - canto inferior direito traseiro
    ( 1,  1, -1),  # 2 - canto superior direito traseiro
    (-1,  1, -1),  # 3 - canto superior esquerdo traseiro

    (-1, -1,  1),  # 4 - canto inferior esquerdo frontal
    ( 1, -1,  1),  # 5 - canto inferior direito frontal
    ( 1,  1,  1),  # 6 - canto superior direito frontal
    (-1,  1,  1)   # 7 - canto superior esquerdo frontal
]

# Índices que definem as 6 faces do cubo com 4 vértices cada
cube_faces = [
    (0, 1, 2, 3),  # Traseira
    (4, 5, 6, 7),  # Frontal
    (0, 1, 5, 4),  # Inferior
    (2, 3, 7, 6),  # Superior
    (1, 2, 6, 5),  # Lateral direita
    (0, 3, 7, 4)   # Lateral esquerda
]

# Coordenadas 2D da textura (mapeamento)
cube_texcoords = [
    (0, 0), # canto inferior esquerdo,
    (1, 0), # inferior direito,
    (1, 1), # superior direito,
    (0, 1)  # superior esquerdo
]

# Função para configurar o ambiente OpenGL (chamada uma vez no início)
def init_opengl(display):
    glEnable(GL_DEPTH_TEST)                 # Ativa o teste de profundidade (necessário para renderização 3D correta)
    glEnable(GL_TEXTURE_2D)                 # Ativa o uso de texturas 2D

    # Define iluminação ambiente básica
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.0, 0.0, 1.0, 1.0))  # Luz ambiente azul
    # Configura uma luz pontual (GL_LIGHT0)
    glEnable(GL_LIGHTING)                   # Ativa o sistema de iluminação do OpenGL
    glEnable(GL_LIGHT0)                     # Ativa a luz 0
    glLightfv(GL_LIGHT0, GL_POSITION, (0, -5, -5, 0))          # Posição da luz no espaço 3D
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))     # Componente difusa (cor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1))    # Componente especular (brilho)

    # Define propriedades do material aplicado ao cubo
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  # Reflexão ambiente e difusa
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))             # Reflexão especular (brilho branco)
    glMaterialf(GL_FRONT, GL_SHININESS, 80)                               # Fator de brilho

    # Define projeção de perspectiva (campo de visão, proporção, plano próximo e distante)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Função principal do programa
def main():
    pygame.init()                                          # Inicializa o Pygame
    display = (800, 600)                                   # Define tamanho da janela
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)   # Cria janela com OpenGL e buffer duplo

    init_opengl(display)                                   # Chama configuração do ambiente OpenGL
    tex_id = load_texture("textura.jpg")                   # Carrega textura da imagem "textura.jpg"
    tex_id2 = load_texture("texturamadeira.jpg")
    tex_id3 = load_texture("texturagrama.jpg")             # Mais texturas
    tex_id4 = load_texture("texturatijolo.jpg")
    tex_id5 = load_texture("beicola.jpg")
    tex_id6 = load_texture("urro.jpg")             
    tex_id7 = load_texture("sherek.jpg")  
    clock = pygame.time.Clock()                            # Relógio para limitar FPS
    global camera_x, camera_y, camera_z, rot_x, rot_y      # Acessa variáveis globais da câmera

    running = True
    while running:
        clock.tick(60)                                     # Limita a 60 frames por segundo

        for event in pygame.event.get():                   # Captura eventos (ex: fechar a janela)
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()                    # Captura teclas pressionadas

        # Translação da câmera com teclas WASD e profundidade com W/S
        if keys[K_w]: camera_z += 0.1                      # Move para frente
        if keys[K_s]: camera_z -= 0.1                      # Move para trás
        if keys[K_a]: camera_x += 0.1                      # Move para a esquerda
        if keys[K_d]: camera_x -= 0.1                      # Move para a direita

        # Rotação da cena com teclas Q/E (giro Y) e R/F (inclinação X)
        if keys[K_q]: rot_y -= 1                           # Gira cena para esquerda (eixo Y)
        if keys[K_e]: rot_y += 1                           # Gira para direita
        if keys[K_r]: rot_x -= 1                           # Inclina para cima (eixo X)
        if keys[K_f]: rot_x += 1                           # Inclina para baixo


        # Define o ponto de observação da câmera (olha sempre para frente no eixo Z positivo)
        target_x = camera_x        # Olha para frente, mantendo a mesma linha no eixo X
        target_y = camera_y        # Mesma altura
        target_z = camera_z + 1    # Um passo à frente na direção Z

        # Define transformações da câmera
        glLoadIdentity()
        #Exemplo gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ)
        gluLookAt(camera_x, camera_y, camera_z,  # posição da câmera no mundo 3D (olho)
                  target_x, target_y, target_z,  # ponto para onde a câmera está olhando, vai virar a lente nesta direção
                  0, 1, 0)                       # vetor 'para cima' (eixo Y positivo) Isso evita que a imagem fique de cabeça para baixo.
        
        glRotatef(rot_x, 1, 0, 0)                                # Rotação vertical
        glRotatef(rot_y, 0, 1, 0)                                # Rotação horizontal

        # Limpa buffers de cor e profundidade para novo frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Aplica a textura e desenha o cubo
        glBindTexture(GL_TEXTURE_2D, tex_id)
        draw_textured_cube()

        # Primeiro cubo na posição padrão
        glBindTexture(GL_TEXTURE_2D, tex_id)
        draw_textured_cube()

        # Segundo cubo à direita (ex: 3 unidades no eixo X)
        draw_textured_cube_at(3, 0, 0, tex_id2)

        draw_textured_floor(tex_id3)
        draw_textured_wall(tex_id4)

        texturas = [tex_id5, tex_id6, tex_id7]

        for i in range(3):  # 3 cubos empilhados
            glPushMatrix()
            glTranslatef(-3, i * 2.0, 0)  # sobe no eixo Y
            glBindTexture(GL_TEXTURE_2D, texturas[i])
            draw_textured_cube()
            glPopMatrix()

        # Atualiza o conteúdo da janela (renderiza frame)
        pygame.display.flip()

    pygame.quit()  # Finaliza o Pygame

# Inicia o programa
main()
