# Ex7_Carregando_Objeto.py
# Renderiza um modelo OBJ com textura usando OpenGL moderno (VAO/VBO, shaders).
# Simplificado: carrega apenas vértices e UVs (sem normais) para facilitar o entendimento.
#
# Arquivos necessários na mesma pasta:
#   - chibi.obj          : modelo 3D
#   - chibi.png          : textura PNG
#   - Camera.py          : classe Camera (yaw/pitch, get_view_matrix, process_keyboard)
#   - TextureLoader.py   : função load_texture(path, texture_id)
#   - ObjLoaderSimple.py : função load_obj(path) → (vertex_buffer, num_vertices)

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from TextureLoader import load_texture      # Carrega imagens PNG como textura OpenGL
from Camera import Camera                   # Gera a view matrix a partir de yaw/pitch
from ObjLoaderSimple import ObjLoaderSimple # Loader simples que retorna (buffer, num_vertices)
import pyrr
from pyrr import matrix44, Vector3    # ← adicione esta linha
import ctypes

# --- Parâmetros da janela ---
WIDTH, HEIGHT = 800, 600

# --- Variáveis globais ---
Window = None           # Handle da janela GLFW
Shader_programm = None  # ID do programa de shaders
vao_objeto = None       # ID do VAO do objeto
num_vertices = 0        # Quantidade de vértices a desenhar
obj_textura = None      # ID da textura UV

# Instância da câmera para controle WASD
cam = Camera()

# ----------------------------------------
# Configurações de GLFW e OpenGL
# ----------------------------------------

def redimensiona_callback(window, w, h):
    """
    Chamado quando a janela é redimensionada.
    Ajusta as variáveis WIDTH e HEIGHT para manter a proporção.
    """
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = w, h
    glViewport(0, 0, WIDTH, HEIGHT)

def teclado_callback(window, key, scancode, action, mods):
    """
    Fechar a janela ao pressionar ESC.
    """
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)



# Guarda a última posição do mouse
first_mouse = True
lastX, lastY = WIDTH/2, HEIGHT/2

def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY
    if first_mouse:
        lastX, lastY = xpos, ypos
        first_mouse = False

    # offset = nova posição – posição anterior
    xoffset = xpos - lastX
    yoffset = lastY - ypos      # invertendo y para que “pra cima” seja positivo

    lastX, lastY = xpos, ypos

    # chama o método da câmera
    cam.process_mouse_movement(xoffset, yoffset)




def inicializa_opengl():
    """
    Inicializa GLFW, cria a janela e configura callbacks.
    """
    global Window
    if not glfw.init():
        raise RuntimeError("Falha ao inicializar GLFW")
    Window = glfw.create_window(WIDTH, HEIGHT, "Ex7 - OBJ com Textura", None, None)
    if not Window:
        glfw.terminate()
        raise RuntimeError("Falha ao criar janela")
    
    # redimensiona e teclado continuam como antes…
    glfw.set_window_size_callback(Window, redimensiona_callback)  
    glfw.set_key_callback(Window, teclado_callback)
    glfw.make_context_current(Window)
    
    # esconde e captura o cursor para receber movimento contínuo
    glfw.set_input_mode(Window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    # registra nosso callback
    glfw.set_cursor_pos_callback(Window, mouse_callback)

    # Ativa teste de profundidade
    glEnable(GL_DEPTH_TEST)
    print("OpenGL:", glGetString(GL_VERSION).decode())

# ----------------------------------------
# Carregamento de objeto e textura
# ----------------------------------------

vaos = []
vbos = []
num_vertices_list = []
texturas = []
modelos = [
    ("meshes/chibi.obj", "textures/chibi.png", [0.0, 0.0, 0.0],1 ),
    ("meshes/mercedes.obj", "textures/chibi.png", [3.0, -10.0, 0.0], 2),
    # Adicione mais objetos aqui:
    ("meshes/skull.obj", "textures/skull.jpg", [0.0, 25.0, -5.0], 0.3),
    ("meshes/sword.obj", "textures/sword.png", [0.0, 0.0, 0.0], 0.5),
    ("meshes/airplane.obj", "textures/airplane.jpg", [-8.0, 0.0, 0.0], 0.005),
    ("meshes/rose.obj", "textures/rose.jpg", [3.2, 3.5, 0.0], 0.01),
    ("meshes/Gun.obj", "textures/Gun.png", [-3.5, 4, 0.0], 2),
    ("meshes/wall.obj", "textures/brickwall_4.jpg", [0, 0, -50], 5),
    ("meshes/Rockwall.obj", "textures/rock.jpg", [0, -10, 0.0], 0.05),
]


   
def inicializa_objeto():
    """
    Carrega múltiplos objetos e suas texturas, criando VAO/VBO para cada um.
    """
    global vaos, vbos, num_vertices_list, texturas

    for obj_path, tex_path, pos, escala in modelos:
        buffer, num_vertices = ObjLoaderSimple.load_obj(obj_path)
        buffer = buffer.astype(np.float32)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)
        stride = buffer.itemsize * 5
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(buffer.itemsize * 3))

        textura = glGenTextures(1)
        load_texture(tex_path, textura)

        vaos.append(vao)
        vbos.append(vbo)
        num_vertices_list.append(num_vertices)
        texturas.append(textura)

    glBindVertexArray(0)


# ----------------------------------------
# Compilação dos shaders
# ----------------------------------------

