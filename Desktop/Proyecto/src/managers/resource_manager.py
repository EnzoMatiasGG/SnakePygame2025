"""
Gestor de recursos del juego.
Centraliza la carga de sprites, imágenes y datos de personajes.
"""
import pygame
from typing import Dict, List, Tuple
from src.utils.helpers import cargar_imagen_con_alpha, cargar_imagen_con_colorkey
from src.utils.config import SpriteConfig


class ResourceManager:
    """Gestor centralizado de recursos del juego"""
    
    def __init__(self):
        """Inicializa el gestor de recursos"""
        self.sprites_personajes: Dict = {}
        self.personajes_data: List[Dict] = []
        self.mapas_data: List[Dict] = []
        
    def cargar_todos_los_recursos(self) -> Tuple[Dict, List, List]:
        """
        Carga todos los recursos del juego.
        
        Returns:
            Tuple: (sprites_personajes, personajes_data, mapas_data)
        """
        self._cargar_sprites_personajes()
        self._cargar_datos_personajes()
        self._cargar_datos_mapas()
        
        return self.sprites_personajes, self.personajes_data, self.mapas_data
    
    def _cargar_sprites_personajes(self):
        """Carga todos los sprites de personajes"""
        self.sprites_personajes = {
            'goku': self._cargar_sprites_goku(),
            'vegeta': self._cargar_sprites_vegeta(),
            'freezer': self._cargar_sprites_freezer(),
            'gohan': self._cargar_sprites_gohan(),
        }
    
    def _cargar_sprites_goku(self) -> Dict:
        """Carga sprites de Goku"""
        return {
            'derecha': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_avanza.png"),
            'izquierda': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_retrocede.png"),
            'bajar': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_baja.png"),
            'inicio': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_base.png"),
            'golpe_j': [
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_golpe_puño_derecho.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_golpe_puño_izquierdo.png"),
            ],
            'patada_k': [
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_2.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_3.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_4.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_5.png"),
            ],
            'cubrirse': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_cubrirse.png"),
            'bola_energia': [
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_bola_energia_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_bola_energia_2.png"),
            ],
            'poder_ligero': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_bola.png"),
            'kamehameha': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_kamehameha.png"),
            'kamehameha_poder': [
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Kamehameha_inicio.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Kamehameha_cuerpo.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Kamehameha_final.png"),
            ],
            'genki_pose': [
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_2.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_3.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_4.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_5.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_6.png"),
            ],
            'genkidama': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genkidama.png"),
            'aturdido': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_aturdido.png"),
            'ko': [
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_KO_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_KO_2.png"),
            ],
        }
    
    def _cargar_sprites_vegeta(self) -> Dict:
        """Carga sprites de Vegeta"""
        return {
            'derecha': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_avanza.png"),
            'izquierda': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_retrocede.png"),
            'bajar': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_baja.png"),
            'subir': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_sube.png"),
            'inicio': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_base.png"),
            'golpe_j': [
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_golpe_puño_derecho.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_golpe_puño_izquierdo.png"),
            ],
            'patada_k': [
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_patada_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_patada_2.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_patada_3.png"),
            ],
            'cubrirse': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_cubrirse.png"),
            'bola_energia': [
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_bola_energia_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_bola_energia_2.png"),
            ],
            'poder_ligero': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_bola.png"),
            'galick_gun': [
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_2.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_3.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_4.png"),
            ],
            'galick_gun_poder': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/galick_gun_final.png"),
            'aturdido': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_aturdido.png"),
            'ko': [
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_KO_1.png"),
                cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_KO_2.png"),
            ],
        }
    
    def _cargar_sprites_freezer(self) -> Dict:
        """Carga sprites de Freezer"""
        return {
            'derecha': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_avanza.png"),
            'izquierda': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_retrocede.png"),
            'subir': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_sube-baja.png"),
            'bajar': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_sube-baja.png"),
            'inicio': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_inicio.png"),
            'golpe_j': [
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_golpe_puño_izquierdo.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_golpe_puño_derecho.png"),
            ],
            'patada_k': [
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_patada.png")
            ],
            'cubrirse': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_cubrirse.png"),
            'poder_ligero': cargar_imagen_con_alpha("Assets/Sprites/Freezer_1/Freezer_bola.png"),
            'bola_energia': [
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_bola_energia.png")
            ],
            'kamehameha': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_kamehameha.png"),
            'kamehameha_poder': [
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_kamehameha_inico.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_kamehameha_final.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_kamehameha_inico.png"),
            ],
            'Ulti': [
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_Ulti_1.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_Ulti_2.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_Ulti_3.png"),
            ],
            'Ulti_poder': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Bola_maligna.png"),
            'aturdido': cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_aturdido.png"),
            'ko': [
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_KO_1.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/Freezer_1/Freezer1_KO_2.png"),
            ],
        }
    
    def _cargar_sprites_gohan(self) -> Dict:
        """Carga sprites de Gohan"""
        return {
            'derecha': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_avanza.png"),
            'izquierda': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_retrocede.png"),
            'bajar': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_sube-baja.png"),
            'inicio': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_inicio.png"),
            'golpe_j': [
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_puño_izquierdo.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_puño_derecho.png"),
            ],
            'patada_k': [
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_1.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_2.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_3.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_4.png"),
            ],
            'cubrirse': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_cubrirse.png"),
            'poder_ligero': cargar_imagen_con_alpha("Assets/Sprites/GohanSSJ_1/Goku_bola.png"),
            'bola_energia': [
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_bola_energia_1.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_bola_energia_2.png"),
            ],
            'kamehameha': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_kamehameha.png"),
            'kamehameha_poder': [
                cargar_imagen_con_alpha("Assets/Sprites/GohanSSJ_1/kamehameha_inicio.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/kamehameha_cuerpo.png"),
                cargar_imagen_con_alpha("Assets/Sprites/GohanSSJ_1/kamehameha_final.png"),
            ],
            'masenko': [
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_masenko_1.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_masenko_2.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_masenko_3.png"),
            ],
            'masenko_poder': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/Masenko.png"),
            'aturdido': cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_aturdido.png"),
            'ko': [
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_KO_1.png"),
                cargar_imagen_con_colorkey("Assets/Sprites/GohanSSJ_1/GohankidSSJ_KO_2.png"),
            ],
        }
    
    def _cargar_datos_personajes(self):
        """Carga la información de los personajes"""
        self.personajes_data = [
            {
                "id": "goku",
                "nombre": "Goku",
                "foto_seleccion": "Assets/Sprites/Goku/Goku_seleccion.png",
                "lore": "Un saiyajin criado en la Tierra, defensor incansable de sus seres queridos."
            },
            {
                "id": "vegeta",
                "nombre": "Vegeta",
                "foto_seleccion": "Assets/Sprites/Vegeta_1/Vegeta_seleccion.png",
                "lore": "Príncipe de los saiyajines, inicialmente un rival feroz de Goku, luego un aliado valioso."
            },
            {
                "id": "freezer",
                "nombre": "Freezer",
                "foto_seleccion": "Assets/Sprites/Freezer_1/Freezer1_seleccion.png",
                "lore": "Conquistador del universo y rival mortal de Goku y los guerreros Z."
            },
            {
                "id": "gohan",
                "nombre": "Gohan",
                "foto_seleccion": "Assets/Sprites/GohanSSJ_1/GohankidSSJ_seleccion.png",
                "lore": "Hijo mayor de Goku, combina gran poder con un corazón noble."
            },
        ]
    
    def _cargar_datos_mapas(self):
        """Carga la información de los mapas"""
        self.mapas_data = [
            {"nombre": "Arena Mario", "ruta": "Fondos/Fondo_Mario.jpg"},
            {"nombre": "Artes Marciales", "ruta": "Fondos/Fondo_torneo.jpg"},
            {"nombre": "Planeta Namek", "ruta": "Fondos/Fondo_Namek.png"},
            {"nombre": "StreetFighter 2", "ruta": "Fondos/Fondo_ST2_Ryu.jpg"},
            {"nombre": "Google Dino", "ruta": "Fondos/Fondo_Dino_Google.jpg"},
            {"nombre": "Ruinas", "ruta": "Fondos/Fondo_ruinas.png"}
        ]