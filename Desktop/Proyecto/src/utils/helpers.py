"""
Funciones auxiliares y utilidades compartidas.
"""
import pygame
from typing import Tuple, Optional

def cargar_imagen_con_colorkey(ruta: str, escala: int = 2, 
                                 colorkey: Tuple[int, int, int] = (255, 255, 255)) -> pygame.Surface:
    """
    Carga una imagen con transparencia basada en colorkey.
    
    Args:
        ruta: Ruta del archivo de imagen
        escala: Factor de escala (2 = doble tamaño)
        colorkey: Color a hacer transparente (RGB)
    
    Returns:
        pygame.Surface: Imagen cargada y escalada
    """
    try:
        imagen = pygame.image.load(ruta).convert()
        imagen.set_colorkey(colorkey)
        ancho, alto = imagen.get_size()
        imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
        return imagen
    except pygame.error as e:
        print(f"Error cargando imagen {ruta}: {e}")
        # Retornar superficie vacía como fallback
        return pygame.Surface((64 * escala, 64 * escala))


def cargar_imagen_con_alpha(ruta: str, escala: int = 2) -> pygame.Surface:
    """
    Carga una imagen PNG con canal alpha real.
    
    Args:
        ruta: Ruta del archivo de imagen
        escala: Factor de escala
    
    Returns:
        pygame.Surface: Imagen cargada con transparencia
    """
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        ancho, alto = imagen.get_size()
        imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
        return imagen
    except pygame.error as e:
        print(f"Error cargando imagen {ruta}: {e}")
        return pygame.Surface((64 * escala, 64 * escala), pygame.SRCALPHA)


def cargar_fuente(ruta: str, tamano: int) -> pygame.font.Font:
    """
    Carga una fuente personalizada con fallback a fuente del sistema.
    
    Args:
        ruta: Ruta del archivo de fuente
        tamano: Tamaño de la fuente
    
    Returns:
        pygame.font.Font: Objeto fuente
    """
    try:
        return pygame.font.Font(ruta, tamano)
    except:
        print(f"No se pudo cargar la fuente {ruta}, usando fuente del sistema")
        return pygame.font.SysFont(None, tamano)


def centrar_texto(texto_surface: pygame.Surface, 
                  centro_x: int, centro_y: int) -> Tuple[int, int]:
    """
    Calcula la posición para centrar un texto.
    
    Args:
        texto_surface: Surface del texto renderizado
        centro_x: Coordenada X del centro
        centro_y: Coordenada Y del centro
    
    Returns:
        Tuple[int, int]: Posición (x, y) para blit
    """
    rect = texto_surface.get_rect(center=(centro_x, centro_y))
    return rect.topleft


def dibujar_texto_con_sombra(pantalla: pygame.Surface, 
                              fuente: pygame.font.Font,
                              texto: str,
                              color_texto: Tuple[int, int, int],
                              color_sombra: Tuple[int, int, int],
                              centro_x: int, centro_y: int,
                              offset_sombra: int = 3):
    """
    Dibuja texto con efecto de sombra.
    
    Args:
        pantalla: Surface donde dibujar
        fuente: Fuente a usar
        texto: Texto a renderizar
        color_texto: Color del texto principal
        color_sombra: Color de la sombra
        centro_x: Centro X
        centro_y: Centro Y
        offset_sombra: Desplazamiento de la sombra
    """
    # Sombra
    sombra = fuente.render(texto, True, color_sombra)
    rect_sombra = sombra.get_rect(center=(centro_x + offset_sombra, centro_y + offset_sombra))
    pantalla.blit(sombra, rect_sombra)
    
    # Texto principal
    texto_render = fuente.render(texto, True, color_texto)
    rect_texto = texto_render.get_rect(center=(centro_x, centro_y))
    pantalla.blit(texto_render, rect_texto)