def inicializa_shaders():
    """
    Cria, compila e linka vertex e fragment shader simplificados:
    - Vertex shader recebe:
        • layout(location = 0) in vec3 in_pos;    → atributo de posição do vértice (x,y,z)
        • layout(location = 1) in vec2 in_uv;     → atributo de coordenada de textura (u,v)
        • uniform mat4 model;                     → matriz de modelo (transformação local do objeto)
        • uniform mat4 view;                      → matriz de visualização (posição/orientação da câmera)
        • uniform mat4 projection;                → matriz de projeção (perspectiva)
      e repassa in_uv para o fragment shader em out vec2 frag_uv.

    - Fragment shader recebe:
        • in vec2 frag_uv;                        → UV interpolada do vertex shader
        • uniform sampler2D texture1;             → sampler que indica a textura vinculada ao texture unit 0
      e gera a cor final em out vec4 FragColor.

    Após definir as fontes, compilamos e linkamos:
    - compileShader(source, type): compila um shader de tipo GL_VERTEX_SHADER ou GL_FRAGMENT_SHADER.
    - compileProgram(vs, fs): linka os shaders compilados em um programa executável pelo glUseProgram.
    """
    
    global Shader_programm

    vertex_src = """#version 400
        layout(location = 0) in vec3 in_pos;    // posição do vértice
        layout(location = 1) in vec2 in_uv;     // coordenada de textura
        uniform mat4 model;                     // matriz de modelo
        uniform mat4 view;                      // matriz de visualização
        uniform mat4 projection;                // matriz de projeção
        out vec2 frag_uv;                       // repassa UV
        void main() {
            frag_uv = in_uv;
            gl_Position = projection * view * model * vec4(in_pos, 1.0);
        }"""

    fragment_src = """#version 400
        in vec2 frag_uv;                         // UV interpolada
        uniform sampler2D texture1;              // textura vinculada
        out vec4 FragColor;
        void main() {
            FragColor = texture(texture1, frag_uv);
        }"""

    # Compila shaders
    vs = OpenGL.GL.shaders.compileShader(vertex_src, GL_VERTEX_SHADER)
    fs = OpenGL.GL.shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER)
    Shader_programm = OpenGL.GL.shaders.compileProgram(vs, fs)

# ----------------------------------------
# Loop de renderização
# ----------------------------------------

def render_loop():
    """
    Loop principal que:
    - Processa movimento da câmera (WASD)
    - Limpa buffers
    - Atualiza matrizes uniformes
    - Renderiza objeto via glDrawArrays
    """

    # Inicializa a matriz de modelo como IDENTIDADE:
    # - A matriz identidade é o “elemento neutro” das transformações,
    #   ou seja, não altera posição, rotação ou escala do objeto.
    # - A partir dela, aplicamos translações, rotações ou escalas
    #   usando multiplcações ou substituições.
    # - Se fosse uma matriz de zeros, todas as coordenadas seriam zeradas
    #   e o objeto não apareceria na cena
    # Matriz de modelo fixa
    model = pyrr.matrix44.create_identity(dtype=np.float32)

    # Tempo da frame anterior
    last_time = glfw.get_time()
    # Velocidade da câmera em unidades do mundo por segundo
    base_speed = 10.0

    while not glfw.window_should_close(Window):
       
        # --- calcula deltaTime ---
        current_time = glfw.get_time()
        delta = current_time - last_time
        last_time = current_time

        # Movimento da câmera
        # --- movimenta a câmera usando deltaTime ---
        vel = base_speed * delta  # unidades por frame

        if glfw.get_key(Window, glfw.KEY_W) == glfw.PRESS:
            cam.process_keyboard("FORWARD", vel)
        if glfw.get_key(Window, glfw.KEY_S) == glfw.PRESS:
            cam.process_keyboard("BACKWARD", vel)
        if glfw.get_key(Window, glfw.KEY_A) == glfw.PRESS:
            cam.process_keyboard("LEFT", vel)
        if glfw.get_key(Window, glfw.KEY_D) == glfw.PRESS:
            cam.process_keyboard("RIGHT", vel)

        # Limpa a tela
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(Shader_programm)

        # Atualiza matrizes de view e projection
        view = cam.get_view_matrix()
        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45.0, WIDTH/HEIGHT, 0.1, 100.0
        )

        # Envia uniforms 
        #localização do uniform
        # 1, // quantidade de matrizes a enviar
        # GL_FALSE  // flag de “transpose” ou transposta
        #  model  // ponteiro/data da matriz
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model)  
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "projection"), 1, GL_FALSE, projection)


                # Desenha todos os objetos
        for i, (_, _, pos, escala) in enumerate(modelos):
            model = pyrr.matrix44.create_from_scale([escala, escala, escala], dtype=np.float32) @ \
            pyrr.matrix44.create_from_translation(pyrr.Vector3(pos), dtype=np.float32)
            glUniformMatrix4fv(glGetUniformLocation(Shader_programm, "model"), 1, GL_FALSE, model)
            glBindVertexArray(vaos[i])
            glBindTexture(GL_TEXTURE_2D, texturas[i])
            glDrawArrays(GL_TRIANGLES, 0, num_vertices_list[i])
        
        
        
        # 2) Segundo chibi deslocado para a direita em X
        #model2 = matrix44.create_from_translation(Vector3([ 2.0, 0.0, 0.0]))
        #glUniformMatrix4fv(loc_model, 1, GL_FALSE, model2)
        # VAO e textura já estão vinculados, basta desenhar de novo
        #glDrawArrays(GL_TRIANGLES, 0, num_vertices)

        # Troca buffers e coleta eventos
        glfw.swap_buffers(Window)
        glfw.poll_events()

    glfw.terminate()

# ----------------------------------------
# Função principal
# ----------------------------------------

def main():
    inicializa_opengl()
    inicializa_objeto()
    inicializa_shaders()
    render_loop()

if __name__ == "__main__":
    main()