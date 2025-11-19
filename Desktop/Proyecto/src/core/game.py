"""
Motor principal del juego.
Coordina todos los sistemas y maneja el game loop.
"""
import pygame
import sys
from typing import Dict, Optional
from src.entities.player import Player
from src.systems.ai import AIController
from src.systems.collision import CollisionSystem
from src.systems.rounds import RoundsManager
from src.ui.hud import HUDManager
from src.ui.transitions import TransitionManager
from src.managers.audio_manager import AudioManager
from src.utils.config import (
    ANCHO, ALTO, NEGRO, FPS, 
    CONTROLES_JUGADOR1, CONTROLES_JUGADOR2
)


class GameEngine:
    """Motor principal del juego"""
    
    def __init__(self, pantalla: pygame.Surface, reloj: pygame.time.Clock,
                 sprites_personajes: Dict, fondo_seleccionado: str,
                 personaje1_nombre: str = 'goku',
                 personaje2_nombre: str = 'freezer',
                 es_modo_torre: bool = False,
                 audio_manager: Optional[AudioManager] = None):
        """
        Inicializa el motor del juego.
        
        Args:
            pantalla: Surface de pygame
            reloj: Clock de pygame
            sprites_personajes: Diccionario con sprites
            fondo_seleccionado: Ruta del fondo
            personaje1_nombre: ID del personaje 1
            personaje2_nombre: ID del personaje 2
            es_modo_torre: Si es modo torre
            audio_manager: Gestor de audio
        """
        self.pantalla = pantalla
        self.reloj = reloj
        self.sprites_personajes = sprites_personajes
        self.personaje1_nombre = personaje1_nombre
        self.personaje2_nombre = personaje2_nombre
        self.es_modo_torre = es_modo_torre
        
        # Gestores
        self.audio_manager = audio_manager or AudioManager()
        self.hud_manager = HUDManager(pantalla)
        self.transition_manager = TransitionManager(pantalla)
        self.rounds_manager = RoundsManager(pantalla, reloj)
        
        # Jugadores
        self.jugador1: Optional[Player] = None
        self.jugador2: Optional[Player] = None
        
        # Sistemas
        self.collision_system: Optional[CollisionSystem] = None
        self.ai_controller: Optional[AIController] = None
        
        # Estado
        self.ejecutando = False
        self.en_introduccion = True
        self.tiempo_inicio = 0
        self.fase_intro = "vs"
        self.tiempo_combate = 60
        self.tiempo_inicio_combate = 0
        self.nivel_torre = 0
        self.dificultad_1vs1 = 'normal'
        
        # Cargar fondo
        try:
            self.fondo = pygame.image.load(fondo_seleccionado).convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        except:
            self.fondo = None
    
    def inicializar_jugadores(self, personaje1: str, personaje2: str):
        """Inicializa los jugadores"""
        sprites_j1 = self.sprites_personajes[personaje1]
        sprites_j2 = self.sprites_personajes[personaje2]
        
        self.jugador1 = Player(100, ALTO - 230, CONTROLES_JUGADOR1, sprites_j1)
        self.jugador2 = Player(ANCHO - 200, ALTO - 230, CONTROLES_JUGADOR2, sprites_j2)
        
        # Inicializar sistemas
        self.collision_system = CollisionSystem(self.jugador1, self.jugador2)
        
        # Configurar IA si es necesario
        if self.es_modo_torre or hasattr(self, 'dificultad_1vs1'):
            if self.es_modo_torre:
                dificultades = ['facil', 'normal', 'dificil']
                dificultad = dificultades[min(self.nivel_torre, 2)]
            else:
                dificultad = self.dificultad_1vs1
            
            self.ai_controller = AIController(self.jugador2, self.jugador1, dificultad)
    
    def ejecutar(self, personaje1: str, personaje2: str, nivel_torre: int = 0):
        """
        Ejecuta el game loop principal.
        
        Args:
            personaje1: ID del personaje 1
            personaje2: ID del personaje 2
            nivel_torre: Nivel de torre (0 = no torre)
        """
        self.nivel_torre = nivel_torre
        self.inicializar_jugadores(personaje1, personaje2)
        self.ejecutando = True
        self.en_introduccion = True
        self.tiempo_inicio = pygame.time.get_ticks()
        self.fase_intro = "vs"
        
        self.rounds_manager.reiniciar()
        self.audio_manager.reproducir_musica_pelea()
        
        while self.ejecutando:
            self._manejar_eventos()
            
            if self.rounds_manager.pelea_terminada:
                resultado = self.rounds_manager.mostrar_pantalla_final(self.es_modo_torre)
                if resultado == "menu":
                    self.ejecutando = False
                elif resultado == "rematch":
                    return self.ejecutar(personaje1, personaje2)
            
            elif self.rounds_manager.mostrando_ko:
                self.rounds_manager.mostrar_animacion_ko(
                    self.fondo, self.jugador1, self.jugador2, self.hud_manager
                )
                if not self.rounds_manager.mostrando_ko and not self.rounds_manager.pelea_terminada:
                    self.rounds_manager.reiniciar_jugadores(self.jugador1, self.jugador2)
            
            elif self.en_introduccion:
                self._actualizar_introduccion()
            
            elif self.rounds_manager.en_cuenta_regresiva:
                nuevo_tiempo = self.rounds_manager.mostrar_cuenta_regresiva(
                    self.fondo, self.jugador1, self.jugador2, self.hud_manager
                )
                if nuevo_tiempo:
                    self.tiempo_inicio_combate = nuevo_tiempo
            
            else:
                self._actualizar_juego()
                self._dibujar_juego()
            
            self.reloj.tick(FPS)
        
        self.audio_manager.reproducir_musica_menu()
    
    def _manejar_eventos(self):
        """Maneja los eventos del juego"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                # Control de volumen
                if evento.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                    self.audio_manager.bajar_volumen()
                elif evento.key in [pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS]:
                    self.audio_manager.subir_volumen()
                elif evento.key == pygame.K_ESCAPE:
                    # TODO: Implementar menú de pausa
                    pass
                
                # Controles J1
                self._procesar_controles_jugador1(evento.key)
                
                # Controles J2 (solo si no hay IA)
                if not self.ai_controller:
                    self._procesar_controles_jugador2(evento.key)
            
            elif evento.type == pygame.KEYUP:
                if evento.key == CONTROLES_JUGADOR1['cubrirse']:
                    self.jugador1.dejar_de_cubrirse()
                elif not self.ai_controller and evento.key == CONTROLES_JUGADOR2['cubrirse']:
                    self.jugador2.dejar_de_cubrirse()
    
    def _procesar_controles_jugador1(self, tecla: int):
        """Procesa controles del jugador 1"""
        if tecla == CONTROLES_JUGADOR1['golpe_ligero']:
            self.jugador1.iniciar_golpe('golpe_j')
        elif tecla == CONTROLES_JUGADOR1['patada']:
            self.jugador1.iniciar_golpe('patada_k')
        elif tecla == CONTROLES_JUGADOR1['cubrirse']:
            self.jugador1.cubrirse()
        elif tecla == CONTROLES_JUGADOR1['bola']:
            self.jugador1.iniciar_lanzar_bola()
        elif tecla == CONTROLES_JUGADOR1.get('kamehameha'):
            self.jugador1.iniciar_kamehameha()
        elif tecla == CONTROLES_JUGADOR1['movimiento_final']:
            self.jugador1.iniciar_movimiento_final()
    
    def _procesar_controles_jugador2(self, tecla: int):
        """Procesa controles del jugador 2"""
        if tecla == CONTROLES_JUGADOR2['golpe_ligero']:
            self.jugador2.iniciar_golpe('golpe_j')
        elif tecla == CONTROLES_JUGADOR2['patada']:
            self.jugador2.iniciar_golpe('patada_k')
        elif tecla == CONTROLES_JUGADOR2['cubrirse']:
            self.jugador2.cubrirse()
        elif tecla == CONTROLES_JUGADOR2['bola']:
            self.jugador2.iniciar_lanzar_bola()
        elif tecla == CONTROLES_JUGADOR2.get('movimiento_final'):
            self.jugador2.iniciar_movimiento_final()
    
    def _actualizar_introduccion(self):
        """Actualiza la pantalla de introducción"""
        if self.fase_intro == "vs":
            terminado = self.transition_manager.mostrar_vs(
                self.fondo, self.jugador1, self.jugador2, self.tiempo_inicio
            )
            if terminado:
                self.fase_intro = "countdown"
                self.tiempo_inicio = pygame.time.get_ticks()
        
        elif self.fase_intro == "countdown":
            resultado = self.transition_manager.mostrar_cuenta_regresiva(
                self.fondo, self.jugador1, self.jugador2, self.tiempo_inicio
            )
            if resultado:
                self.en_introduccion = False
                self.tiempo_inicio_combate = pygame.time.get_ticks()
    
    def _actualizar_juego(self):
        """Actualiza la lógica del juego"""
        teclas = pygame.key.get_pressed()
        
        # Actualizar jugadores
        self.jugador1.actualizar()
        self.jugador2.actualizar()
        
        # Movimiento
        if not self._jugador_esta_ocupado(self.jugador1):
            self.jugador1.mover(teclas)
        
        if not self._jugador_esta_ocupado(self.jugador2):
            if self.ai_controller:
                self.ai_controller.actualizar()
            else:
                self.jugador2.mover(teclas)
        
        # Orientación
        if self.jugador1.x < self.jugador2.x:
            self.jugador1.mirando_derecha = True
            self.jugador2.mirando_derecha = False
        else:
            self.jugador1.mirando_derecha = False
            self.jugador2.mirando_derecha = True
        
        # Proyectiles
        self.jugador1.actualizar_proyectiles()
        self.jugador2.actualizar_proyectiles()
        
        # Colisiones
        self.collision_system.detectar_todas()
        self.rounds_manager.actualizar_estadisticas(
            self.collision_system.obtener_estadisticas()
        )
        
        # Verificar KO
        if self.jugador1.vida_actual <= 0:
            self.rounds_manager.terminar_round(2)
        elif self.jugador2.vida_actual <= 0:
            self.rounds_manager.terminar_round(1)
    
    def _jugador_esta_ocupado(self, jugador: Player) -> bool:
        """Verifica si un jugador está ocupado"""
        return any([
            jugador.golpe_animando,
            jugador.cubriendose,
            jugador.lanzando_bola,
            jugador.usando_kamehameha,
            jugador.usando_movimiento_final
        ])
    
    def _dibujar_juego(self):
        """Dibuja todos los elementos del juego"""
        if self.fondo:
            self.pantalla.blit(self.fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        self.jugador1.dibujar(self.pantalla)
        self.jugador2.dibujar(self.pantalla)
        
        self.jugador1.dibujar_proyectiles(self.pantalla)
        self.jugador2.dibujar_proyectiles(self.pantalla)
        
        self.hud_manager.dibujar_barras_jugadores(
            self.jugador1, self.jugador2,
            self.rounds_manager.rounds_jugador1,
            self.rounds_manager.rounds_jugador2
        )
        
        if not self.en_introduccion:
            tiempo_actual = pygame.time.get_ticks()
            segundos = (tiempo_actual - self.tiempo_inicio_combate) / 1000
            tiempo_restante = max(0, self.tiempo_combate - int(segundos))
            self.hud_manager.dibujar_timer(tiempo_restante, False)
            
            if tiempo_restante <= 0:
                self._terminar_por_tiempo()
        else:
            self.hud_manager.dibujar_timer(0, True)
        
        pygame.display.flip()
    
    def _terminar_por_tiempo(self):
        """Termina el combate por tiempo"""
        if self.jugador1.vida_actual > self.jugador2.vida_actual:
            self.rounds_manager.terminar_round(1)
        elif self.jugador2.vida_actual > self.jugador1.vida_actual:
            self.rounds_manager.terminar_round(2)