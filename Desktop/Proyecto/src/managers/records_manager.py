"""
Gestor de récords del juego.
Maneja el guardado y lectura de récords en formato JSON.
"""
import json
import os
from typing import List, Dict
from src.utils.config import Paths, RecordsConfig, TowerConfig


class RecordsManager:
    """Gestor de récords del juego"""
    
    def __init__(self):
        """Inicializa el gestor de récords"""
        self.archivo_1vs1 = Paths.RECORDS_1VS1
        self.archivo_torre = Paths.RECORDS_TORRE
        self.records_1vs1: List[Dict] = []
        self.records_torre: List[Dict] = []
        
        self._asegurar_carpeta_data()
        self.cargar_records_1vs1()
        self.cargar_records_torre()
    
    def _asegurar_carpeta_data(self):
        """Crea la carpeta data si no existe"""
        os.makedirs(Paths.DATA, exist_ok=True)
    
    def cargar_records_1vs1(self):
        """Carga los récords 1vs1 desde el archivo"""
        if not os.path.exists(self.archivo_1vs1):
            self.records_1vs1 = []
            return
        
        try:
            with open(self.archivo_1vs1, 'r', encoding='utf-8') as f:
                self.records_1vs1 = json.load(f)
        except Exception as e:
            print(f"Error al cargar récords 1vs1: {e}")
            self.records_1vs1 = []
    
    def cargar_records_torre(self):
        """Carga los récords de torre desde el archivo"""
        if not os.path.exists(self.archivo_torre):
            self.records_torre = []
            return
        
        try:
            with open(self.archivo_torre, 'r', encoding='utf-8') as f:
                self.records_torre = json.load(f)
        except Exception as e:
            print(f"Error al cargar récords torre: {e}")
            self.records_torre = []
    
    def guardar_records_1vs1(self):
        """Guarda los récords 1vs1 en el archivo"""
        try:
            with open(self.archivo_1vs1, 'w', encoding='utf-8') as f:
                json.dump(self.records_1vs1, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar récords 1vs1: {e}")
    
    def guardar_records_torre(self):
        """Guarda los récords de torre en el archivo"""
        try:
            with open(self.archivo_torre, 'w', encoding='utf-8') as f:
                json.dump(self.records_torre, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar récords torre: {e}")
    
    def agregar_record(self, nombre: str, stats_j1: Dict, stats_j2: Dict,
                       rounds_j1: int, rounds_j2: int, tiempo_total: int):
        """
        Agrega un nuevo récord 1vs1.
        
        Args:
            nombre: Nombre del jugador
            stats_j1: Estadísticas del jugador 1
            stats_j2: Estadísticas del jugador 2
            rounds_j1: Rounds ganados por jugador 1
            rounds_j2: Rounds ganados por jugador 2
            tiempo_total: Tiempo total en segundos
        """
        puntaje = self._calcular_puntaje_1vs1(stats_j1, rounds_j1, tiempo_total)
        
        record = {
            'nombre': nombre.upper()[:3],
            'puntaje': puntaje,
            'rounds_ganados': rounds_j1,
            'rounds_perdidos': rounds_j2,
            'golpes_totales': stats_j1['golpes_totales'],
            'dano_causado': int(stats_j1['dano_causado']),
            'dano_recibido': int(stats_j1['dano_recibido']),
            'tiempo_segundos': tiempo_total
        }
        
        self.records_1vs1.append(record)
        self._ordenar_records_1vs1()
        self.guardar_records_1vs1()
    
    def agregar_record_torre(self, nombre: str, peleas_ganadas: int, stats_totales: Dict):
        """
        Agrega un nuevo récord de torre.
        
        Args:
            nombre: Nombre del jugador
            peleas_ganadas: Número de peleas ganadas
            stats_totales: Estadísticas acumuladas
        """
        puntaje = self._calcular_puntaje_torre(peleas_ganadas, stats_totales)
        
        record = {
            'nombre': nombre.upper()[:3],
            'puntaje': max(0, puntaje),
            'peleas_ganadas': peleas_ganadas,
            'golpes_totales': stats_totales['golpes_totales'],
            'dano_causado': int(stats_totales['dano_causado']),
            'dano_recibido': int(stats_totales['dano_recibido']),
            'tiempo_segundos': stats_totales['tiempo_total']
        }
        
        self.records_torre.append(record)
        self._ordenar_records_torre()
        self.guardar_records_torre()
    
    def _calcular_puntaje_1vs1(self, stats: Dict, rounds_ganados: int, tiempo: int) -> int:
        """
        Calcula el puntaje para modo 1vs1.
        
        Args:
            stats: Estadísticas del jugador
            rounds_ganados: Rounds ganados
            tiempo: Tiempo en segundos
            
        Returns:
            int: Puntaje calculado
        """
        puntaje = 0
        puntaje += rounds_ganados * RecordsConfig.PUNTOS_POR_ROUND
        puntaje += stats['golpes_totales'] * RecordsConfig.PUNTOS_POR_GOLPE_1VS1
        puntaje += int(stats['dano_causado']) * RecordsConfig.PUNTOS_POR_DANO_1VS1
        puntaje -= int(stats['dano_recibido']) * RecordsConfig.PENALIZACION_DANO_1VS1
        
        # Bonus por tiempo
        if tiempo < 60:
            puntaje += RecordsConfig.BONUS_TIEMPO_60
        elif tiempo < 120:
            puntaje += RecordsConfig.BONUS_TIEMPO_120
        elif tiempo < 180:
            puntaje += RecordsConfig.BONUS_TIEMPO_180
        
        return max(0, puntaje)
    
    def _calcular_puntaje_torre(self, peleas_ganadas: int, stats: Dict) -> int:
        """
        Calcula el puntaje para modo torre.
        
        Args:
            peleas_ganadas: Número de peleas ganadas
            stats: Estadísticas acumuladas
            
        Returns:
            int: Puntaje calculado
        """
        puntaje = 0
        puntaje += peleas_ganadas * TowerConfig.PUNTOS_POR_PELEA_GANADA
        puntaje += stats['golpes_totales'] * TowerConfig.PUNTOS_POR_GOLPE
        puntaje += int(stats['dano_causado']) * TowerConfig.PUNTOS_POR_DANO_CAUSADO
        puntaje -= int(stats['dano_recibido']) * TowerConfig.PENALIZACION_POR_DANO_RECIBIDO
        
        # Bonus por completar torre
        if peleas_ganadas == TowerConfig.NUMERO_PELEAS:
            puntaje += TowerConfig.BONUS_COMPLETAR_TORRE
        
        # Bonus por tiempo
        tiempo_total = stats['tiempo_total']
        if tiempo_total < 180:
            puntaje += TowerConfig.BONUS_TIEMPO_RAPIDO_180
        elif tiempo_total < 300:
            puntaje += TowerConfig.BONUS_TIEMPO_RAPIDO_300
        
        return puntaje
    
    def _ordenar_records_1vs1(self):
        """Ordena los récords 1vs1 por puntaje"""
        self.records_1vs1.sort(key=lambda x: x['puntaje'], reverse=True)
    
    def _ordenar_records_torre(self):
        """Ordena los récords de torre por puntaje"""
        self.records_torre.sort(key=lambda x: x['puntaje'], reverse=True)
    
    def obtener_top_records_1vs1(self, cantidad: int = 10) -> List[Dict]:
        """
        Obtiene los mejores récords 1vs1.
        
        Args:
            cantidad: Número de récords a retornar
            
        Returns:
            List[Dict]: Lista de récords
        """
        return self.records_1vs1[:cantidad]
    
    def obtener_top_records_torre(self, cantidad: int = 10) -> List[Dict]:
        """
        Obtiene los mejores récords de torre.
        
        Args:
            cantidad: Número de récords a retornar
            
        Returns:
            List[Dict]: Lista de récords
        """
        return self.records_torre[:cantidad]