"""
Dragon Ball Z Fighting Game
Punto de entrada principal del juego.
"""
import pygame
import sys
from src.utils.config import ANCHO, ALTO, Paths
from src.managers.resource_manager import ResourceManager
from src.managers.audio_manager import AudioManager
from src.managers.tower_manager import TowerManager
from src.ui.menus import MenuManager
from src.core.game import GameEngine


def inicializar_pygame():
    """Inicializa pygame y configura la ventana"""
    pygame.init()
    
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Dragon Ball Z - Fighting Game")
    
    try:
        icono = pygame.image.load(Paths.ICONO_VENTANA)
        pygame.display.set_icon(icono)
    except:
        pass
    
    reloj = pygame.time.Clock()
    
    return pantalla, reloj


def main():
    """Función principal del juego"""
    # Inicializar
    pantalla, reloj = inicializar_pygame()
    
    # Cargar recursos
    print("Cargando recursos...")
    resource_manager = ResourceManager()
    sprites_personajes, personajes_data, mapas_data = resource_manager.cargar_todos_los_recursos()
    print("Recursos cargados exitosamente")
    
    # Inicializar gestores
    audio_manager = AudioManager()
    audio_manager.reproducir_musica_menu()
    
    menu_manager = MenuManager(pantalla, reloj, personajes_data, mapas_data, audio_manager)
    
    # Pantalla de inicio
    menu_manager.start_menu()
    
    # Loop principal del menú
    while True:
        opcion = menu_manager.menu_principal()
        
        if opcion == "Salir":
            pygame.quit()
            sys.exit()
        
        elif opcion == "Jugar":
            modo = menu_manager.menu_modo_juego()
            
            if modo == "Volver":
                continue
            
            elif modo == "Pelea Rapida":
                # Seleccionar dificultad
                dificultad = menu_manager.menu_seleccion_dificultad()
                if dificultad is None:
                    continue
                
                # Seleccionar personaje
                personaje1 = menu_manager.menu_seleccion_personaje(1)
                if personaje1 is None:
                    continue
                
                # Seleccionar mapa
                mapa_seleccionado = menu_manager.menu_seleccion_mapa()
                if mapa_seleccionado is None:
                    continue
                
                # Oponente fijo (IA)
                personaje2 = 'freezer'
                
                # Crear y ejecutar juego
                juego = GameEngine(
                    pantalla, reloj,
                    sprites_personajes,
                    mapa_seleccionado,
                    personaje1,
                    personaje2,
                    es_modo_torre=False,
                    audio_manager=audio_manager
                )
                juego.dificultad_1vs1 = dificultad
                juego.ejecutar(personaje1, personaje2)
            
            elif modo == "Modo Torre":
                # Seleccionar personaje
                personaje1 = menu_manager.menu_seleccion_personaje(1)
                if personaje1 is None:
                    continue
                
                # Seleccionar mapa
                mapa_seleccionado = menu_manager.menu_seleccion_mapa()
                if mapa_seleccionado is None:
                    continue
                
                # Iniciar torre
                torre_manager = TowerManager(pantalla, reloj, personajes_data)
                torre_manager.iniciar_torre(personaje1)
                
                if not torre_manager.mostrar_pantalla_torre():
                    continue
                
                # Loop de la torre
                torre_abandonada = False
                while not torre_manager.esta_completada() and not torre_abandonada:
                    oponente = torre_manager.obtener_oponente_actual()
                    
                    juego = GameEngine(
                        pantalla, reloj,
                        sprites_personajes,
                        mapa_seleccionado,
                        personaje1,
                        oponente,
                        es_modo_torre=True,
                        audio_manager=audio_manager
                    )
                    juego.nivel_torre = torre_manager.pelea_actual
                    juego.ejecutar(personaje1, oponente, torre_manager.pelea_actual)
                    
                    if juego.rounds_manager.rounds_jugador1 >= 2:
                        # Jugador ganó la pelea
                        tiempo_pelea = (pygame.time.get_ticks() - juego.rounds_manager.tiempo_inicio_pelea_total) // 1000
                        stats = juego.collision_system.obtener_estadisticas()
                        torre_manager.agregar_stats_pelea(stats['jugador1'], tiempo_pelea)
                        torre_manager.avanzar_pelea()
                        
                        if not torre_manager.esta_completada():
                            if not torre_manager.mostrar_pantalla_torre():
                                torre_abandonada = True
                        else:
                            # Torre completada
                            torre_manager.mostrar_pantalla_victoria_torre()
                    else:
                        # Jugador perdió
                        torre_manager.mostrar_pantalla_game_over()
                        break
        
        elif opcion == "Personajes":
            menu_manager.menu_personajes()
        
        elif opcion == "Records":
            menu_manager.menu_records()


if __name__ == "__main__":
    main()