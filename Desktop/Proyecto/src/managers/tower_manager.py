"""
Gestor del modo Torre.
Maneja la lógica del modo torre (3 peleas consecutivas).
"""
import pygame
import sys
from typing import List, Dict, Optional
from src.utils.config import (
    ANCHO, ALTO, AMARILLO, BLANCO, NEGRO, NARANJA, ROJO,
    Paths, TowerConfig
)
from src.utils.helpers import cargar_fuente


class TowerManager:
    """Gestor del modo Torre"""
    
    def __init__(self, pantalla: pygame.Surface, reloj: pygame.time.Clock,
                 personajes_data: List[Dict]):
        """
        Inicializa el gestor de torre.
        
        Args:
            pantalla: Surface de pygame
            reloj: Clock de pygame
            personajes_data: Lista con datos de personajes
        """
        self.pantalla = pantalla
        self.reloj = reloj
        self.personajes_data = personajes_data
        
        # Cargar imagen de la torre
        try:
            self.imagen_torre = pygame.image.load(Paths.TORRE_IMAGEN).convert_alpha()
            self.imagen_torre = pygame.transform.scale(self.imagen_torre, (200, 550))
        except:
            self.imagen_torre = None
        
        # Fuentes
        self.fuente_grande = cargar_fuente(Paths.FUENTE_PRINCIPAL, 24)
        self.fuente_media = cargar_fuente(Paths.FUENTE_PRINCIPAL, 16)
        self.fuente_pequena = cargar_fuente(Paths.FUENTE_PRINCIPAL, 12)
        
        # Estado de la torre
        self.personaje_jugador: Optional[str] = None
        self.oponentes: List[str] = []
        self.pelea_actual = 0
        
        # Estadísticas acumuladas
        self.stats_totales = {
            'golpes_totales': 0,
            'dano_causado': 0,
            'dano_recibido': 0,
            'tiempo_total': 0
        }
    
    def iniciar_torre(self, personaje_jugador: str):
        """
        Inicia una nueva torre.
        
        Args:
            personaje_jugador: ID del personaje seleccionado
        """
        self.personaje_jugador = personaje_jugador
        self.pelea_actual = 0
        
        # Obtener oponentes (todos excepto el jugador)
        oponentes_disponibles = [
            p['id'] for p in self.personajes_data
            if p['id'] != personaje_jugador
        ]
        
        self.oponentes = oponentes_disponibles
        
        # Reiniciar estadísticas
        self.stats_totales = {
            'golpes_totales': 0,
            'dano_causado': 0,
            'dano_recibido': 0,
            'tiempo_total': 0
        }
    
    def obtener_oponente_actual(self) -> Optional[str]:
        """
        Obtiene el oponente de la pelea actual.
        
        Returns:
            Optional[str]: ID del oponente o None
        """
        if self.pelea_actual < len(self.oponentes):
            return self.oponentes[self.pelea_actual]
        return None
    
    def avanzar_pelea(self):
        """Avanza a la siguiente pelea"""
        self.pelea_actual += 1
    
    def esta_completada(self) -> bool:
        """
        Verifica si se completó la torre.
        
        Returns:
            bool: True si se completó
        """
        return self.pelea_actual >= len(self.oponentes)
    
    def agregar_stats_pelea(self, stats_jugador: Dict, tiempo: int):
        """
        Acumula las estadísticas de una pelea.
        
        Args:
            stats_jugador: Estadísticas del jugador
            tiempo: Tiempo de la pelea en segundos
        """
        self.stats_totales['golpes_totales'] += stats_jugador['golpes_totales']
        self.stats_totales['dano_causado'] += stats_jugador['dano_causado']
        self.stats_totales['dano_recibido'] += stats_jugador['dano_recibido']
        self.stats_totales['tiempo_total'] += tiempo
    
    def mostrar_pantalla_torre(self) -> bool:
        """
        Muestra la pantalla de progreso de la torre.
        
        Returns:
            bool: True para continuar, False para abandonar
        """
        es_inicio = (self.pelea_actual == 0)
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                        return True
                    elif evento.key == pygame.K_ESCAPE:
                        return False
            
            self._dibujar_pantalla_progreso(es_inicio)
            
            pygame.display.flip()
            self.reloj.tick(30)
    
    def _dibujar_pantalla_progreso(self, es_inicio: bool):
        """Dibuja la pantalla de progreso"""
        self.pantalla.fill((10, 10, 30))
        
        # Título
        titulo = self.fuente_grande.render("MODO TORRE", True, AMARILLO)
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))
        
        # Información del próximo oponente
        if self.pelea_actual < len(self.oponentes):
            oponente = self._obtener_datos_oponente(self.oponentes[self.pelea_actual])
            if oponente:
                texto = "PRIMER RIVAL:" if es_inicio else "PROXIMO:"
                texto_completo = f"{texto} {oponente['nombre'].upper()}"
                texto_render = self.fuente_media.render(texto_completo, True, AMARILLO)
                self.pantalla.blit(texto_render, (ANCHO // 2 - texto_render.get_width() // 2, 70))
        
        # Torre con iconos
        if self.imagen_torre:
            self._dibujar_torre_con_iconos()
        
        # Progreso
        progreso = self.fuente_pequena.render(
            f"Pelea {self.pelea_actual + 1} de {len(self.oponentes)}",
            True, BLANCO
        )
        self.pantalla.blit(progreso, (30, ALTO - 80))
        
        # Instrucciones
        if es_inicio:
            inst = "ENTER para comenzar | ESC para cancelar"
        else:
            inst = "ENTER para continuar | ESC para abandonar"
        
        instruccion = self.fuente_pequena.render(inst, True, NARANJA)
        self.pantalla.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO - 30))
    
    def _dibujar_torre_con_iconos(self):
        """Dibuja la torre con los iconos de oponentes"""
        torre_escalada = pygame.transform.scale(self.imagen_torre, (250, 500))
        torre_x = ANCHO // 2 - torre_escalada.get_width() // 2
        torre_y = 95
        self.pantalla.blit(torre_escalada, (torre_x, torre_y))
        
        # Posiciones de los iconos (de abajo hacia arriba)
        posiciones = [
            (torre_x + 120, torre_y + 305),  # Abajo
            (torre_x + 120, torre_y + 160),  # Medio
            (torre_x + 120, torre_y + 15),   # Arriba
        ]
        
        for i, oponente_id in enumerate(self.oponentes):
            oponente_data = self._obtener_datos_oponente(oponente_id)
            
            if oponente_data:
                pos_x, pos_y = posiciones[i]
                self._dibujar_icono_oponente(oponente_data, pos_x, pos_y, i)
    
    def _dibujar_icono_oponente(self, oponente_data: Dict, x: int, y: int, indice: int):
        """Dibuja el icono de un oponente"""
        try:
            icono = pygame.image.load(oponente_data["foto_seleccion"]).convert()
            icono.set_colorkey((255, 255, 255))
            icono = pygame.transform.scale(icono, (50, 50))
            
            self.pantalla.blit(icono, (x, y))
            
            # Overlay si fue vencido
            if indice < self.pelea_actual:
                overlay = pygame.Surface((50, 50), pygame.SRCALPHA)
                overlay.fill((0, 200, 0, 100))
                self.pantalla.blit(overlay, (x, y))
                
                check = self.fuente_grande.render("✓", True, (0, 255, 0))
                self.pantalla.blit(check, (x + 10, y + 5))
            
            # Borde según estado
            if indice < self.pelea_actual:
                color_borde = (0, 255, 0)  # Vencido
                grosor = 2
            elif indice == self.pelea_actual:
                color_borde = AMARILLO  # Actual
                grosor = 4
            else:
                color_borde = BLANCO  # Pendiente
                grosor = 2
            
            pygame.draw.rect(self.pantalla, color_borde, (x - 2, y - 2, 54, 54), grosor)
        except:
            pygame.draw.rect(self.pantalla, BLANCO, (x, y, 50, 50), 2)
    
    def mostrar_pantalla_victoria_torre(self):
        """Muestra la pantalla de victoria al completar la torre"""
        from src.managers.records_manager import RecordsManager
        
        nombre_input = ""
        ingresando_nombre = True
        cursor_visible = True
        ultimo_parpadeo = pygame.time.get_ticks()
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if ingresando_nombre:
                        if evento.key == pygame.K_RETURN and len(nombre_input) > 0:
                            records_manager = RecordsManager()
                            records_manager.agregar_record_torre(
                                nombre_input,
                                len(self.oponentes),
                                self.stats_totales
                            )
                            return
                        elif evento.key == pygame.K_BACKSPACE:
                            nombre_input = nombre_input[:-1]
                        elif evento.key == pygame.K_ESCAPE:
                            return
                        elif len(nombre_input) < 3 and evento.unicode.isalpha():
                            nombre_input += evento.unicode.upper()
            
            ahora = pygame.time.get_ticks()
            if ahora - ultimo_parpadeo > 500:
                cursor_visible = not cursor_visible
                ultimo_parpadeo = ahora
            
            self._dibujar_pantalla_victoria(nombre_input, cursor_visible)
            
            pygame.display.flip()
            self.reloj.tick(30)
    
    def mostrar_pantalla_game_over(self):
        """Muestra la pantalla de Game Over"""
        from src.managers.records_manager import RecordsManager
        
        nombre_input = ""
        ingresando_nombre = True
        cursor_visible = True
        ultimo_parpadeo = pygame.time.get_ticks()
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if ingresando_nombre:
                        if evento.key == pygame.K_RETURN and len(nombre_input) > 0:
                            records_manager = RecordsManager()
                            records_manager.agregar_record_torre(
                                nombre_input,
                                self.pelea_actual,
                                self.stats_totales
                            )
                            return
                        elif evento.key == pygame.K_BACKSPACE:
                            nombre_input = nombre_input[:-1]
                        elif evento.key == pygame.K_ESCAPE:
                            return
                        elif len(nombre_input) < 3 and evento.unicode.isalpha():
                            nombre_input += evento.unicode.upper()
            
            ahora = pygame.time.get_ticks()
            if ahora - ultimo_parpadeo > 500:
                cursor_visible = not cursor_visible
                ultimo_parpadeo = ahora
            
            self._dibujar_pantalla_derrota(nombre_input, cursor_visible)
            
            pygame.display.flip()
            self.reloj.tick(30)
    
    def _dibujar_pantalla_victoria(self, nombre_input: str, cursor_visible: bool):
        """Dibuja la pantalla de victoria"""
        self.pantalla.fill((10, 10, 30))
        
        titulo = self.fuente_grande.render("TORRE COMPLETADA!", True, (255, 215, 0))
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 30))
        
        subtitulo = self.fuente_media.render("¡FELICIDADES!", True, AMARILLO)
        self.pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 80))
        
        self._dibujar_estadisticas(140)
        self._dibujar_input_nombre(nombre_input, cursor_visible, 270)
    
    def _dibujar_pantalla_derrota(self, nombre_input: str, cursor_visible: bool):
        """Dibuja la pantalla de derrota"""
        self.pantalla.fill((10, 10, 30))
        
        titulo = self.fuente_grande.render("GAME OVER", True, ROJO)
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 40))
        
        subtitulo = self.fuente_media.render(
            f"Llegaste al nivel {self.pelea_actual + 1}",
            True, AMARILLO
        )
        self.pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 100))
        
        self._dibujar_estadisticas(160)
        self._dibujar_input_nombre(nombre_input, cursor_visible, 280)
    
    def _dibujar_estadisticas(self, y_inicial: int):
        """Dibuja las estadísticas acumuladas"""
        stats_textos = [
            f"Peleas ganadas: {self.pelea_actual}",
            f"Golpes totales: {self.stats_totales['golpes_totales']}",
            f"Daño causado: {int(self.stats_totales['dano_causado'])}",
            f"Daño recibido: {int(self.stats_totales['dano_recibido'])}",
            f"Tiempo total: {self.stats_totales['tiempo_total'] // 60}:{self.stats_totales['tiempo_total'] % 60:02d}"
        ]
        
        y = y_inicial
        for texto in stats_textos:
            render = self.fuente_pequena.render(texto, True, BLANCO)
            self.pantalla.blit(render, (ANCHO // 2 - render.get_width() // 2, y))
            y += 25
    
    def _dibujar_input_nombre(self, nombre_input: str, cursor_visible: bool, y: int):
        """Dibuja el input de nombre"""
        prompt = self.fuente_media.render("INGRESA TU NOMBRE (3 LETRAS):", True, BLANCO)
        self.pantalla.blit(prompt, (ANCHO // 2 - prompt.get_width() // 2, y))
        
        texto_input = nombre_input + ("|" if cursor_visible else " ")
        input_render = self.fuente_grande.render(texto_input, True, AMARILLO)
        self.pantalla.blit(input_render, (ANCHO // 2 - input_render.get_width() // 2, y + 40))
        
        instruccion = self.fuente_pequena.render("ENTER: guardar | ESC: saltar", True, NARANJA)
        self.pantalla.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO - 40))
    
    def _obtener_datos_oponente(self, oponente_id: str) -> Optional[Dict]:
        """Obtiene los datos de un oponente por su ID"""
        for personaje in self.personajes_data:
            if personaje['id'] == oponente_id:
                return personaje
        return None