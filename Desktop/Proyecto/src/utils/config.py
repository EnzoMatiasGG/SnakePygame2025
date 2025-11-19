"""
Configuración global del juego.
Contiene todas las constantes utilizadas en el proyecto.
"""
import pygame

# ============================================================================
# CONFIGURACIÓN DE PANTALLA
# ============================================================================
ANCHO = 800
ALTO = 600
FPS = 60
FPS_MENU = 30

# ============================================================================
# PALETA DE COLORES
# ============================================================================
NARANJA = (255, 165, 0)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Colores UI
COLOR_BARRA_VIDA = (0, 255, 0)
COLOR_BARRA_VIDA_FONDO = (60, 0, 0)
COLOR_BARRA_STAMINA = (0, 200, 255)
COLOR_BARRA_STAMINA_FONDO = (0, 40, 60)

# ============================================================================
# CONTROLES - JUGADOR 1
# ============================================================================
CONTROLES_JUGADOR1 = {
    "izquierda": pygame.K_a,
    "derecha": pygame.K_d,
    "arriba": pygame.K_w,
    "abajo": pygame.K_s,
    "golpe_ligero": pygame.K_j,
    "patada": pygame.K_k,
    "cubrirse": pygame.K_l,
    "bola": pygame.K_i,
    "kamehameha": pygame.K_o,
    "movimiento_final": pygame.K_p,
}

# ============================================================================
# CONTROLES - JUGADOR 2
# ============================================================================
CONTROLES_JUGADOR2 = {
    'izquierda': pygame.K_LEFT,
    'derecha': pygame.K_RIGHT,
    'arriba': pygame.K_UP,
    'abajo': pygame.K_DOWN,
    'golpe_ligero': pygame.K_KP1,
    'patada': pygame.K_KP2,
    'cubrirse': pygame.K_KP4,
    'bola': pygame.K_KP3,
    'movimiento_final': pygame.K_KP5,
}

# ============================================================================
# PARÁMETROS DE COMBATE
# ============================================================================
class CombatConfig:
    """Configuración del sistema de combate"""
    
    # Vida y Stamina
    VIDA_MAXIMA = 100
    STAMINA_MAXIMA = 100
    REGENERACION_STAMINA = 0.15
    
    # Costos de Stamina
    COSTO_GOLPE = 5
    COSTO_PATADA = 8
    COSTO_BOLA = 15
    COSTO_KAMEHAMEHA = 50
    COSTO_MOVIMIENTO_FINAL = 80
    
    # Daño de Ataques
    DANO_GOLPE = 5           # Puño (más débil)
    DANO_PATADA = 8          # Patada (medio-bajo)
    DANO_BOLA = 12           # Bola de energía "i" (medio-alto)
    DANO_KAMEHAMEHA = 1.5    # Kamehameha "o" (fuerte, por tick)
    DANO_MOVIMIENTO_FINAL = 25  # Movimiento final "p" (muy fuerte)
    
    # Sistema de Combos
    GOLPES_PARA_ATURDIR = 4
    TIEMPO_RESETEO_COMBO = 2000  # ms
    DURACION_ATURDIMIENTO = 1000  # ms
    MULTIPLICADOR_DANO_ATURDIDO = 2.0
    
    # Defensa
    REDUCCION_DANO_CUBIERTO = 0.3  # 70% de reducción

# ============================================================================
# PARÁMETROS DE TIEMPO
# ============================================================================
class TimeConfig:
    """Configuración de tiempos del juego"""
    
    # Combate
    TIEMPO_COMBATE = 60  # segundos
    
    # Animaciones
    DURACION_KO = 2000  # ms
    DURACION_VS = 4000  # ms
    DURACION_COUNTDOWN = 4500  # ms
    
    # Golpes
    TIEMPO_FRAME_GOLPE = 100  # ms
    TIEMPO_FRAME_PATADA = 100  # ms
    
    # Proyectiles
    TIEMPO_ANIMACION_BOLA = 150  # ms
    VELOCIDAD_PROYECTIL = 12  # pixeles por frame
    
    # Especiales
    DURACION_KAMEHAMEHA = 1000  # ms
    TIEMPO_FRAME_MOVIMIENTO_FINAL = 200  # ms

# ============================================================================
# ROUNDS
# ============================================================================
class RoundsConfig:
    """Configuración del sistema de rounds"""
    
    MAX_ROUNDS = 2  # Primero en ganar 2
    DURACION_CUENTA_REGRESIVA = 4500  # ms