def crear_overlay(ancho: int, alto: int, 
                  color: Tuple[int, int, int] = (0, 0, 0),
                  alpha: int = 128) -> pygame.Surface:
    """
    Crea una superficie semi-transparente para overlay.
    
    Args:
        ancho: Ancho del overlay
        alto: Alto del overlay
        color: Color RGB del overlay
        alpha: Transparencia (0-255)
    
    Returns:
        pygame.Surface: Overlay semi-transparente
    """
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((*color, alpha))
    return overlay


def limitar_valor(valor: float, minimo: float, maximo: float) -> float:
    """
    Limita un valor entre un mínimo y máximo.
    
    Args:
        valor: Valor a limitar
        minimo: Valor mínimo
        maximo: Valor máximo
    
    Returns:
        float: Valor limitado
    """
    return max(minimo, min(valor, maximo))


def calcular_distancia(x1: float, y1: float, 
                       x2: float, y2: float) -> Tuple[float, float]:
    """
    Calcula la distancia entre dos puntos en X e Y.
    
    Args:
        x1, y1: Coordenadas del primer punto
        x2, y2: Coordenadas del segundo punto
    
    Returns:
        Tuple[float, float]: Distancia en X y distancia en Y
    """
    return abs(x2 - x1), abs(y2 - y1)


def formatear_tiempo(segundos: int) -> str:
    """
    Formatea segundos a formato MM:SS.
    
    Args:
        segundos: Tiempo en segundos
    
    Returns:
        str: Tiempo formateado (ej: "02:45")
    """
    minutos = segundos // 60
    segs = segundos % 60
    return f"{minutos}:{segs:02d}"


def interpolacion_lineal(inicio: float, fin: float, t: float) -> float:
    """
    Interpolación lineal entre dos valores.
    
    Args:
        inicio: Valor inicial
        fin: Valor final
        t: Factor de interpolación (0.0 a 1.0)
    
    Returns:
        float: Valor interpolado
    """
    return inicio + (fin - inicio) * t


def crear_rectangulo_con_borde(pantalla: pygame.Surface,
                                x: int, y: int,
                                ancho: int, alto: int,
                                color_relleno: Tuple[int, int, int],
                                color_borde: Tuple[int, int, int],
                                grosor_borde: int = 2):
    """
    Dibuja un rectángulo con relleno y borde.
    
    Args:
        pantalla: Surface donde dibujar
        x, y: Posición
        ancho, alto: Dimensiones
        color_relleno: Color del relleno
        color_borde: Color del borde
        grosor_borde: Grosor del borde
    """
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, color_relleno, rect)
    pygame.draw.rect(pantalla, color_borde, rect, grosor_borde)


def parpadeo(tiempo_actual: int, intervalo: int = 500) -> bool:
    """
    Genera un efecto de parpadeo basado en el tiempo.
    
    Args:
        tiempo_actual: Tiempo actual en ms
        intervalo: Intervalo de parpadeo en ms
    
    Returns:
        bool: True si debe mostrarse, False si no
    """
    return (tiempo_actual // intervalo) % 2 == 0


def escalar_mantener_aspecto(imagen: pygame.Surface,
                              ancho_objetivo: int,
                              alto_objetivo: int) -> pygame.Surface:
    """
    Escala una imagen manteniendo su relación de aspecto.
    
    Args:
        imagen: Imagen a escalar
        ancho_objetivo: Ancho máximo
        alto_objetivo: Alto máximo
    
    Returns:
        pygame.Surface: Imagen escalada
    """
    ancho_original, alto_original = imagen.get_size()
    ratio = min(ancho_objetivo / ancho_original, alto_objetivo / alto_original)
    
    nuevo_ancho = int(ancho_original * ratio)
    nuevo_alto = int(alto_original * ratio)
    
    return pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))


def validar_entrada_alfabetica(caracter: str) -> bool:
    """
    Valida que un carácter sea alfabético.
    
    Args:
        caracter: Carácter a validar
    
    Returns:
        bool: True si es alfabético
    """
    return caracter.isalpha() and len(caracter) == 1