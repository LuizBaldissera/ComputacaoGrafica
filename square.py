import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Configuração inicial do OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)  # Ajuste da tela para 800x600
    glMatrixMode(GL_MODELVIEW)

# Função para desenhar um quadrado com linhas
def draw_square_lines():
    glBegin(GL_LINE_LOOP)
    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glEnd()

# Função principal
def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)  # Ajuste para 800x600
    init()
    x, y, z  = 0.0, 0.0, -5.0
    rot_x, rot_y, rot_z = 0.0, 0.0, 0.0
    theta = 0
    running = True
    while running:  # Loop principal do programa
            for event in pygame.event.get():  # Verifica eventos do Pygame
                if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                    running = False  # Sai do loop
                if event.type == KEYDOWN:  # Se uma tecla for pressionada
                    if event.key == K_ESCAPE:  # Se a tecla ESC for pressionada
                        running = False  # Sai do loop e fecha o programa
                    if event.key == K_a:  # Se a tecla A for pressionada
                        x += -0.2  # Move o triângulo para a esquerda
                    if event.key == K_d:  # Se a tecla D for pressionada
                        x += 0.2  # Move o triângulo para a direita
                    if event.key == K_w:  # Se a tecla W for pressionada
                        y += 0.2  # Move o triângulo para cima
                    if event.key == K_s:  # Se a tecla S for pressionada
                        y += -0.2  # Move o triângulo para baixo
                    if event.key == K_f:  # Se a tecla F for pressionada
                        rot_y += 15  # rotaciona para direita
                    if event.key == K_r:  # Se a tecla R for pressionada
                        rot_y += -15  # Rotaciona para esquerca
                    if event.key == K_q:  # Se a tecla F for pressionada
                        rot_x += 15  # rotaciona para direita
                    if event.key == K_e:  # Se a tecla R for pressionada
                        rot_x += -15  # Rotaciona para esquerca
                    if event.key == K_z:  # Se a tecla Z for pressionada
                        z += -0.2  # da zoom
                    if event.key == K_x:  # Se a tecla X for pressionada
                        z += 0.2  # tira zoom
                if event.type == MOUSEBUTTONDOWN:  # Se o usuário rolar o mouse    
                    if event.button == 4:  # Scroll para cima
                        z += -0.2  # da zoom
                    if event.button == 5:  # Scroll para baixo
                        z += 0.2  # tira zoom
               
                
                
            theta += 1    
                

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(x, y, z)  # Posição fixa
            glRotatef(rot_y , 0.0, 1.0, 0.0)  # Aplica a rotação no eixo Y
            glRotatef(theta , 0.0, 0.0, 1.0) 
            glRotatef(rot_x, 1.0, 0.0, 0.0)  # Aplica a rotação no eixo Y
            glColor3f(1.0, 1.0, 1.0)  # Branco
            draw_square_lines()
            pygame.display.flip()
            pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()