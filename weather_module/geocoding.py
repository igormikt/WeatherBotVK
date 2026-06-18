"""
Модуль для геокодинга (преобразование между названием города и координатами).
Использует Geocoding API OpenWeatherMap.
"""

import requests
from .config import GEOCODING_URL, OPENWEATHER_API_KEY
from .exceptions import CityNotFoundError, APIRequestError


class GeocodingService:
    """Сервис для работы с геокодингом."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.api_key = OPENWEATHER_API_KEY
        self.session = requests.Session()
    
    def get_coordinates(self, city_name):
        """
        Получить координаты города по его названию.
        
        Args:
            city_name (str): Название города
            
        Returns:
            dict: Словарь с координатами {'lat': float, 'lon': float}
            
        Raises:
            CityNotFoundError: Если город не найден
            APIRequestError: Если произошла ошибка при запросе
        """
        url = f"{GEOCODING_URL}/direct"
        params = {
            'q': city_name,
            'limit': 1,  # Берём первый результат
            'appid': self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise CityNotFoundError(f"Город '{city_name}' не найден")
            
            return {
                'lat': data[0]['lat'],
                'lon': data[0]['lon']
            }
            
        except requests.exceptions.RequestException as e:
            raise APIRequestError(f"Ошибка при геокодинге города: {e}")
    
    def get_city_name(self, lat, lon):
        """
        Получить название города по координатам (обратный геокодинг).
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            
        Returns:
            str: Название города
            
        Raises:
            CityNotFoundError: Если место не найдено
            APIRequestError: Если произошла ошибка при запросе
        """
        url = f"{GEOCODING_URL}/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'limit': 1,
            'appid': self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise CityNotFoundError(
                    f"Место с координатами ({lat}, {lon}) не найдено"
                )
            
            # Возвращаем название города и страну
            city = data[0].get('name', 'Неизвестное место')
            country = data[0].get('country', '')
            
            return f"{city}, {country}" if country else city
            
        except requests.exceptions.RequestException as e:
            raise APIRequestError(
                f"Ошибка при обратном геокодинге: {e}"
            )