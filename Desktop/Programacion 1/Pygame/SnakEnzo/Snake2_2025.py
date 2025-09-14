import pygame # Importa la libreria Pygame para crear juegos
import sys # Importa sys para poder cerrar el programa correctamente
import random   # Importa random para generar numero aleatorios

pygame.init() # Inicia todos los modulos de python necesarios para que se puedan usar
pygame.mixer.init()

# Configuracion ventana
ANCHO, ALTO = 800, 800
TAM_CELDA = 20  # Definido antes de usar la imagen
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake en Python")

# Sonidos
sonido_comer = pygame.mixer.Sound("./assets/sonido_comida.mp3")
sonido_final = pygame.mixer.Sound("./assets/sonido_final.wav")
sonido_nav = pygame.mixer.Sound("./assets/sonido_clic.wav")

# Fuente
fuente = pygame.font.Font("./assets/nokiafc22.ttf", 30)

# Fondos e imagenes
fondo_inicio = pygame.image.load("./assets/snake_nokia.jpg")   # Pantalla inicial
fondo_inicio = pygame.transform.scale(fondo_inicio, (ANCHO, ALTO))

fondo_menu = pygame.image.load("./assets/imagen_menu.jpg")     # Menu de modos
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))

fondo_final = pygame.image.load("./assets/Imagen_final.gif")   # Fondo final
fondo_final = pygame.transform.scale(fondo_final, (ANCHO, ALTO))

comida_snake = pygame.image.load("./assets/Comida_snake.png")
comida_snake = pygame.transform.scale(comida_snake, (TAM_CELDA, TAM_CELDA))

cabeza_normal = pygame.image.load("./assets/cabeza_normal.png")
cabeza_normal = pygame.transform.scale(cabeza_normal, (TAM_CELDA, TAM_CELDA))

cabeza_comiendo = pygame.image.load("./assets/cabeza_comiendo.png")
cabeza_comiendo = pygame.transform.scale(cabeza_comiendo, (TAM_CELDA, TAM_CELDA))

cuerpo_snake= pygame.image.load("./assets/cuerpo_snake.png")
cuerpo_snake= pygame.transform.scale(cuerpo_snake, (TAM_CELDA, TAM_CELDA))



fps = 10

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
VERDE_SNAKE = (156, 200, 0)

# Bordes y margenes
GROSOR_BORDE = 8
MARGEN = 20
MARGEN_SUP = 70

# Estados
ESTADO_INICIO = "inicio"
ESTADO_MENU = "menu"
ESTADO_JUEGO = "juego"
ESTADO_FIN = "fin"

estado = ESTADO_INICIO

# Snake
snake = [(100, 100), (90, 100), (80, 100)]
direccion = (TAM_CELDA, 0)
comida = (200, 200)
puntos = 0
modo = "NORMAL"

# Estados de la cabeza
comiendo = False
comiendo_contador = 0
TIEMPO_COMIENDO = 4  # Cantidad de frames para mostrar la cabeza comiendo

# Variables para los menus
NUM_OPCIONES = 4
opcion_seleccionada = 0  # Menu principal
num_opciones_fin = 2
op_seleccionada_fin = 0  # Menu fin

def dibujar_menu():
    ventana.blit(fondo_menu, (0, 0))
    textos = ["JUGAR", "MODO FACIL", "MODO NORMAL", "MODO IMPOSIBLE"]
    for i in range(NUM_OPCIONES):
        if i == opcion_seleccionada:
            color_texto = VERDE_SNAKE
            color_fondo = NEGRO
        else:
            color_texto = NEGRO
            color_fondo = VERDE_SNAKE
        texto = fuente.render(textos[i], True, color_texto)

        # Calcular posicion
        x = ANCHO // 2 - texto.get_width() // 2
        y = 550 + i * 60   # Separacion entre botones

        # Dibujar rectangulo de fondo
        rect = pygame.Rect(x - 20, y - 10, texto.get_width() + 30, texto.get_height() + 10)
        pygame.draw.rect(ventana, color_fondo, rect, border_radius=15)  # esquinas redondeadas

        # Poner texto encima del fondo
        ventana.blit(texto, (x, y))

# Rotacion de la cabeza
def rotar_cabeza (imagen, direccion):
    if direccion == (TAM_CELDA, 0): # Derecha
        return imagen
    elif direccion == (-TAM_CELDA, 0): # Izquierda
        return pygame.transform.flip(imagen,True, False) # Voltea horizontalmente
    elif direccion == (0, TAM_CELDA):  # Abajo
        return pygame.transform.rotate(imagen, 270)
    elif direccion == (0, -TAM_CELDA):  # Arriba
        return pygame.transform.rotate(imagen, 90)

