"""
HUD (Heads-Up Display) del juego.
Maneja las barras de vida, stamina y timer.
"""
import pygame
from typing import Tuple, Optional
from src.entities.player import Player
from src.utils.config import (
    ANCHO, ALTO, AMARILLO, BLANCO, NEGRO, NARANJA, ROJO,
    Paths, COLOR_BARRA_VIDA, COLOR_BARRA_VIDA_FONDO,
    COLOR_BARRA_STAMINA, COLOR_BARRA_STAMINA_FONDO
)
from src.utils.helpers import cargar_fuente


class HUDManager:
    """Gestor del HUD del juego"""
    
    def __init__(self, pantalla: pygame.Surface):
        """
        Inicializa el gestor de HUD.
        
        Args:
            pantalla: Surface de pygame
        """
        self.pantalla = pantalla
        
        # Fuentes
        try:
            self.fuente_press_start = cargar_fuente(Paths.FUENTE_PRINCIPAL, 12)
            self.fuente_press_start_mediana = cargar_fuente(Paths.FUENTE_PRINCIPAL, 16)
            self.fuente_press_start_grande = cargar_fuente(Paths.FUENTE_PRINCIPAL, 24)
            self.fuente_ui_pequena = pygame.font.SysFont(None, 18)
        except:
            self.fuente_press_start = pygame.font.SysFont(None, 18)
            self.fuente_press_start_mediana = pygame.font.SysFont(None, 24)
            self.fuente_press_start_grande = pygame.font.SysFont(None, 36)
            self.fuente_ui_pequena = pygame.font.SysFont(None, 18)
        
        # Cargar icono de Z
        try:
            self.icono_z = pygame.image.load(Paths.ICONO_Z).convert_alpha()
            self.icono_z = pygame.transform.scale(self.icono_z, (30, 30))
        except:
            self.icono_z = None
    
    def dibujar_barras_jugadores(self, jugador1: Player, jugador2: Player,
                                  rounds_j1: int, rounds_j2: int):
        """
        Dibuja las barras de vida y stamina de ambos jugadores.
        
        Args:
            jugador1: Jugador 1
            jugador2: Jugador 2
            rounds_j1: Rounds ganados por jugador 1
            rounds_j2: Rounds ganados por jugador 2
        """
        margen = 20
        ancho_timer = 100
        espacio_timer = 10
        ancho_barra = (ANCHO // 2) - margen - (ancho_timer // 2) - espacio_timer
        
        alto_barra_vida = 20
        alto_barra_stamina = 15
        espacio = 25
        
        # Jugador 1 (izquierda)
        self._dibujar_hud_jugador(
            jugador1, rounds_j1,
            margen, margen,
            ancho_barra, alto_barra_vida, alto_barra_stamina, espacio,
            "JUGADOR 1", alineacion="izquierda"
        )
        
        # Jugador 2 (derecha)
        x_j2 = ANCHO - margen - ancho_barra
        self._dibujar_hud_jugador(
            jugador2, rounds_j2,
            x_j2, margen,
            ancho_barra, alto_barra_vida, alto_barra_stamina, espacio,
            "JUGADOR 2", alineacion="derecha"
        )
    
    def _dibujar_hud_jugador(self, jugador: Player, rounds: int,
                             x: int, y: int,
                             ancho_barra: int, alto_vida: int, alto_stamina: int, espacio: int,
                             nombre: str, alineacion: str = "izquierda"):
        """Dibuja el HUD de un jugador"""
        # Nombre
        texto_nombre = self.fuente_press_start.render(nombre, True, AMARILLO)
        
        if alineacion == "izquierda":
            self.pantalla.blit(texto_nombre, (x, y))
        else:
            rect = texto_nombre.get_rect(topright=(ANCHO - 20, y))
            self.pantalla.blit(texto_nombre, rect)
        
        # Barra de vida
        y_vida = y + 25
        self._dibujar_barra(
            x, y_vida, ancho_barra, alto_vida,
            jugador.vida_actual, jugador.vida_maxima,
            COLOR_BARRA_VIDA_FONDO, COLOR_BARRA_VIDA
        )
        
        # Barra de stamina
        y_stamina = y_vida + espacio
        self._dibujar_barra(
            x, y_stamina, ancho_barra, alto_stamina,
            jugador.stamina_actual, jugador.stamina_maxima,
            COLOR_BARRA_STAMINA_FONDO, COLOR_BARRA_STAMINA
        )
        
        # Iconos de rounds ganados
        if self.icono_z:
            y_iconos = y_stamina + alto_stamina + 10
            
            for i in range(rounds):
                if alineacion == "izquierda":
                    x_icono = x + i * 35
                else:
                    x_icono = ANCHO - 20 - (i + 1) * 35
                
                self.pantalla.blit(self.icono_z, (x_icono, y_iconos))
    
    def _dibujar_barra(self, x: int, y: int, ancho: int, alto: int,
                       valor_actual: float, valor_maximo: float,
                       color_fondo: Tuple[int, int, int],
                       color_barra: Tuple[int, int, int]):
        """Dibuja una barra de progreso"""
        # Borde
        pygame.draw.rect(self.pantalla, BLANCO, (x - 2, y - 2, ancho + 4, alto + 4), 2)
        
        # Fondo
        pygame.draw.rect(self.pantalla, color_fondo, (x, y, ancho, alto))
        
        # Barra de progreso
        porcentaje = max(0, valor_actual / valor_maximo)
        ancho_relleno = int(ancho * porcentaje)
        pygame.draw.rect(self.pantalla, color_barra, (x, y, ancho_relleno, alto))
        
        # Texto (opcional)
        if alto >= 18:
            texto = self.fuente_ui_pequena.render(
                f"{int(valor_actual)}/{valor_maximo}",
                True, BLANCO
            )
            texto_x = x + (ancho - texto.get_width()) // 2
            texto_y = y + (alto - texto.get_height()) // 2
            self.pantalla.blit(texto, (texto_x, texto_y))
    
    def dibujar_timer(self, tiempo_restante: int, en_introduccion: bool = False):
        """
        Dibuja el timer del combate.
        
        Args:
            tiempo_restante: Tiempo restante en segundos
            en_introduccion: Si está en la introducción
        """
        ancho_timer = 100
        alto_timer = 50
        x_centro = ANCHO // 2
        y_centro = 35
        
        rect_fondo = pygame.Rect(
            x_centro - ancho_timer // 2,
            y_centro - alto_timer // 2,
            ancho_timer, alto_timer
        )
        
        pygame.draw.rect(self.pantalla, (20, 20, 40), rect_fondo)
        
        if not en_introduccion:
            # Color según tiempo
            if tiempo_restante <= 10:
                color_borde = ROJO
                color_numero = ROJO
                grosor = 4
            elif tiempo_restante <= 30:
                color_borde = NARANJA
                color_numero = NARANJA
                grosor = 3
            else:
                color_borde = AMARILLO
                color_numero = AMARILLO
                grosor = 3
            
            pygame.draw.rect(self.pantalla, color_borde, rect_fondo, grosor)
            
            # Número
            texto = self.fuente_press_start_grande.render(str(tiempo_restante), True, color_numero)
            sombra = self.fuente_press_start_grande.render(str(tiempo_restante), True, NEGRO)
            
            rect_sombra = sombra.get_rect(center=(x_centro + 2, y_centro + 2))
            rect_texto = texto.get_rect(center=(x_centro, y_centro))
            
            self.pantalla.blit(sombra, rect_sombra)
            self.pantalla.blit(texto, rect_texto)
            
            # "TIME"
            texto_time = self.fuente_press_start.render("TIME", True, AMARILLO)
            rect_time = texto_time.get_rect(center=(x_centro, y_centro + alto_timer // 2 + 12))
            self.pantalla.blit(texto_time, rect_time)
        else:
            # Durante introducción
            pygame.draw.rect(self.pantalla, NARANJA, rect_fondo, 3)
            texto_ko = self.fuente_press_start_grande.render("KO", True, NARANJA)
            rect_ko = texto_ko.get_rect(center=(x_centro, y_centro))
            self.pantalla.blit(texto_ko, rect_ko)