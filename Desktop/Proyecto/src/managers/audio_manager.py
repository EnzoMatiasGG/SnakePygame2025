"""
Gestor de audio del juego.
Centraliza la gestión de música y efectos de sonido.
"""
import pygame
from typing import Optional
from src.utils.config import Paths


class AudioManager:
    """Gestor centralizado de audio"""
    
    def __init__(self, volumen_inicial: float = 0.1):
        """
        Inicializa el gestor de audio.
        
        Args:
            volumen_inicial: Volumen inicial (0.0 a 1.0)
        """
        self.volumen = volumen_inicial
        self.musica_actual: Optional[str] = None
        self.sonidos: dict = {}
        
        # Cargar efectos de sonido
        self._cargar_sonidos()
    
    def _cargar_sonidos(self):
        """Carga los efectos de sonido"""
        try:
            self.sonidos['cursor'] = pygame.mixer.Sound(Paths.SONIDO_CURSOR)
        except:
            print("No se pudo cargar el sonido del cursor")
            self.sonidos['cursor'] = None
    
    def reproducir_musica_menu(self):
        """Reproduce la música del menú"""
        self._cambiar_musica(Paths.MUSICA_MENU)
    
    def reproducir_musica_pelea(self):
        """Reproduce la música de pelea"""
        self._cambiar_musica(Paths.MUSICA_PELEA)
    
    def _cambiar_musica(self, ruta: str):
        """
        Cambia la música actual.
        
        Args:
            ruta: Ruta del archivo de música
        """
        if self.musica_actual == ruta:
            return
        
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(self.volumen)
            pygame.mixer.music.play(-1)  # Loop infinito
            self.musica_actual = ruta
        except Exception as e:
            print(f"No se pudo cargar la música {ruta}: {e}")
    
    def detener_musica(self):
        """Detiene la música actual"""
        pygame.mixer.music.stop()
        self.musica_actual = None
    
    def reproducir_sonido(self, nombre: str):
        """
        Reproduce un efecto de sonido.
        
        Args:
            nombre: Nombre del sonido ('cursor', etc.)
        """
        if nombre in self.sonidos and self.sonidos[nombre]:
            self.sonidos[nombre].play()
    
    def ajustar_volumen(self, delta: float):
        """
        Ajusta el volumen de la música.
        
        Args:
            delta: Cambio en el volumen (puede ser negativo)
        """
        self.volumen = max(0.0, min(1.0, self.volumen + delta))
        pygame.mixer.music.set_volume(self.volumen)
    
    def subir_volumen(self):
        """Sube el volumen un 10%"""
        self.ajustar_volumen(0.1)
    
    def bajar_volumen(self):
        """Baja el volumen un 10%"""
        self.ajustar_volumen(-0.1)
    
    def obtener_volumen(self) -> float:
        """
        Obtiene el volumen actual.
        
        Returns:
            float: Volumen actual (0.0 a 1.0)
        """
        return self.volumen