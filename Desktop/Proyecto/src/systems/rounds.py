"""
Sistema de gestión de rounds.
Maneja la lógica de rounds, KO y pantallas finales.
"""
import pygame
import sys
from typing import Optional, Literal
from src.entities.player import Player
from src.utils.config import (
    ANCHO, ALTO, AMARILLO, NEGRO, BLANCO, NARANJA, ROJO,
    FPS, RoundsConfig, TimeConfig
)


class RoundsManager:
    """Gestor del sistema de rounds"""
    
    def __init__(self, pantalla: pygame.Surface, reloj: pygame.time.Clock):
        """
        Inicializa el gestor de rounds.
        
        Args:
            pantalla: Surface de pygame
            reloj: Clock de pygame
        """
        self.pantalla = pantalla
        self.reloj = reloj
        
        # Estado de rounds
        self.rounds_jugador1 = 0
        self.rounds_jugador2 = 0
        self.max_rounds = RoundsConfig.MAX_ROUNDS
        self.round_actual = 1
        
        # Estados
        self.en_cuenta_regresiva = False
        self.tiempo_cuenta_regresiva = 0
        self.pelea_terminada = False
        self.mostrando_ko = False
        self.tiempo_inicio_ko = 0
        
        # Estadísticas
        self.stats_jugador1 = {
            'golpes_totales': 0,
            'dano_causado': 0,
            'dano_recibido': 0
        }
        self.stats_jugador2 = {
            'golpes_totales': 0,
            'dano_causado': 0,
            'dano_recibido': 0
        }
        self.tiempo_inicio_pelea_total = 0
        
        # Fuentes
        try:
            self.fuente_grande = pygame.font.Font("Fuentes/PressStart2P.ttf", 100)
            self.fuente_media = pygame.font.Font("Fuentes/PressStart2P.ttf", 24)
            self.fuente_pequena = pygame.font.Font("Fuentes/PressStart2P.ttf", 12)
        except:
            self.fuente_grande = pygame.font.SysFont(None, 100)
            self.fuente_media = pygame.font.SysFont(None, 36)
            self.fuente_pequena = pygame.font.SysFont(None, 18)
    
    def reiniciar(self):
        """Reinicia el sistema de rounds"""
        self.rounds_jugador1 = 0
        self.rounds_jugador2 = 0
        self.round_actual = 1
        self.pelea_terminada = False
        self.mostrando_ko = False
        
        self.stats_jugador1 = {'golpes_totales': 0, 'dano_causado': 0, 'dano_recibido': 0}
        self.stats_jugador2 = {'golpes_totales': 0, 'dano_causado': 0, 'dano_recibido': 0}
        self.tiempo_inicio_pelea_total = pygame.time.get_ticks()
    
    def terminar_round(self, ganador: int):
        """
        Termina el round actual.
        
        Args:
            ganador: Número del jugador ganador (1 o 2)
        """
        if ganador == 1:
            self.rounds_jugador1 += 1
        elif ganador == 2:
            self.rounds_jugador2 += 1
        
        self.mostrando_ko = True
        self.tiempo_inicio_ko = pygame.time.get_ticks()
        
        if self.rounds_jugador1 >= self.max_rounds or self.rounds_jugador2 >= self.max_rounds:
            self.pelea_terminada = True
    
    def iniciar_cuenta_regresiva(self):
        """Inicia la cuenta regresiva entre rounds"""
        self.en_cuenta_regresiva = True
        self.tiempo_cuenta_regresiva = pygame.time.get_ticks()
        self.round_actual += 1
    
    def actualizar_estadisticas(self, stats: dict):
        """
        Actualiza las estadísticas desde el sistema de colisiones.
        
        Args:
            stats: Diccionario con estadísticas de ambos jugadores
        """
        self.stats_jugador1 = stats['jugador1']
        self.stats_jugador2 = stats['jugador2']
    
    def mostrar_animacion_ko(self, fondo: Optional[pygame.Surface],
                            jugador1: Player, jugador2: Player,
                            ui_manager) -> bool:
        """
        Muestra la animación de KO.
        
        Args:
            fondo: Fondo del juego
            jugador1: Jugador 1
            jugador2: Jugador 2
            ui_manager: Gestor de UI
            
        Returns:
            bool: True si terminó la animación
        """
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_ko
        
        if fondo:
            self.pantalla.blit(fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        jugador1.actualizar()
        jugador2.actualizar()
        jugador1.dibujar(self.pantalla)
        jugador2.dibujar(self.pantalla)
        
        ui_manager.dibujar_barras_jugadores(
            jugador1, jugador2,
            self.rounds_jugador1, self.rounds_jugador2
        )
        ui_manager.dibujar_timer(0, en_introduccion=True)
        
        # Texto K.O.
        texto_ko = self.fuente_grande.render("K.O.", True, ROJO)
        sombra = self.fuente_grande.render("K.O.", True, NEGRO)
        
        rect_sombra = sombra.get_rect(center=(ANCHO // 2 + 3, ALTO // 2 + 3))
        rect_texto = texto_ko.get_rect(center=(ANCHO // 2, ALTO // 2))
        
        self.pantalla.blit(sombra, rect_sombra)
        self.pantalla.blit(texto_ko, rect_texto)
        
        pygame.display.flip()
        
        if tiempo_transcurrido > TimeConfig.DURACION_KO:
            self.mostrando_ko = False
            if not self.pelea_terminada:
                self.iniciar_cuenta_regresiva()
            return True
        
        return False
    
    def mostrar_cuenta_regresiva(self, fondo: Optional[pygame.Surface],
                                 jugador1: Player, jugador2: Player,
                                 ui_manager) -> Optional[int]:
        """
        Muestra la cuenta regresiva entre rounds.
        
        Returns:
            Optional[int]: Nuevo tiempo de inicio de combate o None
        """
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_cuenta_regresiva) / 1000
        
        if fondo:
            self.pantalla.blit(fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        jugador1.dibujar(self.pantalla)
        jugador2.dibujar(self.pantalla)
        
        ui_manager.dibujar_barras_jugadores(
            jugador1, jugador2,
            self.rounds_jugador1, self.rounds_jugador2
        )
        ui_manager.dibujar_timer(0, en_introduccion=True)
        
        # Mostrar "ROUND X"
        if tiempo_transcurrido < 1.5:
            texto = f"ROUND {self.round_actual}"
            self._dibujar_texto_centrado(texto, AMARILLO, ALTO // 2 - 50)
        
        # Cuenta regresiva
        elif tiempo_transcurrido < 4.5:
            tiempo_cuenta = tiempo_transcurrido - 1.5
            numero = 3 - int(tiempo_cuenta)
            
            if numero > 0:
                texto = str(numero)
                color = AMARILLO
            else:
                texto = "FIGHT!"
                color = ROJO
            
            self._dibujar_texto_centrado(texto, color, ALTO // 2)
        else:
            self.en_cuenta_regresiva = False
            pygame.display.flip()
            return pygame.time.get_ticks()
        
        pygame.display.flip()
        return None
    
    def reiniciar_jugadores(self, jugador1: Player, jugador2: Player):
        """
        Reinicia los jugadores para un nuevo round.
        
        Args:
            jugador1: Jugador 1
            jugador2: Jugador 2
        """
        # Resetear estados
        jugador1.resetear_ko()
        jugador2.resetear_ko()
        
        # Reiniciar vida y stamina
        jugador1.vida_actual = jugador1.vida_maxima
        jugador1.stamina_actual = jugador1.stamina_maxima
        jugador2.vida_actual = jugador2.vida_maxima
        jugador2.stamina_actual = jugador2.stamina_maxima
        
        # Reiniciar posiciones
        jugador1.x = 100
        jugador1.y = ALTO - 150 - 80
        jugador2.x = ANCHO - 200
        jugador2.y = ALTO - 150 - 80
        
        # Limpiar proyectiles
        jugador1.bolas_activas = []
        jugador2.bolas_activas = []
        jugador1.kamehameha_activo = None
        jugador2.kamehameha_activo = None
    
    def mostrar_pantalla_final(self, es_modo_torre: bool = False) -> Literal["menu", "rematch"]:
        """
        Muestra la pantalla final con estadísticas.
        
        Args:
            es_modo_torre: True si es modo torre
            
        Returns:
            str: "menu" o "rematch"
        """
        from src.managers.records_manager import RecordsManager
        
        ganador_num = 1 if self.rounds_jugador1 > self.rounds_jugador2 else 2
        ganador = "JUGADOR 1" if ganador_num == 1 else "JUGADOR 2"
        
        tiempo_total = (pygame.time.get_ticks() - self.tiempo_inicio_pelea_total) // 1000
        
        # En modo torre, retornar automáticamente
        if es_modo_torre:
            pygame.time.wait(2000)
            return "menu"
        
        # Sistema de input de nombre
        nombre_input = ""
        ingresando_nombre = (ganador_num == 1)
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
                            records_manager.agregar_record(
                                nombre_input,
                                self.stats_jugador1,
                                self.stats_jugador2,
                                self.rounds_jugador1,
                                self.rounds_jugador2,
                                tiempo_total
                            )
                            ingresando_nombre = False
                        elif evento.key == pygame.K_BACKSPACE:
                            nombre_input = nombre_input[:-1]
                        elif len(nombre_input) < 3 and evento.unicode.isalpha():
                            nombre_input += evento.unicode.upper()
                    else:
                        if evento.key == pygame.K_ESCAPE:
                            return "menu"
                        elif evento.key == pygame.K_RETURN:
                            return "rematch"
            
            # Parpadeo del cursor
            ahora = pygame.time.get_ticks()
            if ahora - ultimo_parpadeo > 500:
                cursor_visible = not cursor_visible
                ultimo_parpadeo = ahora
            
            self._dibujar_pantalla_victoria(
                ganador, tiempo_total,
                ingresando_nombre, nombre_input,
                cursor_visible
            )
            
            pygame.display.flip()
            self.reloj.tick(FPS)
    
    def _dibujar_texto_centrado(self, texto: str, color: tuple, y: int):
        """Dibuja texto centrado con sombra"""
        texto_render = self.fuente_grande.render(texto, True, color)
        sombra = self.fuente_grande.render(texto, True, NEGRO)
        
        rect_sombra = sombra.get_rect(center=(ANCHO // 2 + 3, y + 3))
        rect_texto = texto_render.get_rect(center=(ANCHO // 2, y))
        
        self.pantalla.blit(sombra, rect_sombra)
        self.pantalla.blit(texto_render, rect_texto)
    
    def _dibujar_pantalla_victoria(self, ganador: str, tiempo_total: int,
                                   ingresando_nombre: bool, nombre_input: str,
                                   cursor_visible: bool):
        """Dibuja la pantalla de victoria"""
        self.pantalla.fill((10, 10, 30))
        
        # Título
        titulo = self.fuente_media.render("VICTORIA", True, AMARILLO)
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 30))
        
        # Ganador
        texto_ganador = self.fuente_media.render(f"{ganador} GANA!", True, AMARILLO)
        self.pantalla.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, 80))
        
        if ingresando_nombre:
            self._dibujar_input_nombre(nombre_input, cursor_visible)
        else:
            self._dibujar_estadisticas_finales(tiempo_total)
    
    def _dibujar_input_nombre(self, nombre_input: str, cursor_visible: bool):
        """Dibuja el input de nombre"""
        prompt = self.fuente_pequena.render("INGRESA TU NOMBRE (3 LETRAS):", True, BLANCO)
        self.pantalla.blit(prompt, (ANCHO // 2 - prompt.get_width() // 2, 130))
        
        texto_input = nombre_input + ("|" if cursor_visible else " ")
        input_render = self.fuente_media.render(texto_input, True, AMARILLO)
        self.pantalla.blit(input_render, (ANCHO // 2 - input_render.get_width() // 2, 170))
        
        instruccion = self.fuente_pequena.render("ENTER para guardar", True, NARANJA)
        self.pantalla.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, 220))
    
    def _dibujar_estadisticas_finales(self, tiempo_total: int):
        """Dibuja las estadísticas finales"""
        # Rounds
        texto_rounds = self.fuente_pequena.render(
            f"Rounds: {self.rounds_jugador1} - {self.rounds_jugador2}",
            True, BLANCO
        )
        self.pantalla.blit(texto_rounds, (ANCHO // 2 - texto_rounds.get_width() // 2, 130))
        
        # Estadísticas en columnas
        y_stats = 180
        col1_x, col2_x = 80, ANCHO - 280
        
        self._dibujar_columna_stats("JUGADOR 1", self.stats_jugador1, col1_x, y_stats)
        self._dibujar_columna_stats("JUGADOR 2", self.stats_jugador2, col2_x, y_stats)
        
        # Tiempo
        minutos = tiempo_total // 60
        segundos = tiempo_total % 60
        tiempo_texto = self.fuente_pequena.render(
            f"Tiempo: {minutos}:{segundos:02d}",
            True, NARANJA
        )
        self.pantalla.blit(tiempo_texto, (ANCHO // 2 - tiempo_texto.get_width() // 2, 320))
        
        # Instrucciones
        inst = self.fuente_pequena.render("ESC: Menú | ENTER: Rematch", True, NARANJA)
        self.pantalla.blit(inst, (ANCHO // 2 - inst.get_width() // 2, ALTO - 40))
    
    def _dibujar_columna_stats(self, titulo: str, stats: dict, x: int, y: int):
        """Dibuja una columna de estadísticas"""
        titulo_render = self.fuente_pequena.render(titulo, True, AMARILLO)
        self.pantalla.blit(titulo_render, (x, y))
        
        stats_texto = [
            f"Golpes: {stats['golpes_totales']}",
            f"Daño: {int(stats['dano_causado'])}",
            f"Recibido: {int(stats['dano_recibido'])}"
        ]
        
        for i, stat in enumerate(stats_texto):
            texto = self.fuente_pequena.render(stat, True, BLANCO)
            self.pantalla.blit(texto, (x, y + 30 + i * 25))