"""
Sistema de detección de colisiones.
Maneja todas las colisiones entre jugadores, ataques y proyectiles.
"""
from typing import Dict
from src.entities.player import Player


class CollisionSystem:
    """Sistema centralizado de detección de colisiones"""
    
    def __init__(self, jugador1: Player, jugador2: Player):
        """
        Inicializa el sistema de colisiones.
        
        Args:
            jugador1: Primer jugador
            jugador2: Segundo jugador
        """
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        
        # Estadísticas de combate
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
    
    def detectar_todas(self):
        """Detecta todas las colisiones del juego"""
        self._detectar_ataques_cuerpo_a_cuerpo()
        self._detectar_proyectiles()
        self._detectar_kamehamehas()
    
    def _detectar_ataques_cuerpo_a_cuerpo(self):
        """Detecta colisiones de ataques cuerpo a cuerpo"""
        # Jugador 1 -> Jugador 2
        if self.jugador1.hitbox_activa and self.jugador1.hitbox_ataque:
            if self.jugador1.hitbox_ataque.colliderect(self.jugador2.rect):
                dano = self.jugador1.obtener_dano_ataque()
                dano_real = self.jugador2.recibir_dano(dano)
                self.jugador1.hitbox_activa = False
                self.jugador2.recibir_golpe_combo()
                
                self._registrar_golpe(1, dano_real)
        
        # Jugador 2 -> Jugador 1
        if self.jugador2.hitbox_activa and self.jugador2.hitbox_ataque:
            if self.jugador2.hitbox_ataque.colliderect(self.jugador1.rect):
                dano = self.jugador2.obtener_dano_ataque()
                dano_real = self.jugador1.recibir_dano(dano)
                self.jugador2.hitbox_activa = False
                self.jugador1.recibir_golpe_combo()
                
                self._registrar_golpe(2, dano_real)
    
    def _detectar_proyectiles(self):
        """Detecta colisiones de proyectiles"""
        # Proyectiles J1 -> J2
        for bola in self.jugador1.bolas_activas[:]:
            if bola.rect.colliderect(self.jugador2.rect):
                # Usar el daño del proyectil (puede ser bola normal o movimiento final)
                dano = bola.obtener_dano()
                dano_real = self.jugador2.recibir_dano(dano)
                self.jugador1.bolas_activas.remove(bola)
                self._registrar_golpe(1, dano_real)
        
        # Proyectiles J2 -> J1
        for bola in self.jugador2.bolas_activas[:]:
            if bola.rect.colliderect(self.jugador1.rect):
                dano = bola.obtener_dano()
                dano_real = self.jugador1.recibir_dano(dano)
                self.jugador2.bolas_activas.remove(bola)
                self._registrar_golpe(2, dano_real)
    
    def _detectar_kamehamehas(self):
        """Detecta colisiones de Kamehamehas"""
        # Kamehameha J1 -> J2
        if self.jugador1.kamehameha_activo:
            hitboxes = self.jugador1.kamehameha_activo.obtener_hitboxes()
            for hitbox in hitboxes:
                if hitbox.colliderect(self.jugador2.rect):
                    dano_real = self.jugador2.recibir_dano(self.jugador1.dano_kamehameha)
                    self.jugador1.kamehameha_activo.marcar_impacto()
                    
                    # Registrar estadísticas solo una vez
                    if not hasattr(self.jugador1.kamehameha_activo, '_stats_registradas'):
                        self.stats_jugador1['dano_causado'] += dano_real
                        self.stats_jugador2['dano_recibido'] += dano_real
                        self.jugador1.kamehameha_activo._stats_registradas = True
                    break
        
        # Kamehameha J2 -> J1
        if self.jugador2.kamehameha_activo:
            hitboxes = self.jugador2.kamehameha_activo.obtener_hitboxes()
            for hitbox in hitboxes:
                if hitbox.colliderect(self.jugador1.rect):
                    dano_real = self.jugador1.recibir_dano(self.jugador2.dano_kamehameha)
                    self.jugador2.kamehameha_activo.marcar_impacto()
                    
                    if not hasattr(self.jugador2.kamehameha_activo, '_stats_registradas'):
                        self.stats_jugador2['dano_causado'] += dano_real
                        self.stats_jugador1['dano_recibido'] += dano_real
                        self.jugador2.kamehameha_activo._stats_registradas = True
                    break
    
    def _registrar_golpe(self, jugador_num: int, dano_real: float):
        """
        Registra un golpe en las estadísticas.
        
        Args:
            jugador_num: Número del jugador que atacó (1 o 2)
            dano_real: Daño real aplicado
        """
        if jugador_num == 1:
            self.stats_jugador1['golpes_totales'] += 1
            self.stats_jugador1['dano_causado'] += dano_real
            self.stats_jugador2['dano_recibido'] += dano_real
        else:
            self.stats_jugador2['golpes_totales'] += 1
            self.stats_jugador2['dano_causado'] += dano_real
            self.stats_jugador1['dano_recibido'] += dano_real
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene las estadísticas de combate.
        
        Returns:
            Dict: Diccionario con las estadísticas de ambos jugadores
        """
        return {
            'jugador1': self.stats_jugador1.copy(),
            'jugador2': self.stats_jugador2.copy()
        }
    
    def reiniciar_estadisticas(self):
        """Reinicia las estadísticas de combate"""
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