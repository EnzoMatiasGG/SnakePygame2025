"""
Paquete de entidades del juego.
Exporta las clases principales de personajes y objetos.
"""
from src.entities.player import Player
from src.entities.proyectile import Projectile
from src.entities.special_moves import Kamehameha

__all__ = ['Player', 'Projectile', 'Kamehameha']