"""
Sistema de Inteligencia Artificial.
Controla el comportamiento de los oponentes controlados por la CPU.
"""
import pygame
import random
from typing import Literal
from src.entities.player import Player
from src.utils.config import ANCHO, ALTO, IAConfig


DificultadType = Literal['facil', 'normal', 'dificil']


class AIController:
    """Controlador de IA para oponentes"""
    
    def __init__(self, jugador_ia: Player, jugador_oponente: Player, 
                 dificultad: DificultadType = 'normal'):
        """
        Inicializa el controlador de IA.
        
        Args:
            jugador_ia: Jugador controlado por la IA
            jugador_oponente: Jugador humano (oponente)
            dificultad: Nivel de dificultad ('facil', 'normal', 'dificil')
        """
        self.jugador_ia = jugador_ia
        self.jugador_oponente = jugador_oponente
        self.dificultad = dificultad
        
        # Cargar configuración según dificultad
        self._cargar_configuracion(dificultad)
        
        # Estado interno
        self.ultimo_ataque = 0
        self.tiempo_entre_ataques = self.tiempo_reaccion
        self.modo_actual = "AGRESIVO"
        self.tiempo_cambio_modo = 0
        self.duracion_modo = 2000
        
        # Sistema anti-bloqueo
        self.ultima_posicion_x = jugador_ia.x
        self.ultima_posicion_y = jugador_ia.y
        self.tiempo_sin_mover = 0
        self.ultima_verificacion = 0
        self.contador_emergencias = 0
    
    def _cargar_configuracion(self, dificultad: DificultadType):
        """Carga la configuración según la dificultad"""
        if dificultad == 'facil':
            config = IAConfig.FACIL
        elif dificultad == 'normal':
            config = IAConfig.NORMAL
        else:  # dificil
            config = IAConfig.DIFICIL
        
        self.velocidad = config['velocidad']
        self.tiempo_reaccion = config['tiempo_reaccion']
        self.probabilidad_ataque = config['prob_ataque']
        self.probabilidad_defensa = config['prob_defensa']
        self.probabilidad_especial = config['prob_especial']
        self.distancia_ataque = config['distancia_ataque']
        self.distancia_minima = config['distancia_minima']
    
    def actualizar(self):
        """Lógica principal de la IA"""
        ahora = pygame.time.get_ticks()
        
        # Verificar estados bloqueantes
        if self._esta_bloqueado():
            return
        
        # Forzar dejar de cubrirse después de un tiempo
        if self.jugador_ia.cubriendose and ahora - self.ultimo_ataque > 500:
            self.jugador_ia.dejar_de_cubrirse()
        
        # Sistema anti-bloqueo
        self._verificar_bloqueo(ahora)
        
        # Cambiar modo periódicamente
        if ahora - self.tiempo_cambio_modo > self.duracion_modo:
            self._cambiar_modo()
            self.tiempo_cambio_modo = ahora
        
        # Forzar acción si no ha atacado en mucho tiempo
        if ahora - self.ultimo_ataque > 2000:
            self._accion_emergencia(ahora)
            return
        
        # Calcular distancias
        distancia_x = abs(self.jugador_ia.x - self.jugador_oponente.x)
        distancia_y = abs(self.jugador_ia.y - self.jugador_oponente.y)
        
        # Evaluar situación y decidir
        self._evaluar_situacion(distancia_x, distancia_y, ahora)
    
    def _esta_bloqueado(self) -> bool:
        """Verifica si la IA está en un estado bloqueante"""
        return any([
            self.jugador_ia.golpe_animando,
            self.jugador_ia.lanzando_bola,
            self.jugador_ia.usando_kamehameha,
            self.jugador_ia.usando_movimiento_final,
            self.jugador_ia.aturdido,
            self.jugador_ia.en_ko
        ])
    
    def _verificar_bloqueo(self, ahora: int):
        """Sistema anti-bloqueo mejorado"""
        if ahora - self.ultima_verificacion > 150:
            distancia_movida = (
                abs(self.jugador_ia.x - self.ultima_posicion_x) +
                abs(self.jugador_ia.y - self.ultima_posicion_y)
            )
            
            if distancia_movida < 1:
                self.tiempo_sin_mover += 150
                
                if self.tiempo_sin_mover > 450:
                    self.contador_emergencias += 1
                    
                    if self.contador_emergencias > 5:
                        self._reseteo_total()
                    
                    self._accion_emergencia(ahora)
                    self.tiempo_sin_mover = 0
            else:
                self.tiempo_sin_mover = 0
                if self.contador_emergencias > 0:
                    self.contador_emergencias = max(0, self.contador_emergencias - 1)
            
            self.ultima_posicion_x = self.jugador_ia.x
            self.ultima_posicion_y = self.jugador_ia.y
            self.ultima_verificacion = ahora
    
    def _cambiar_modo(self):
        """Cambia el modo de juego de la IA"""
        vida_porcentaje = self.jugador_ia.vida_actual / self.jugador_ia.vida_maxima
        stamina_porcentaje = self.jugador_ia.stamina_actual / self.jugador_ia.stamina_maxima
        
        if stamina_porcentaje < 0.2:
            self.modo_actual = "NEUTRO"
        elif vida_porcentaje < 0.3:
            if self.dificultad == 'dificil':
                self.modo_actual = "AGRESIVO"
            else:
                self.modo_actual = random.choice(["AGRESIVO", "AGRESIVO", "NEUTRO"])
        else:
            self.modo_actual = random.choice(["AGRESIVO", "AGRESIVO", "NEUTRO"])
    
    def _evaluar_situacion(self, distancia_x: float, distancia_y: float, ahora: int):
        """Evalúa la situación y toma decisiones"""
        # Prioridad 1: Defender si el oponente está atacando muy cerca
        if self.jugador_oponente.golpe_animando and distancia_x < 80:
            if random.random() < self.probabilidad_defensa:
                self.jugador_ia.cubrirse()
                self.ultimo_ataque = ahora
                return
        
        # Prioridad 2: Retroceder o atacar si está muy cerca
        if distancia_x < self.distancia_minima:
            if random.random() < 0.3:
                self._alejarse_del_oponente()
            else:
                if ahora - self.ultimo_ataque > self.tiempo_entre_ataques:
                    self._decidir_ataque(ahora)
            return
        
        # Prioridad 3: Atacar si está en rango
        if distancia_x <= self.distancia_ataque and distancia_y < 60:
            if ahora - self.ultimo_ataque > self.tiempo_entre_ataques:
                self._decidir_ataque(ahora)
                return
            else:
                self._movimiento_lateral(distancia_y)
                return
        
        # Prioridad 4: Acercarse si está lejos
        if distancia_x > self.distancia_ataque:
            self._acercarse_al_oponente(distancia_x, distancia_y)
            return
        
        # Prioridad 5: Decidir según modo
        if self.modo_actual == "AGRESIVO":
            if ahora - self.ultimo_ataque > self.tiempo_entre_ataques:
                self._decidir_ataque(ahora)
            else:
                self._acercarse_al_oponente(distancia_x, distancia_y)
        elif self.modo_actual == "DEFENSIVO":
            if distancia_x < 70:
                self._alejarse_del_oponente()
            else:
                self._movimiento_lateral(distancia_y)
        else:  # NEUTRO
            if random.random() < 0.5:
                self._acercarse_al_oponente(distancia_x, distancia_y)
            else:
                self._movimiento_lateral(distancia_y)
    
    def _decidir_ataque(self, ahora: int):
        """Decide qué tipo de ataque usar"""
        if self.jugador_ia.stamina_actual < 10:
            distancia_x = abs(self.jugador_ia.x - self.jugador_oponente.x)
            distancia_y = abs(self.jugador_ia.y - self.jugador_oponente.y)
            self._acercarse_al_oponente(distancia_x, distancia_y)
            return
        
        # Ajustar probabilidad de especiales según vida
        vida_porcentaje = self.jugador_ia.vida_actual / self.jugador_ia.vida_maxima
        prob_especial = self.probabilidad_especial * (1.5 if vida_porcentaje < 0.3 else 1.0)
        
        probabilidad = random.random()
        
        # Ataque especial
        if probabilidad < prob_especial * 0.5:
            if self.jugador_ia.tiene_stamina(50) and random.random() < 0.4:
                self.jugador_ia.iniciar_kamehameha()
                self.ultimo_ataque = ahora
                self.tiempo_entre_ataques = random.randint(1500, 2500)
            elif self.jugador_ia.tiene_stamina(15):
                self.jugador_ia.iniciar_lanzar_bola()
                self.ultimo_ataque = ahora
                self.tiempo_entre_ataques = random.randint(800, 1200)
            else:
                self._ataque_cuerpo_a_cuerpo(ahora)
        
        # Movimiento final
        elif probabilidad < prob_especial and self.jugador_ia.tiene_stamina(80):
            if random.random() < 0.2:
                self.jugador_ia.iniciar_movimiento_final()
                self.ultimo_ataque = ahora
                self.tiempo_entre_ataques = random.randint(2000, 3000)
            else:
                self._ataque_cuerpo_a_cuerpo(ahora)
        
        # Ataque cuerpo a cuerpo
        else:
            self._ataque_cuerpo_a_cuerpo(ahora)
    
    def _ataque_cuerpo_a_cuerpo(self, ahora: int):
        """Ejecuta un ataque cuerpo a cuerpo"""
        if random.random() < 0.65:
            self.jugador_ia.iniciar_golpe('golpe_j')
            self.ultimo_ataque = ahora
            
            if self.dificultad == 'dificil':
                self.tiempo_entre_ataques = random.randint(100, 250)
            elif self.dificultad == 'normal':
                self.tiempo_entre_ataques = random.randint(200, 400)
            else:
                self.tiempo_entre_ataques = random.randint(300, 550)
        else:
            self.jugador_ia.iniciar_golpe('patada_k')
            self.ultimo_ataque = ahora
            
            if self.dificultad == 'dificil':
                self.tiempo_entre_ataques = random.randint(150, 350)
            elif self.dificultad == 'normal':
                self.tiempo_entre_ataques = random.randint(300, 550)
            else:
                self.tiempo_entre_ataques = random.randint(400, 750)
    
    def _acercarse_al_oponente(self, distancia_x: float, distancia_y: float):
        """Se acerca al oponente de forma inteligente"""
        # Movimiento horizontal
        if self.jugador_ia.x < self.jugador_oponente.x:
            self.jugador_ia.x += self.velocidad
            self.jugador_ia.estado = 'derecha' if self.jugador_ia.mirando_derecha else 'izquierda'
        else:
            self.jugador_ia.x -= self.velocidad
            self.jugador_ia.estado = 'izquierda' if self.jugador_ia.mirando_derecha else 'derecha'
        
        # Movimiento vertical (alinearse)
        if distancia_y > 40:
            if self.jugador_ia.y < self.jugador_oponente.y:
                self.jugador_ia.y += self.velocidad * 0.6
            else:
                self.jugador_ia.y -= self.velocidad * 0.6
        
        self.jugador_ia.sprite = self.jugador_ia.sprites[self.jugador_ia.estado]
        self._aplicar_limites()
    
    def _alejarse_del_oponente(self):
        """Se aleja del oponente"""
        if self.jugador_ia.x < self.jugador_oponente.x:
            self.jugador_ia.x -= self.velocidad * 1.2
            self.jugador_ia.estado = 'izquierda' if self.jugador_ia.mirando_derecha else 'derecha'
        else:
            self.jugador_ia.x += self.velocidad * 1.2
            self.jugador_ia.estado = 'derecha' if not self.jugador_ia.mirando_derecha else 'izquierda'
        
        self.jugador_ia.sprite = self.jugador_ia.sprites[self.jugador_ia.estado]
        self._aplicar_limites()
    
    def _movimiento_lateral(self, distancia_y: float):
        """Movimiento lateral para esquivar"""
        if distancia_y > 40:
            if self.jugador_ia.y < self.jugador_oponente.y:
                self.jugador_ia.y += self.velocidad * 0.8
                self.jugador_ia.estado = 'bajar'
            else:
                self.jugador_ia.y -= self.velocidad * 0.8
                self.jugador_ia.estado = 'subir' if 'subir' in self.jugador_ia.sprites else 'bajar'
            
            self.jugador_ia.sprite = self.jugador_ia.sprites[self.jugador_ia.estado]
        else:
            if random.random() < 0.5:
                if self.jugador_ia.x < self.jugador_oponente.x:
                    self.jugador_ia.x += self.velocidad * 0.3
                    self.jugador_ia.estado = 'derecha' if self.jugador_ia.mirando_derecha else 'izquierda'
                else:
                    self.jugador_ia.x -= self.velocidad * 0.3
                    self.jugador_ia.estado = 'izquierda' if self.jugador_ia.mirando_derecha else 'derecha'
                self.jugador_ia.sprite = self.jugador_ia.sprites[self.jugador_ia.estado]
            else:
                self.jugador_ia.estado = 'inicio'
                self.jugador_ia.sprite = self.jugador_ia.sprites['inicio']
        
        self._aplicar_limites()
    
    def _accion_emergencia(self, ahora: int):
        """Acción de emergencia cuando la IA se queda trabada"""
        distancia_x = abs(self.jugador_ia.x - self.jugador_oponente.x)
        
        # Movimiento agresivo forzado
        if distancia_x > 50:
            for _ in range(8):
                if self.jugador_ia.x < self.jugador_oponente.x:
                    self.jugador_ia.x += self.velocidad * 2
                    self.jugador_ia.estado = 'derecha' if self.jugador_ia.mirando_derecha else 'izquierda'
                else:
                    self.jugador_ia.x -= self.velocidad * 2
                    self.jugador_ia.estado = 'izquierda' if self.jugador_ia.mirando_derecha else 'derecha'
            
            self.jugador_ia.sprite = self.jugador_ia.sprites[self.jugador_ia.estado]
            self._aplicar_limites()
        
        # Atacar si tiene stamina
        if self.jugador_ia.tiene_stamina(5):
            if random.random() < 0.8:
                if random.random() < 0.7:
                    self.jugador_ia.iniciar_golpe('golpe_j')
                else:
                    self.jugador_ia.iniciar_golpe('patada_k')
                self.ultimo_ataque = ahora
                self.tiempo_entre_ataques = 100
            elif self.jugador_ia.tiene_stamina(15):
                self.jugador_ia.iniciar_lanzar_bola()
                self.ultimo_ataque = ahora
                self.tiempo_entre_ataques = 400
    
    def _reseteo_total(self):
        """Reseteo total cuando la IA está completamente trabada"""
        self.jugador_ia.cubriendose = False
        self.jugador_ia.golpe_animando = False
        self.jugador_ia.lanzando_bola = False
        self.contador_emergencias = 0
    
    def _aplicar_limites(self):
        """Asegura que el personaje no salga de pantalla"""
        ancho_sprite = self.jugador_ia.sprite.get_width()
        alto_sprite = self.jugador_ia.sprite.get_height()
        
        self.jugador_ia.x = max(0, min(self.jugador_ia.x, ANCHO - ancho_sprite))
        self.jugador_ia.y = max(0, min(self.jugador_ia.y, ALTO - alto_sprite))