# ============================================================================
# IA
# ============================================================================
class IAConfig:
    """Configuración de la inteligencia artificial"""
    
    # Dificultad FÁCIL
    FACIL = {
        'velocidad': 4,
        'tiempo_reaccion': 700,
        'prob_ataque': 0.75,
        'prob_defensa': 0.3,
        'prob_especial': 0.25,
        'distancia_ataque': 110,
        'distancia_minima': 45
    }
    
    # Dificultad NORMAL
    NORMAL = {
        'velocidad': 6,
        'tiempo_reaccion': 350,
        'prob_ataque': 0.9,
        'prob_defensa': 0.55,
        'prob_especial': 0.5,
        'distancia_ataque': 105,
        'distancia_minima': 40
    }
    
    # Dificultad DIFÍCIL
    DIFICIL = {
        'velocidad': 9,
        'tiempo_reaccion': 150,
        'prob_ataque': 0.98,
        'prob_defensa': 0.75,
        'prob_especial': 0.7,
        'distancia_ataque': 100,
        'distancia_minima': 35
    }

# ============================================================================
# RUTAS DE RECURSOS
# ============================================================================
class Paths:
    """Rutas de archivos de recursos"""
    
    # Directorios
    ASSETS = "Assets/"
    FONDOS = "Fondos/"
    FUENTES = "Fuentes/"
    SONIDOS = "Sonidos/"
    DATA = "data/"
    
    # Fuentes
    FUENTE_PRINCIPAL = "Fuentes/PressStart2P.ttf"
    
    # Imágenes especiales
    ICONO_VENTANA = "Assets/Imagenes_especiales/Icono_ventana.png"
    IMAGEN_VS = "Assets/Imagenes_especiales/vs.png"
    ICONO_Z = "Assets/Imagenes_especiales/Z-logo.png"
    DRAGON_RADAR = "Assets/Imagenes_especiales/Dragon_Radar.png"
    LOGO_INFO = "Assets/imagenes_especiales/Logo_info.png"
    MEME = "Assets/Imagenes_especiales/Meme.jpg"
    TORRE_IMAGEN = "Assets/Imagenes_especiales/MortalKombatTower.png"
    
    # Fondos
    FONDO_START = "Fondos/Fondo_start_2.png"
    FONDO_NUBES = "Fondos/Fondo_nubes.png"
    
    # Sonidos
    MUSICA_MENU = "Sonidos/Sonido_menu.wav"
    MUSICA_PELEA = "Sonidos/Sonido_pelea_1.wav"
    SONIDO_CURSOR = "Sonidos/Sonido_cursor.wav"
    
    # Datos
    RECORDS_1VS1 = "data/records.json"
    RECORDS_TORRE = "data/records_torre.json"

# ============================================================================
# CONFIGURACIÓN DE TORRE
# ============================================================================
class TowerConfig:
    """Configuración del modo Torre"""
    
    NUMERO_PELEAS = 3
    
    # Puntajes
    PUNTOS_POR_PELEA_GANADA = 2000
    PUNTOS_POR_GOLPE = 15
    PUNTOS_POR_DANO_CAUSADO = 8
    PENALIZACION_POR_DANO_RECIBIDO = 3
    BONUS_COMPLETAR_TORRE = 5000
    BONUS_TIEMPO_RAPIDO_180 = 1000  # < 3 minutos
    BONUS_TIEMPO_RAPIDO_300 = 500   # < 5 minutos

# ============================================================================
# CONFIGURACIÓN DE RÉCORDS
# ============================================================================
class RecordsConfig:
    """Configuración del sistema de récords"""
    
    # Puntajes 1vs1
    PUNTOS_POR_ROUND = 1000
    PUNTOS_POR_GOLPE_1VS1 = 10
    PUNTOS_POR_DANO_1VS1 = 5
    PENALIZACION_DANO_1VS1 = 2
    
    # Bonus por tiempo
    BONUS_TIEMPO_60 = 500   # < 1 minuto
    BONUS_TIEMPO_120 = 300  # < 2 minutos
    BONUS_TIEMPO_180 = 100  # < 3 minutos

# ============================================================================
# CONFIGURACIÓN DE SPRITES
# ============================================================================
class SpriteConfig:
    """Configuración de sprites"""
    
    ESCALA_DEFAULT = 2
    COLORKEY_BLANCO = (255, 255, 255)
    
    # Tamaños de iconos
    ICONO_Z_SIZE = (30, 30)
    ICONO_PERSONAJE_SELECCION = (120, 120)
    PREVIEW_MAPA = (160, 120)
    
    # Animación KO
    KO_TIEMPO_FRAME = 300  # ms