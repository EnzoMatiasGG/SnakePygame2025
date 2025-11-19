"""
Sistema de menús del juego.
Maneja todos los menús: principal, selección, récords, etc.
"""
import pygame
import sys
from typing import Optional, List, Dict, Tuple
from src.utils.config import (
    ANCHO, ALTO, NARANJA, AMARILLO, NEGRO, FPS_MENU, BLANCO, ROJO, VERDE,
    Paths
)
from src.utils.helpers import cargar_fuente, crear_overlay, parpadeo
from src.managers.audio_manager import AudioManager
from src.managers.records_manager import RecordsManager


class MenuManager:
    """Gestor de todos los menús del juego"""
    
    def __init__(self, pantalla: pygame.Surface, reloj: pygame.time.Clock,
                 personajes_data: List[Dict], mapas_data: List[Dict],
                 audio_manager: AudioManager):
        """
        Inicializa el gestor de menús.
        
        Args:
            pantalla: Surface de pygame
            reloj: Clock de pygame
            personajes_data: Lista con datos de personajes
            mapas_data: Lista con datos de mapas
            audio_manager: Gestor de audio
        """
        self.pantalla = pantalla
        self.reloj = reloj
        self.personajes_data = personajes_data
        self.mapas_data = mapas_data
        self.audio_manager = audio_manager
        
        # Cargar recursos
        self._cargar_recursos()
        
        # Estado del menú
        self.opciones_menu = ["Jugar", "Personajes", "Records", "Salir"]
        self.seleccion_menu = 0
    
    def _cargar_recursos(self):
        """Carga los recursos del menú"""
        # Fondo
        try:
            self.fondo_start = pygame.image.load(Paths.FONDO_START).convert()
            self.fondo_start = pygame.transform.scale(self.fondo_start, (ANCHO, ALTO))
        except:
            self.fondo_start = None
        
        try:
            self.fondo_nubes = pygame.image.load(Paths.FONDO_NUBES).convert()
            self.fondo_nubes = pygame.transform.scale(self.fondo_nubes, (ANCHO, ALTO))
        except:
            self.fondo_nubes = None
        
        # Imágenes especiales
        try:
            self.logo_info = pygame.image.load(Paths.LOGO_INFO).convert_alpha()
        except:
            self.logo_info = None
        
        try:
            self.meme_img = pygame.image.load(Paths.MEME).convert()
            self.meme_img = pygame.transform.scale(self.meme_img, (120, 120))
        except:
            self.meme_img = None
        
        # Fuentes
        self.fuente_grande = cargar_fuente(Paths.FUENTE_PRINCIPAL, 24)
        self.fuente_media = cargar_fuente(Paths.FUENTE_PRINCIPAL, 18)
        self.fuente_pequena = cargar_fuente(Paths.FUENTE_PRINCIPAL, 12)
    
    # ========================================================================
    # MENÚ PRINCIPAL
    # ========================================================================
    
    def start_menu(self):
        """Pantalla inicial del juego"""
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    if evento.key == pygame.K_RETURN:
                        return
            
            if self.fondo_start:
                self.pantalla.blit(self.fondo_start, (0, 0))
            else:
                self.pantalla.fill(NEGRO)
            
            # Texto parpadeante
            if parpadeo(pygame.time.get_ticks()):
                info = self.fuente_media.render("Presiona ENTER para comenzar", True, NARANJA)
                rect_info = info.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
                self.pantalla.blit(info, rect_info)
            
            pygame.display.flip()
            self.reloj.tick(FPS_MENU)
    
    def menu_principal(self) -> str:
        """
        Loop del menú principal.
        
        Returns:
            str: Opción seleccionada
        """
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    
                    if evento.key == pygame.K_UP:
                        self.seleccion_menu = (self.seleccion_menu - 1) % len(self.opciones_menu)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_DOWN:
                        self.seleccion_menu = (self.seleccion_menu + 1) % len(self.opciones_menu)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_RETURN:
                        return self.opciones_menu[self.seleccion_menu]
            
            self._dibujar_menu_principal()
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_menu_principal(self):
        """Dibuja el menú principal"""
        if self.fondo_start:
            self.pantalla.blit(self.fondo_start, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        # Overlay oscuro
        overlay = crear_overlay(ANCHO, ALTO, (0, 0, 0), 120)
        self.pantalla.blit(overlay, (0, 0))
        
        # Opciones
        y_inicial = ALTO * 0.55
        espacio = 60
        
        for i, opcion in enumerate(self.opciones_menu):
            color = AMARILLO if i == self.seleccion_menu else NARANJA
            texto = self.fuente_grande.render(opcion, True, color)
            rect_texto = texto.get_rect(center=(ANCHO // 2, int(y_inicial + i * espacio)))
            self.pantalla.blit(texto, rect_texto)
        
        pygame.display.flip()
    
    # ========================================================================
    # MENÚ DE MODO DE JUEGO
    # ========================================================================
    
    def menu_modo_juego(self) -> str:
        """
        Menú para elegir modo de juego.
        
        Returns:
            str: Modo seleccionado o "Volver"
        """
        opciones = ["Pelea Rapida", "Modo Torre", "Volver"]
        seleccion = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_RETURN:
                        return opciones[seleccion]
                    elif evento.key == pygame.K_ESCAPE:
                        return "Volver"
            
            self._dibujar_menu_modo_juego(opciones, seleccion)
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_menu_modo_juego(self, opciones: List[str], seleccion: int):
        """Dibuja el menú de modo de juego"""
        if self.fondo_start:
            self.pantalla.blit(self.fondo_start, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        overlay = crear_overlay(ANCHO, ALTO, (0, 0, 0), 150)
        self.pantalla.blit(overlay, (0, 0))
        
        titulo = self.fuente_grande.render("MODO DE JUEGO", True, AMARILLO)
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))
        
        y_inicial = 280
        for i, opcion in enumerate(opciones):
            color = AMARILLO if i == seleccion else NARANJA
            texto = self.fuente_grande.render(opcion, True, color)
            self.pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, y_inicial + i * 70))
        
        pygame.display.flip()
    
    # ========================================================================
    # MENÚ DE SELECCIÓN DE DIFICULTAD
    # ========================================================================
    
    def menu_seleccion_dificultad(self) -> Optional[str]:
        """
        Menú para seleccionar dificultad.
        
        Returns:
            Optional[str]: Dificultad seleccionada o None
        """
        dificultades = [
            {"nombre": "FACIL", "descripcion": "Para principiantes", "color": VERDE},
            {"nombre": "NORMAL", "descripcion": "Desafio equilibrado", "color": AMARILLO},
            {"nombre": "DIFICIL", "descripcion": "Solo para expertos", "color": ROJO}
        ]
        seleccion = 1  # Empezar en Normal
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    
                    if evento.key in [pygame.K_UP, pygame.K_LEFT]:
                        seleccion = (seleccion - 1) % len(dificultades)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                        seleccion = (seleccion + 1) % len(dificultades)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_RETURN:
                        return dificultades[seleccion]["nombre"].lower()
                    elif evento.key == pygame.K_ESCAPE:
                        return None
            
            self._dibujar_menu_dificultad(dificultades, seleccion)
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_menu_dificultad(self, dificultades: List[Dict], seleccion: int):
        """Dibuja el menú de dificultad"""
        if self.fondo_start:
            self.pantalla.blit(self.fondo_start, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        overlay = crear_overlay(ANCHO, ALTO, (0, 0, 0), 150)
        self.pantalla.blit(overlay, (0, 0))
        
        titulo = self.fuente_grande.render("SELECCIONA DIFICULTAD", True, AMARILLO)
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 80))
        
        y_inicial = 200
        espacio_y = 120
        
        for i, dif in enumerate(dificultades):
            y_pos = y_inicial + i * espacio_y
            
            if i == seleccion:
                rect_fondo = pygame.Rect(ANCHO // 2 - 200, y_pos - 10, 400, 90)
                pygame.draw.rect(self.pantalla, dif["color"], rect_fondo, 4)
                pygame.draw.rect(self.pantalla, (0, 0, 0), rect_fondo.inflate(-8, -8))
            
            color_nombre = dif["color"] if i == seleccion else BLANCO
            nombre = self.fuente_grande.render(dif["nombre"], True, color_nombre)
            self.pantalla.blit(nombre, (ANCHO // 2 - nombre.get_width() // 2, y_pos))
            
            color_desc = BLANCO if i == seleccion else (150, 150, 150)
            desc = self.fuente_pequena.render(dif["descripcion"], True, color_desc)
            self.pantalla.blit(desc, (ANCHO // 2 - desc.get_width() // 2, y_pos + 35))
            
            if i == seleccion:
                indicador_izq = self.fuente_media.render(">", True, dif["color"])
                indicador_der = self.fuente_media.render("<", True, dif["color"])
                self.pantalla.blit(indicador_izq, (ANCHO // 2 - 220, y_pos + 5))
                self.pantalla.blit(indicador_der, (ANCHO // 2 + 200, y_pos + 5))
        
        instrucciones = self.fuente_pequena.render(
            "↑↓ o ←→ para navegar | ENTER para elegir | ESC para volver",
            True, NARANJA
        )
        self.pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 50))
        
        pygame.display.flip()
    
    # ========================================================================
    # MENÚ DE SELECCIÓN DE PERSONAJE
    # ========================================================================
    
    def menu_seleccion_personaje(self, jugador_num: int = 1) -> Optional[str]:
        """
        Menú de selección de personaje.
        
        Args:
            jugador_num: Número de jugador (1 o 2)
            
        Returns:
            Optional[str]: ID del personaje o None
        """
        seleccion = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    
                    if evento.key == pygame.K_LEFT:
                        seleccion = (seleccion - 1) % len(self.personajes_data)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_RIGHT:
                        seleccion = (seleccion + 1) % len(self.personajes_data)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_RETURN:
                        return self.personajes_data[seleccion]["id"]
                    elif evento.key == pygame.K_ESCAPE:
                        return None
            
            self._dibujar_menu_personajes(seleccion, jugador_num)
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_menu_personajes(self, seleccion: int, jugador_num: int):
        """Dibuja el menú de selección de personajes"""
        self.pantalla.fill((10, 10, 30))
        
        if jugador_num == 2:
            titulo = self.fuente_grande.render("Elige tu rival", True, AMARILLO)
        else:
            titulo = self.fuente_grande.render(
                f"JUGADOR {jugador_num} - Elige tu personaje",
                True, AMARILLO
            )
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
        
        cols = 4
        espacio_x = ANCHO // (cols + 1)
        espacio_y = 150
        inicio_y = 150
        
        for i, pj in enumerate(self.personajes_data):
            col = i % cols
            fila = i // cols
            x = espacio_x * (col + 1) - 60
            y = inicio_y + fila * espacio_y
            
            try:
                imagen = pygame.image.load(pj["foto_seleccion"]).convert()
                imagen.set_colorkey((255, 255, 255))
                imagen = pygame.transform.scale(imagen, (120, 120))
                
                if i == seleccion:
                    pygame.draw.rect(self.pantalla, AMARILLO, (x - 5, y - 5, 130, 130), 3)
                
                self.pantalla.blit(imagen, (x, y))
                
                color_texto = AMARILLO if i == seleccion else BLANCO
                nombre = self.fuente_media.render(pj["nombre"], True, color_texto)
                self.pantalla.blit(nombre, (x + 60 - nombre.get_width() // 2, y + 130))
            except:
                pass
        
        instrucciones = self.fuente_pequena.render(
            "← → para navegar | ENTER para elegir | ESC para volver",
            True, NARANJA
        )
        self.pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 40))
        
        pygame.display.flip()
    
    # ========================================================================
    # MENÚ DE SELECCIÓN DE MAPA
    # ========================================================================
    
    def menu_seleccion_mapa(self) -> Optional[str]:
        """
        Menú de selección de mapa.
        
        Returns:
            Optional[str]: Ruta del mapa o None
        """
        seleccion = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    
                    if evento.key == pygame.K_LEFT:
                        seleccion = (seleccion - 1) % len(self.mapas_data)
                    elif evento.key == pygame.K_RIGHT:
                        seleccion = (seleccion + 1) % len(self.mapas_data)
                    elif evento.key == pygame.K_RETURN:
                        return self.mapas_data[seleccion]["ruta"]
                    elif evento.key == pygame.K_ESCAPE:
                        return None
            
            self._dibujar_menu_mapas(seleccion)
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_menu_mapas(self, seleccion: int):
        """Dibuja el menú de selección de mapas"""
        self.pantalla.fill((10, 10, 30))
        
        titulo = self.fuente_grande.render("Elige el escenario", True, AMARILLO)
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
        
        cols = 3
        espacio_x = ANCHO // (cols + 1)
        espacio_y = 180
        inicio_y = 150
        
        for i, mapa in enumerate(self.mapas_data):
            col = i % cols
            fila = i // cols
            x = espacio_x * (col + 1) - 80
            y = inicio_y + fila * espacio_y
            
            try:
                preview = pygame.image.load(mapa["ruta"]).convert()
                preview = pygame.transform.scale(preview, (160, 120))
                
                if i == seleccion:
                    pygame.draw.rect(self.pantalla, AMARILLO, (x - 5, y - 5, 170, 130), 3)
                
                self.pantalla.blit(preview, (x, y))
                
                color_texto = AMARILLO if i == seleccion else BLANCO
                nombre = self.fuente_pequena.render(mapa["nombre"], True, color_texto)
                self.pantalla.blit(nombre, (x + 80 - nombre.get_width() // 2, y + 135))
            except:
                pygame.draw.rect(self.pantalla, (50, 50, 50), (x, y, 160, 120))
                nombre = self.fuente_pequena.render(mapa["nombre"], True, BLANCO)
                self.pantalla.blit(nombre, (x + 80 - nombre.get_width() // 2, y + 60))
        
        instrucciones = self.fuente_pequena.render(
            "← → para navegar | ENTER para elegir | ESC para volver",
            True, NARANJA
        )
        self.pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 40))
        
        pygame.display.flip()
    
    # ========================================================================
    # MENÚ DE PERSONAJES (INFO)
    # ========================================================================
    
    def menu_personajes(self):
        """Menú de información de personajes"""
        seleccion = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(self.personajes_data)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(self.personajes_data)
                    elif evento.key == pygame.K_RETURN:
                        self.mostrar_lore_personaje(seleccion)
                    elif evento.key == pygame.K_ESCAPE:
                        return
            
            self._dibujar_menu_info_personajes(seleccion)
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_menu_info_personajes(self, seleccion: int):
        """Dibuja el menú de información de personajes"""
        if self.fondo_nubes:
            self.pantalla.blit(self.fondo_nubes, (0, 0))
        else:
            self.pantalla.fill((10, 10, 30))
        
        if self.logo_info:
            logo_rect = self.logo_info.get_rect(center=(ANCHO // 2, 80))
            self.pantalla.blit(self.logo_info, logo_rect)
        
        for i, pj in enumerate(self.personajes_data):
            color = AMARILLO if i == seleccion else NARANJA
            texto = self.fuente_grande.render(pj["nombre"], True, color)
            rect_texto = texto.get_rect(center=(ANCHO // 2, 200 + i * 60))
            self.pantalla.blit(texto, rect_texto)
        
        boton_rect = pygame.Rect(ANCHO // 2 - 95, ALTO - 80, 190, 40)
        pygame.draw.rect(self.pantalla, NARANJA, boton_rect)
        texto_boton = self.fuente_pequena.render("ESC para volver", True, NEGRO)
        rect_texto_boton = texto_boton.get_rect(center=boton_rect.center)
        self.pantalla.blit(texto_boton, rect_texto_boton)
        
        pygame.display.flip()
    
    def mostrar_lore_personaje(self, indice: int):
        """Muestra el lore de un personaje"""
        pj = self.personajes_data[indice]
        
        try:
            imagen = pygame.image.load(pj["foto_seleccion"]).convert()
            imagen.set_colorkey((255, 255, 255))
            imagen = pygame.transform.scale(imagen, (120, 120))
        except:
            imagen = None
        
        boton_rect = pygame.Rect(ANCHO - 180, ALTO - 80, 150, 50)
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_controles_volumen(evento.key)
                    if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        return
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_rect.collidepoint(evento.pos):
                        return
            
            self.pantalla.fill((20, 20, 30))
            
            if imagen:
                self.pantalla.blit(imagen, (ANCHO // 2 - 60, 50))
            
            nombre = self.fuente_grande.render(pj["nombre"], True, AMARILLO)
            self.pantalla.blit(nombre, (ANCHO // 2 - nombre.get_width() // 2, 180))
            
            lore_texto = pj.get("lore", "")
            y_lore = 230
            max_len = 46
            
            while lore_texto:
                linea = lore_texto[:max_len]
                lore_render = self.fuente_pequena.render(linea, True, BLANCO)
                self.pantalla.blit(lore_render, (ANCHO // 2 - lore_render.get_width() // 2, y_lore))
                y_lore += 28
                lore_texto = lore_texto[max_len:]
            
            if self.meme_img:
                meme_x = (ANCHO // 2) - (self.meme_img.get_width() // 2)
                meme_y = ALTO - self.meme_img.get_height() - 90
                self.pantalla.blit(self.meme_img, (meme_x, meme_y))
            
            pygame.draw.rect(self.pantalla, AMARILLO, boton_rect)
            boton_texto = self.fuente_grande.render("Volver", True, NEGRO)
            rect_boton = boton_texto.get_rect(center=boton_rect.center)
            self.pantalla.blit(boton_texto, rect_boton)
            
            pygame.display.flip()
            self.reloj.tick(FPS_MENU)
    
    # ========================================================================
    # MENÚ DE RÉCORDS
    # ========================================================================
    
    def menu_records(self):
        """Menú de récords"""
        opciones = ["Records 1vs1", "Records Torre", "Volver"]
        seleccion = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                        self.audio_manager.reproducir_sonido('cursor')
                    elif evento.key == pygame.K_RETURN:
                        if opciones[seleccion] == "Records 1vs1":
                            self.mostrar_records_1vs1()
                        elif opciones[seleccion] == "Records Torre":
                            self.mostrar_records_torre()
                        elif opciones[seleccion] == "Volver":
                            return
                    elif evento.key == pygame.K_ESCAPE:
                        return
            
            self._dibujar_menu_records(opciones, seleccion)
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_menu_records(self, opciones: List[str], seleccion: int):
        """Dibuja el menú de récords"""
        self.pantalla.fill((10, 10, 30))
        
        titulo = self.fuente_grande.render("RECORDS", True, AMARILLO)
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))
        
        y_inicial = 220
        for i, opcion in enumerate(opciones):
            color = AMARILLO if i == seleccion else NARANJA
            texto = self.fuente_grande.render(opcion, True, color)
            self.pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, y_inicial + i * 70))
        
        pygame.display.flip()
    
    def mostrar_records_1vs1(self):
        """Muestra los récords 1vs1"""
        records_manager = RecordsManager()
        records = records_manager.obtener_top_records_1vs1(8)
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                        return
            
            self._dibujar_tabla_records(records, "RECORDS 1vs1", es_torre=False)
            self.reloj.tick(FPS_MENU)
    
    def mostrar_records_torre(self):
        """Muestra los récords de torre"""
        records_manager = RecordsManager()
        records = records_manager.obtener_top_records_torre(8)
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                        return
            
            self._dibujar_tabla_records(records, "RECORDS TORRE", es_torre=True)
            self.reloj.tick(FPS_MENU)
    
    def _dibujar_tabla_records(self, records: List[Dict], titulo: str, es_torre: bool):
        """Dibuja la tabla de récords"""
        self.pantalla.fill((10, 10, 30))
        
        titulo_render = self.fuente_grande.render(titulo, True, AMARILLO)
        self.pantalla.blit(titulo_render, (ANCHO // 2 - titulo_render.get_width() // 2, 30))
        
        if len(records) == 0:
            texto = self.fuente_media.render("No hay records aun", True, BLANCO)
            self.pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
        else:
            # Encabezados
            y = 100
            self.pantalla.blit(self.fuente_pequena.render("#", True, NARANJA), (50, y))
            self.pantalla.blit(self.fuente_pequena.render("NOMBRE", True, NARANJA), (100, y))
            self.pantalla.blit(self.fuente_pequena.render("PUNTAJE", True, NARANJA), (220, y))
            
            if es_torre:
                self.pantalla.blit(self.fuente_pequena.render("NIVEL", True, NARANJA), (340, y))
            else:
                self.pantalla.blit(self.fuente_pequena.render("ROUNDS", True, NARANJA), (340, y))
            
            self.pantalla.blit(self.fuente_pequena.render("GOLPES", True, NARANJA), (450, y))
            self.pantalla.blit(self.fuente_pequena.render("TIEMPO", True, NARANJA), (570, y))
            
            # Récords
            y = 140
            for i, record in enumerate(records):
                if i == 0:
                    color = (255, 215, 0)  # Oro
                elif i == 1:
                    color = (192, 192, 192)  # Plata
                elif i == 2:
                    color = (205, 127, 50)  # Bronce
                else:
                    color = BLANCO
                
                self.pantalla.blit(self.fuente_pequena.render(f"{i+1}", True, color), (50, y))
                self.pantalla.blit(self.fuente_pequena.render(record['nombre'], True, color), (100, y))
                self.pantalla.blit(self.fuente_pequena.render(str(record['puntaje']), True, color), (220, y))
                
                if es_torre:
                    nivel_txt = f"{record['peleas_ganadas']}/3"
                    self.pantalla.blit(self.fuente_pequena.render(nivel_txt, True, color), (340, y))
                else:
                    rounds_txt = f"{record['rounds_ganados']}-{record['rounds_perdidos']}"
                    self.pantalla.blit(self.fuente_pequena.render(rounds_txt, True, color), (340, y))
                
                self.pantalla.blit(self.fuente_pequena.render(str(record['golpes_totales']), True, color), (450, y))
                
                mins = record['tiempo_segundos'] // 60
                secs = record['tiempo_segundos'] % 60
                self.pantalla.blit(self.fuente_pequena.render(f"{mins}:{secs:02d}", True, color), (570, y))
                
                y += 50
        
        instrucciones = self.fuente_pequena.render("ESC o ENTER para volver", True, NARANJA)
        self.pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 40))
        
        pygame.display.flip()
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def _manejar_controles_volumen(self, tecla: int):
        """Maneja los controles de volumen"""
        if tecla in [pygame.K_MINUS, pygame.K_KP_MINUS]:
            self.audio_manager.bajar_volumen()
        elif tecla in [pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS]:
            self.audio_manager.subir_volumen()