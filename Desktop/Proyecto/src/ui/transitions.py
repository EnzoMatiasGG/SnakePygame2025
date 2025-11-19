"""
Transiciones y pantallas intermedias.
Maneja pantallas VS, KO, cuenta regresiva, etc.
"""
import pygame
from typing import Optional
from src.entities.player import Player
from src.utils.config import ANCHO, ALTO, AMARILLO, NEGRO, ROJO, Paths
from src.utils.helpers import dibujar_texto_con_sombra


class TransitionManager:
    """Gestor de transiciones del juego"""
    
    def __init__(self, pantalla: pygame.Surface):
        """
        Inicializa el gestor de transiciones.
        
        Args:
            pantalla: Surface de pygame
        """
        self.pantalla = pantalla
        
        # Cargar imagen VS
        try:
            self.imagen_vs = pygame.image.load(Paths.IMAGEN_VS).convert_alpha()
            ancho_vs = 300
            alto_vs = int(self.imagen_vs.get_height() * (ancho_vs / self.imagen_vs.get_width()))
            self.imagen_vs = pygame.transform.scale(self.imagen_vs, (ancho_vs, alto_vs))
        except:
            self.imagen_vs = None
        
        # Fuente
        try:
            self.fuente_grande = pygame.font.Font(Paths.FUENTE_PRINCIPAL, 100)
        except:
            self.fuente_grande = pygame.font.SysFont(None, 100)
    
    def mostrar_vs(self, fondo: Optional[pygame.Surface],
                   jugador1: Player, jugador2: Player,
                   tiempo_inicio: int) -> bool:
        """
        Muestra la pantalla VS.
        
        Args:
            fondo: Fondo del juego
            jugador1: Jugador 1
            jugador2: Jugador 2
            tiempo_inicio: Tiempo de inicio
            
        Returns:
            bool: True si debe continuar a cuenta regresiva
        """
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000
        
        if fondo:
            self.pantalla.blit(fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        jugador1.dibujar(self.pantalla)
        jugador2.dibujar(self.pantalla)
        
        if self.imagen_vs:
            vs_rect = self.imagen_vs.get_rect(center=(ANCHO // 2, ALTO // 2))
            self.pantalla.blit(self.imagen_vs, vs_rect)
        else:
            dibujar_texto_con_sombra(
                self.pantalla, self.fuente_grande, "VS",
                ROJO, NEGRO, ANCHO // 2, ALTO // 2
            )
        
        pygame.display.flip()
        
        return tiempo_transcurrido >= 4.0
    
    def mostrar_cuenta_regresiva(self, fondo: Optional[pygame.Surface],
                                  jugador1: Player, jugador2: Player,
                                  tiempo_inicio: int) -> Optional[bool]:
        """
        Muestra la cuenta regresiva.
        
        Returns:
            Optional[bool]: True si terminó, None si continúa
        """
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000
        
        if fondo:
            self.pantalla.blit(fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        jugador1.dibujar(self.pantalla)
        jugador2.dibujar(self.pantalla)
        
        tiempo_countdown = int(4 - tiempo_transcurrido)
        
        if tiempo_countdown > 0:
            texto = str(tiempo_countdown)
            color = AMARILLO
        elif tiempo_transcurrido < 4.5:
            texto = "FIGHT!"
            color = ROJO
        else:
            return True
        
        dibujar_texto_con_sombra(
            self.pantalla, self.fuente_grande, texto,
            color, NEGRO, ANCHO // 2, ALTO // 2
        )
        
        pygame.display.flip()
        return None