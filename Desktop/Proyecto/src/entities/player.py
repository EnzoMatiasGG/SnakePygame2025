"""
Módulo de jugador/peleador.
Contiene la lógica del personaje jugable.
"""
import pygame
from typing import Dict, List, Optional
from src.entities.proyectile import Projectile
from src.entities.special_moves import Kamehameha
from src.utils.config import (
    ANCHO, ALTO, CombatConfig, TimeConfig
)


class Player:
    """Representa un peleador en el juego"""
    
    def __init__(self, x: int, y: int, controles: Dict, sprites: Dict):
        """
        Inicializa un jugador.
        
        Args:
            x, y: Posición inicial
            controles: Diccionario de teclas de control
            sprites: Diccionario de sprites del personaje
        """
        # Posición
        self.x = x
        self.y = y
        self.velocidad = 5
        
        # Controles y sprites
        self.controles = controles
        self.sprites = sprites
        self.estado = 'inicio'
        self.sprite = self.sprites[self.estado]
        self.mirando_derecha = True
        
        # Hitbox
        self.rect = pygame.Rect(
            self.x, self.y, 
            self.sprite.get_width(), 
            self.sprite.get_height()
        )
        
        # Sistema de golpes
        self.golpe_animando = False
        self.golpe_tipo = None
        self.golpe_frame = 0
        self.golpe_contador = 0
        self.golpe_ultimo_tiempo = 0
        
        # Hitbox de ataque
        self.hitbox_activa = False
        self.hitbox_ataque = None
        self.dano_golpe_j = CombatConfig.DANO_GOLPE
        self.dano_patada_k = CombatConfig.DANO_PATADA
        self.dano_bola = CombatConfig.DANO_BOLA
        self.dano_kamehameha = CombatConfig.DANO_KAMEHAMEHA
        self.dano_movimiento_final = CombatConfig.DANO_MOVIMIENTO_FINAL
        
        # Sistema de defensa
        self.cubriendose = False
        
        # Sistema de proyectiles
        self.bolas_activas: List[Projectile] = []
        self.imagen_bola = self.sprites.get('poder_ligero', None)
        
        # Animación lanzamiento bola
        self.lanzando_bola = False
        self.bola_energia_frames = self.sprites.get('bola_energia', [])
        self.bola_contador_mano = 0
        self.bola_energia_inicio_tiempo = 0
        
        # Sistema de vida y energía
        self.vida_maxima = CombatConfig.VIDA_MAXIMA
        self.vida_actual = CombatConfig.VIDA_MAXIMA
        self.stamina_maxima = CombatConfig.STAMINA_MAXIMA
        self.stamina_actual = CombatConfig.STAMINA_MAXIMA
        
        # Sistema de Kamehameha
        self.kamehameha_activo: Optional[Kamehameha] = None
        self.usando_kamehameha = False
        self.imagenes_kamehameha = self.sprites.get('kamehameha_poder', [])
        
        # Sistema de aturdimiento
        self.golpes_consecutivos = 0
        self.tiempo_ultimo_golpe = 0
        self.aturdido = False
        self.tiempo_inicio_aturdido = 0
        
        # Sistema de KO
        self.en_ko = False
        self.ko_frame = 0
        self.ko_ultimo_tiempo = 0
        self.ko_animacion_completada = False
        
        # Sistema de movimiento final
        self.usando_movimiento_final = False
        self.movimiento_final_frame = 0
        self.movimiento_final_inicio_tiempo = 0
        self.movimiento_final_tipo = None
    
    # ========================================================================
    # MÉTODOS DE ACTUALIZACIÓN
    # ========================================================================
    
    def actualizar(self):
        """Actualiza el estado del jugador"""
        self._actualizar_rect()
        
        if self.en_ko:
            self._actualizar_ko()
            return
        
        if self.aturdido:
            self._actualizar_aturdimiento()
            return
        
        if self.lanzando_bola:
            self._actualizar_animacion_bola()
        if self.golpe_animando:
            self._actualizar_golpe()
        if self.usando_kamehameha:
            self._actualizar_kamehameha()
        if self.usando_movimiento_final:
            self._actualizar_movimiento_final()
        
        # Regenerar stamina si no está atacando
        if not any([self.golpe_animando, self.lanzando_bola, 
                   self.usando_kamehameha, self.usando_movimiento_final]):
            self._regenerar_stamina()
    
    def _actualizar_rect(self):
        """Actualiza el rectángulo de colisión"""
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.rect.width = self.sprite.get_width()
        self.rect.height = self.sprite.get_height()
    
    def actualizar_proyectiles(self):
        """Actualiza todos los proyectiles activos"""
        for bola in self.bolas_activas[:]:
            bola.actualizar()
            if bola.esta_fuera_de_pantalla(ANCHO):
                self.bolas_activas.remove(bola)
    
    # ========================================================================
    # MÉTODOS DE DIBUJO
    # ========================================================================
    
    def dibujar(self, pantalla: pygame.Surface):
        """Dibuja el jugador en pantalla"""
        imagen = self.sprite
        if not self.mirando_derecha:
            imagen = pygame.transform.flip(imagen, True, False)
        pantalla.blit(imagen, (self.x, self.y))
        
        if self.kamehameha_activo:
            self.kamehameha_activo.dibujar(pantalla)
    
    def dibujar_proyectiles(self, pantalla: pygame.Surface):
        """Dibuja todos los proyectiles"""
        for bola in self.bolas_activas:
            bola.dibujar(pantalla)
    
    # ========================================================================
    # SISTEMA DE COMBATE
    # ========================================================================
    
    def iniciar_golpe(self, tipo_golpe: str):
        """Inicia un ataque cuerpo a cuerpo"""
        costo = (CombatConfig.COSTO_GOLPE if tipo_golpe == 'golpe_j' 
                else CombatConfig.COSTO_PATADA)
        
        if not self.golpe_animando and self.tiene_stamina(costo):
            self.consumir_stamina(costo)
            self.golpe_animando = True
            self.golpe_tipo = tipo_golpe
            self.golpe_frame = 0
            self.golpe_ultimo_tiempo = pygame.time.get_ticks()
            
            self._crear_hitbox_ataque()
            
            if tipo_golpe == 'golpe_j':
                self.golpe_contador = (self.golpe_contador + 1) % 2
                self.sprite = self.sprites['golpe_j'][self.golpe_contador]
            elif tipo_golpe == 'patada_k':
                self.sprite = self.sprites['patada_k'][self.golpe_frame]
    
    def _actualizar_golpe(self):
        """Actualiza la animación de golpe"""
        ahora = pygame.time.get_ticks()
        tiempo_frame = TimeConfig.TIEMPO_FRAME_GOLPE
        
        if self.golpe_tipo == 'golpe_j':
            if ahora - self.golpe_ultimo_tiempo > tiempo_frame:
                self._finalizar_golpe()
        
        elif self.golpe_tipo == 'patada_k':
            if ahora - self.golpe_ultimo_tiempo > tiempo_frame:
                self.golpe_ultimo_tiempo = ahora
                self.golpe_frame += 1
                
                if self.golpe_frame < len(self.sprites['patada_k']):
                    self.sprite = self.sprites['patada_k'][self.golpe_frame]
                    self._crear_hitbox_ataque()
                else:
                    self._finalizar_golpe()
    
    def _finalizar_golpe(self):
        """Finaliza la animación de golpe"""
        self.golpe_animando = False
        self.hitbox_activa = False
        self.hitbox_ataque = None
        self.estado = 'inicio'
        self.sprite = self.sprites[self.estado]
    
    def _crear_hitbox_ataque(self):
        """Crea la hitbox del ataque"""
        ancho_hitbox = 60
        alto_hitbox = 40
        
        if self.mirando_derecha:
            x_hitbox = self.x + self.sprite.get_width()
        else:
            x_hitbox = self.x - ancho_hitbox
        
        y_hitbox = self.y + self.sprite.get_height() // 2 - alto_hitbox // 2
        
        self.hitbox_ataque = pygame.Rect(x_hitbox, y_hitbox, ancho_hitbox, alto_hitbox)
        self.hitbox_activa = True
    
    def obtener_dano_ataque(self) -> float:
        """Retorna el daño del ataque actual"""
        if self.golpe_tipo == 'golpe_j':
            return self.dano_golpe_j
        elif self.golpe_tipo == 'patada_k':
            return self.dano_patada_k
        return 0
    
    # ========================================================================
    # SISTEMA DE DEFENSA
    # ========================================================================
    
    def cubrirse(self):
        """Activa el estado de defensa"""
        self.cubriendose = True
        self.estado = 'cubrirse'
        self.sprite = self.sprites['cubrirse']
    
    def dejar_de_cubrirse(self):
        """Desactiva el estado de defensa"""
        self.cubriendose = False
        self.estado = 'inicio'
        self.sprite = self.sprites[self.estado]
    
    def recibir_dano(self, cantidad: float) -> float:
        """
        Recibe daño y retorna el daño real aplicado.
        
        Args:
            cantidad: Cantidad de daño a recibir
            
        Returns:
            float: Daño real aplicado
        """
        if self.aturdido:
            cantidad *= CombatConfig.MULTIPLICADOR_DANO_ATURDIDO
        
        if not self.cubriendose:
            dano_real = cantidad
        else:
            dano_real = cantidad * CombatConfig.REDUCCION_DANO_CUBIERTO
        
        self.vida_actual = max(0, self.vida_actual - dano_real)
        
        if self.vida_actual <= 0 and not self.en_ko:
            self._iniciar_ko()
        
        return dano_real
    
    # ========================================================================
    # SISTEMA DE PROYECTILES
    # ========================================================================
    
    def iniciar_lanzar_bola(self):
        """Inicia el lanzamiento de una bola de energía"""
        if (not self.lanzando_bola and not self.golpe_animando and 
            not self.cubriendose and self.tiene_stamina(CombatConfig.COSTO_BOLA)):
            
            self.consumir_stamina(CombatConfig.COSTO_BOLA)
            self.lanzando_bola = True
            self.bola_energia_inicio_tiempo = pygame.time.get_ticks()
            
            # Seleccionar sprite de animación
            if isinstance(self.bola_energia_frames, list) and len(self.bola_energia_frames) >= 2:
                self.sprite = self.bola_energia_frames[self.bola_contador_mano]
                self.bola_contador_mano = (self.bola_contador_mano + 1) % 2
            elif isinstance(self.bola_energia_frames, list) and len(self.bola_energia_frames) == 1:
                self.sprite = self.bola_energia_frames[0]
            
            self._lanzar_bola()
    
    def _actualizar_animacion_bola(self):
        """Actualiza la animación de lanzamiento"""
        if not self.lanzando_bola:
            return
        
        ahora = pygame.time.get_ticks()
        if ahora - self.bola_energia_inicio_tiempo > TimeConfig.TIEMPO_ANIMACION_BOLA:
            self.lanzando_bola = False
            self.estado = 'inicio'
            self.sprite = self.sprites[self.estado]
    
    def _lanzar_bola(self):
        """Lanza un proyectil"""
        if self.imagen_bola is None:
            return
        
        centro_y = self.y + self.sprite.get_height() // 2
        
        if self.mirando_derecha:
            inicio_x = self.x + self.sprite.get_width()
            direccion = True
        else:
            inicio_x = self.x
            direccion = False
        
        nueva_bola = Projectile(inicio_x, centro_y, direccion, self.imagen_bola, dano=self.dano_bola)
        self.bolas_activas.append(nueva_bola)
    
    # ========================================================================
    # SISTEMA DE KAMEHAMEHA
    # ========================================================================
    
    def iniciar_kamehameha(self):
        """Inicia el Kamehameha"""
        if ('kamehameha' not in self.sprites or not self.imagenes_kamehameha or
            self.usando_kamehameha or not self.tiene_stamina(CombatConfig.COSTO_KAMEHAMEHA)):
            return
        
        self.consumir_stamina(CombatConfig.COSTO_KAMEHAMEHA)
        self.usando_kamehameha = True
        self.estado = 'kamehameha'
        self.sprite = self.sprites['kamehameha']
        
        origen_x = self.x + self.sprite.get_width() if self.mirando_derecha else self.x
        
        self.kamehameha_activo = Kamehameha(
            origen_x, self.y,
            self.mirando_derecha,
            self.sprite,
            self.imagenes_kamehameha
        )
    
    def _actualizar_kamehameha(self):
        """Actualiza el Kamehameha"""
        if self.kamehameha_activo:
            self.kamehameha_activo.actualizar()
            
            if not self.kamehameha_activo.esta_activo():
                self.usando_kamehameha = False
                self.kamehameha_activo = None
                self.estado = 'inicio'
                self.sprite = self.sprites[self.estado]
    
    # ========================================================================
    # SISTEMA DE MOVIMIENTOS FINALES
    # ========================================================================
    
    def iniciar_movimiento_final(self):
        """Inicia el movimiento final del personaje"""
        if (self.usando_movimiento_final or 
            not self.tiene_stamina(CombatConfig.COSTO_MOVIMIENTO_FINAL)):
            return
        
        # Detectar tipo de movimiento final
        if 'genki_pose' in self.sprites:
            self.movimiento_final_tipo = 'genkidama'
        elif 'galick_gun' in self.sprites:
            self.movimiento_final_tipo = 'galick_gun'
        elif 'masenko' in self.sprites:
            self.movimiento_final_tipo = 'masenko'
        elif 'Ulti' in self.sprites:
            self.movimiento_final_tipo = 'bola_maligna'
        else:
            return
        
        self.consumir_stamina(CombatConfig.COSTO_MOVIMIENTO_FINAL)
        self.usando_movimiento_final = True
        self.movimiento_final_frame = 0
        self.movimiento_final_inicio_tiempo = pygame.time.get_ticks()
    
    def _actualizar_movimiento_final(self):
        """Actualiza la animación del movimiento final"""
        if not self.usando_movimiento_final:
            return
        
        ahora = pygame.time.get_ticks()
        tiempo_transcurrido = ahora - self.movimiento_final_inicio_tiempo
        
        # Obtener frames según el tipo
        frames_map = {
            'genkidama': 'genki_pose',
            'galick_gun': 'galick_gun',
            'masenko': 'masenko',
            'bola_maligna': 'Ulti'
        }
        
        key = frames_map.get(self.movimiento_final_tipo)
        if not key or key not in self.sprites:
            self.usando_movimiento_final = False
            return
        
        frames = self.sprites[key]
        
        if tiempo_transcurrido > TimeConfig.TIEMPO_FRAME_MOVIMIENTO_FINAL * self.movimiento_final_frame:
            self.movimiento_final_frame += 1
            
            if self.movimiento_final_frame < len(frames):
                self.sprite = frames[self.movimiento_final_frame]
            else:
                self._lanzar_movimiento_final()
                self.usando_movimiento_final = False
                self.estado = 'inicio'
                self.sprite = self.sprites['inicio']
    
    def _lanzar_movimiento_final(self):
        """Lanza el proyectil del movimiento final"""
        imagen_map = {
            'genkidama': 'genkidama',
            'galick_gun': 'galick_gun_poder',
            'masenko': 'masenko_poder',
            'bola_maligna': 'Ulti_poder'
        }
        
        key = imagen_map.get(self.movimiento_final_tipo)
        if not key or key not in self.sprites:
            return
        
        imagen_proyectil = self.sprites[key]
        centro_y = self.y + self.sprite.get_height() // 2
        
        if self.mirando_derecha:
            inicio_x = self.x + self.sprite.get_width()
            direccion = True
        else:
            inicio_x = self.x
            direccion = False
        
        nueva_bola = Projectile(inicio_x, centro_y, direccion, imagen_proyectil, velocidad=8)
        self.bolas_activas.append(nueva_bola)
    
    # ========================================================================
    # SISTEMA DE COMBOS Y ATURDIMIENTO
    # ========================================================================
    
    def recibir_golpe_combo(self):
        """Registra un golpe para el sistema de combos"""
        ahora = pygame.time.get_ticks()
        
        if ahora - self.tiempo_ultimo_golpe > CombatConfig.TIEMPO_RESETEO_COMBO:
            self.golpes_consecutivos = 0
        
        self.golpes_consecutivos += 1
        self.tiempo_ultimo_golpe = ahora
        
        if self.golpes_consecutivos >= CombatConfig.GOLPES_PARA_ATURDIR and not self.aturdido:
            self._iniciar_aturdimiento()
    
    def _iniciar_aturdimiento(self):
        """Inicia el estado de aturdimiento"""
        self.aturdido = True
        self.tiempo_inicio_aturdido = pygame.time.get_ticks()
        self.golpes_consecutivos = 0
        self.estado = 'aturdido'
        if 'aturdido' in self.sprites:
            self.sprite = self.sprites['aturdido']
    
    def _actualizar_aturdimiento(self):
        """Actualiza el estado de aturdimiento"""
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_inicio_aturdido > CombatConfig.DURACION_ATURDIMIENTO:
            self.aturdido = False
            self.estado = 'inicio'
            self.sprite = self.sprites['inicio']
    
    # ========================================================================
    # SISTEMA DE KO
    # ========================================================================
    
    def _iniciar_ko(self):
        """Inicia la animación de KO"""
        if 'ko' not in self.sprites or len(self.sprites['ko']) == 0:
            return
        
        self.en_ko = True
        self.ko_frame = 0
        self.ko_ultimo_tiempo = pygame.time.get_ticks()
        self.ko_animacion_completada = False
        self.sprite = self.sprites['ko'][0]
    
    def _actualizar_ko(self):
        """Actualiza la animación de KO"""
        if not self.en_ko or 'ko' not in self.sprites:
            return
        
        ahora = pygame.time.get_ticks()
        
        if ahora - self.ko_ultimo_tiempo > TimeConfig.DURACION_KO // len(self.sprites['ko']):
            self.ko_ultimo_tiempo = ahora
            self.ko_frame = (self.ko_frame + 1) % len(self.sprites['ko'])
            self.sprite = self.sprites['ko'][self.ko_frame]
    
    def resetear_ko(self):
        """Resetea el estado de KO para un nuevo round"""
        self.en_ko = False
        self.ko_frame = 0
        self.ko_animacion_completada = False
        self.vida_actual = self.vida_maxima
        self.estado = 'inicio'
        self.sprite = self.sprites['inicio']
    
    # ========================================================================
    # SISTEMA DE MOVIMIENTO
    # ========================================================================
    
    def mover(self, teclas: pygame.key.ScancodeWrapper):
        """Mueve el jugador según las teclas presionadas"""
        if any([self.golpe_animando, self.lanzando_bola, self.cubriendose,
               self.usando_kamehameha, self.aturdido, self.en_ko,
               self.usando_movimiento_final]):
            return
        
        mov_x, mov_y = 0, 0
        estado_horizontal = None
        
        # Detectar movimiento diagonal y horizontal
        if teclas[self.controles['izquierda']] and teclas[self.controles['arriba']]:
            mov_x, mov_y = -self.velocidad, -self.velocidad
            estado_horizontal = 'izquierda'
        elif teclas[self.controles['derecha']] and teclas[self.controles['arriba']]:
            mov_x, mov_y = self.velocidad, -self.velocidad
            estado_horizontal = 'derecha'
        elif teclas[self.controles['izquierda']] and teclas[self.controles['abajo']]:
            mov_x, mov_y = -self.velocidad, self.velocidad
            estado_horizontal = 'izquierda'
        elif teclas[self.controles['derecha']] and teclas[self.controles['abajo']]:
            mov_x, mov_y = self.velocidad, self.velocidad
            estado_horizontal = 'derecha'
        elif teclas[self.controles['izquierda']]:
            mov_x = -self.velocidad
            estado_horizontal = 'izquierda'
        elif teclas[self.controles['derecha']]:
            mov_x = self.velocidad
            estado_horizontal = 'derecha'
        elif teclas[self.controles['arriba']]:
            mov_y = -self.velocidad
        elif teclas[self.controles['abajo']]:
            mov_y = self.velocidad
        
        # Aplicar movimiento con límites
        self._aplicar_movimiento(mov_x, mov_y, estado_horizontal)
    
    def _aplicar_movimiento(self, mov_x: float, mov_y: float, estado_horizontal: Optional[str]):
        """Aplica el movimiento con límites de pantalla"""
        nuevo_x = self.x + mov_x
        nuevo_y = self.y + mov_y
        
        ancho_sprite = self.sprite.get_width()
        alto_sprite = self.sprite.get_height()
        
        # Limitar a los bordes de la pantalla
        if nuevo_x < 0:
            nuevo_x = 0
        elif nuevo_x > ANCHO - ancho_sprite:
            nuevo_x = ANCHO - ancho_sprite
        
        if nuevo_y < 0:
            nuevo_y = 0
        elif nuevo_y > ALTO - alto_sprite:
            nuevo_y = ALTO - alto_sprite
        
        self.x = nuevo_x
        self.y = nuevo_y
        self.rect.topleft = (self.x, self.y)
        
        # Actualizar sprite según movimiento
        if estado_horizontal is not None:
            self.estado = estado_horizontal
        else:
            if mov_y != 0:
                self.estado = 'bajar'
            else:
                self.estado = 'inicio'
        
        self.sprite = self.sprites[self.estado]
    
    # ========================================================================
    # SISTEMA DE RECURSOS
    # ========================================================================
    
    def tiene_stamina(self, cantidad: float) -> bool:
        """Verifica si tiene suficiente stamina"""
        return self.stamina_actual >= cantidad
    
    def consumir_stamina(self, cantidad: float):
        """Consume stamina"""
        self.stamina_actual = max(0, self.stamina_actual - cantidad)
    
    def _regenerar_stamina(self):
        """Regenera stamina pasivamente"""
        if self.stamina_actual < self.stamina_maxima:
            self.stamina_actual = min(
                self.stamina_maxima,
                self.stamina_actual + CombatConfig.REGENERACION_STAMINA
            )