# ¿Que pasa cuando perdemos?
def game_over(): 
    ventana.blit(fondo_final, (0, 0))  # Dibuja el fondo primero

    mensaje_fin = fuente.render("GAME OVER", True, ROJO)
    x_mensaje = ANCHO // 2 - mensaje_fin.get_width() // 2
    y_mensaje = ALTO // 3.50
    ventana.blit(mensaje_fin, (x_mensaje, y_mensaje))

    puntaje_fin = fuente.render(f"Puntaje final: {puntos}", True, BLANCO)
    x_puntaje = ANCHO // 2 - puntaje_fin.get_width() // 2
    y_puntaje = y_mensaje + mensaje_fin.get_height() + 30
    ventana.blit(puntaje_fin, (x_puntaje, y_puntaje))

    textos = ["REINICIAR", "VOLVER AL MENU PRINCIPAL"]
    for i in range(num_opciones_fin):
        if i == op_seleccionada_fin:
            color_texto = VERDE_SNAKE
            color_fondo = NEGRO
        else:
            color_texto = NEGRO
            color_fondo = VERDE_SNAKE
        texto = fuente.render(textos[i], True, color_texto)

        x = ANCHO // 2 - texto.get_width() // 2
        y = 550 + i * 60

        rect = pygame.Rect(x - 20, y - 10, texto.get_width() + 30, texto.get_height() + 10)
        pygame.draw.rect(ventana, color_fondo, rect, border_radius=15)

        ventana.blit(texto, (x, y))

# Inicia el juego, config snake (marca pos. inical), comida(limites por los bordes)
def jugar():
    global estado, snake, direccion, comida, puntos
    estado = ESTADO_JUEGO # Cambia el estado del juego
    snake[:] = [(100, 100), (90, 100), (80, 100)] # Pos.inicial
    direccion = (TAM_CELDA, 0) # Empieza para la derecha

    # Limites de donde aparece la comida 
    min_x = MARGEN // TAM_CELDA
    max_x = (ANCHO - MARGEN) // TAM_CELDA - 1
    min_y = MARGEN_SUP // TAM_CELDA
    max_y = (ALTO - MARGEN) // TAM_CELDA - 1

    # comida de forma aleatoria
    comida = (random.randint(min_x, max_x) * TAM_CELDA, random.randint(min_y, max_y) * TAM_CELDA)
    puntos = 0

def modo_facil():
    global modo, fps
    modo = "FACIL"
    fps = 5
    jugar()

def modo_normal():
    global modo, fps
    modo = "NORMAL"
    fps = 20
    jugar()

def modo_imposible():
    global modo, fps
    modo = "IMPOSIBLE"
    fps = 50
    jugar()

def reiniciar():
    global estado
    estado = ESTADO_MENU

clock = pygame.time.Clock()

