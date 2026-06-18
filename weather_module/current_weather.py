"""
Модуль для получения текущей погоды.
Использует Current Weather API OpenWeatherMap.
"""

import requests
from datetime import datetime
from .config import BASE_URL, OPENWEATHER_API_KEY
from .exceptions import APIRequestError


class CurrentWeatherService:
    """Сервис для получения текущей погоды."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.api_key = OPENWEATHER_API_KEY
        self.session = requests.Session()
    
    def get_weather(self, lat, lon):
        """
        Получить текущую погоду по координатам.
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            
        Returns:
            dict: Словарь с данными о погоде:
                - temperature: температура (°C)
                - feels_like: ощущается как (°C)
                - humidity: влажность (%)
                - pressure: давление (гПа)
                - wind_speed: скорость ветра (м/с)
                - description: описание погоды
                - sunrise: время восхода солнца
                - sunset: время заката солнца
                - visibility: видимость (м)
                
        Raises:
            APIRequestError: Если произошла ошибка при запросе
        """
        url = f"{BASE_URL}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  # Температура в Цельсиях
            'lang': 'ru'  # Описание на русском
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                'visibility': data.get('visibility', 0) / 1000  # Переводим в км
            }
            
        except requests.exceptions.RequestException as e:
            raise APIRequestError(f"Ошибка при получении погоды: {e}")
        except KeyError as e:
            raise APIRequestError(
                f"Некорректный формат ответа API: {e}"
            )