# Bucle
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Movimiento en el menu principal
        if estado == ESTADO_MENU:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % NUM_OPCIONES # Baja y vuelve al inicio si se pasa el final
                    sonido_nav.play() # Reproduce el sonido de navegacion
                elif evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % NUM_OPCIONES # sube y vuelve al final si se psa el principio
                    sonido_nav.play() # Reproduce el sonido de navegacion
                elif evento.key == pygame.K_RETURN: #Ejecuta lo seleccionado
                    sonido_nav.play() # Reproduce el sonido de navegacion
                    if opcion_seleccionada == 0:
                        jugar()
                    elif opcion_seleccionada == 1:
                        modo_facil()
                    elif opcion_seleccionada == 2:
                        modo_normal()
                    elif opcion_seleccionada == 3:
                        modo_imposible()

        # Movimiento en el menu de fin
        elif estado == ESTADO_FIN:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    op_seleccionada_fin = (op_seleccionada_fin + 1) % num_opciones_fin
                    sonido_nav.play() # Reproduce el sonido de navegacion
                elif evento.key == pygame.K_UP:
                    op_seleccionada_fin = (op_seleccionada_fin - 1) % num_opciones_fin
                    sonido_nav.play() # Reproduce el sonido de navegacion
                elif evento.key == pygame.K_RETURN:
                    sonido_nav.play() # Reproduce el sonido de navegacion
                    if op_seleccionada_fin == 0:  
                        jugar()  # reinicia el juego
                    elif op_seleccionada_fin == 1:  #vOLVER AL MENU PRINCIPAL
                        estado = ESTADO_MENU

    #Segun estado
    if estado == ESTADO_INICIO:
        ventana.blit(fondo_inicio, (0, 0)) 
        texto_jugar = fuente.render("Presiona ENTER para jugar", True, NEGRO)
        ventana.blit(texto_jugar, (ANCHO // 2 - texto_jugar.get_width() // 2, ALTO - texto_jugar.get_height() - 30))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sonido_nav.play() # Reproduce el sonido de navegacion
            estado = ESTADO_MENU

    elif estado == ESTADO_MENU:
        dibujar_menu()

    elif estado == ESTADO_JUEGO:
        min_x = MARGEN // TAM_CELDA
        max_x = (ANCHO - MARGEN) // TAM_CELDA - 1
        min_y = MARGEN_SUP // TAM_CELDA
        max_y = (ALTO - MARGEN) // TAM_CELDA - 1

        keys = pygame.key.get_pressed() # Estado actual de todas las teclas
        # Cambiar la direccion segun la tecla presionada sin que la serpiente se mueva en sentido contrario
        if keys[pygame.K_UP] and direccion != (0, TAM_CELDA):
            direccion = (0, -TAM_CELDA) # Arriba
        if keys[pygame.K_DOWN] and direccion != (0, -TAM_CELDA):
            direccion = (0, TAM_CELDA) # Abajo
        if keys[pygame.K_LEFT] and direccion != (TAM_CELDA, 0):
            direccion = (-TAM_CELDA, 0) # Izquierda
        if keys[pygame.K_RIGHT] and direccion != (-TAM_CELDA, 0):
            direccion = (TAM_CELDA, 0) # Derecha

        # Calcula la nueva posicion de la cabeza sumando la direccion actual
        cabeza = (snake[0][0] + direccion[0], snake[0][1] + direccion[1])
        snake.insert(0, cabeza) 

        if cabeza == comida: # Si la cabeza llego donde esta la comida:
            puntos += 1 #suma un punto
            sonido_comer.play() # Reproduce el sonido
            comida = (random.randint(min_x, max_x) * TAM_CELDA, random.randint(min_y, max_y) * TAM_CELDA) # Pone comida en otro lugar random
            comiendo = True # Cambia el estado para mostrar la cabeza comiendo
            comiendo_contador = TIEMPO_COMIENDO # Tiempo que dura la imagen de la cabeza comiendo
        else:
            snake.pop() # Si no comio elimina la ultima parte, asi no crece infinito

        # Si la cabeza toca un borde o choca contra si misma, se termina el juego
        if (cabeza[0] < MARGEN or cabeza[0] >= ANCHO - MARGEN or cabeza[1] < MARGEN_SUP or cabeza[1] >= ALTO - MARGEN or cabeza in snake[1:]):
            sonido_final.play() # Reproduce el sonido
            estado = ESTADO_FIN # Cambia el estado para mostrar la pantalla de game over
            op_seleccionada_fin = 0 

        ventana.fill(VERDE_SNAKE) 
        # Dibuja los bordes
        pygame.draw.rect(ventana, NEGRO, (MARGEN, MARGEN_SUP, ANCHO - 2 * MARGEN, ALTO - MARGEN_SUP - MARGEN), GROSOR_BORDE)
        # Dibuja una linea abajo de la puntuacion
        pygame.draw.line(ventana, NEGRO, (MARGEN, MARGEN_SUP - 10), (ANCHO - MARGEN, MARGEN_SUP - 10), 3)

        ventana.blit(comida_snake, comida) # Dibuja la comida en su pos.actual

        for i, segmento in enumerate(snake): # Por cada segmento de la serpiente (cabeza a cola)
            if i == 0:
                # Si es la cabeza, elige la imagen segun si esta comiendo o no
                imagen_cabeza = cabeza_comiendo if comiendo else cabeza_normal 
                # Rota la imagen de la cabeza segun la direccion actual
                imagen_rotada = rotar_cabeza(imagen_cabeza, direccion) 
                # Dibuja la cabeza en la pos.correcta
                ventana.blit(imagen_rotada, segmento)
            else: # Permite saber en qué direccion se mueve cada segmento para despues rotar la imagen del cuerpo correctamente segun el valor de dx y dy.
                dx = snake[i-1][0] - segmento[0] # Toma el valor de x del segmento anterior y le resta el valor de x actual
                dy = snake[i-1][1] - segmento[1]
                if dx > 0: # Segun la diferencia , defina le rotacion adecuada
                    angulo = 0        #derecha
                elif dx < 0:
                    angulo = 180      #izquierda
                elif dy > 0:
                    angulo = 270      #abajo
                elif dy < 0:
                    angulo = 90       #arriba

                # Rota la imagen del cuerpo segun el angulo calculado
                imagen_cuerpo_rotada = pygame.transform.rotate(cuerpo_snake, angulo)
                # Dibuja el segmento del cuerpo en su pos
                ventana.blit(imagen_cuerpo_rotada, segmento) 

        # Si la serpiente esta en estado comiendo, reduce el contador para saber cuando volver a estado normal
        if comiendo:
            comiendo_contador -= 1
            # Cuando el contador llega a 0 deja de estar en estado "comiendo"
            if comiendo_contador <= 0: 
                comiendo = False

        # Dibuja marcador
        marcador = fuente.render(f"Puntos: {puntos}", True, NEGRO)
        ventana.blit(marcador, (10, 10))

    elif estado == ESTADO_FIN:
        game_over()

    pygame.display.flip() # Actualiza la pantalla con los dibujos realizados en este ciclo
    clock.tick(fps) #  Cuadros por segundo, para que corra a la velocidad deseada
