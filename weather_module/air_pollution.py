"""
Модуль для получения данных о качестве воздуха.
Использует Air Pollution API OpenWeatherMap.
"""

import requests
from .config import AIR_POLLUTION_URL, OPENWEATHER_API_KEY
from .exceptions import APIRequestError


# Шкала интерпретации AQI (Air Quality Index)
AQI_SCALE = {
    1: "Хорошо",
    2: "Приемлемо",
    3: "Умеренно",
    4: "Плохо",
    5: "Очень плохо"
}


class AirPollutionService:
    """Сервис для получения данных о качестве воздуха."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.api_key = OPENWEATHER_API_KEY
        self.session = requests.Session()
    
    def get_air_quality(self, lat, lon):
        """
        Получить данные о качестве воздуха по координатам.
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            
        Returns:
            dict: Словарь с данными:
                - aqi: индекс качества воздуха (1-5)
                - aqi_description: текстовое описание индекса
                - components: словарь с концентрациями (CO, NO2, O3, PM2.5, PM10 и т.д.)
                
        Raises:
            APIRequestError: Если произошла ошибка при запросе
        """
        url = f"{AIR_POLLUTION_URL}/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # API возвращает список, берём первый элемент
            main_data = data['list'][0]['main']
            components = data['list'][0]['components']
            
            aqi_value = main_data['aqi']
            
            return {
                'aqi': aqi_value,
                'aqi_description': AQI_SCALE.get(aqi_value, "Неизвестно"),
                'components': {
                    'CO': components.get('co', 0),
                    'NO2': components.get('no2', 0),
                    'O3': components.get('o3', 0),
                    'PM2.5': components.get('pm2_5', 0),
                    'PM10': components.get('pm10', 0)
                }
            }
            
        except requests.exceptions.RequestException as e:
            raise APIRequestError(f"Ошибка при получении качества воздуха: {e}")
        except (KeyError, IndexError) as e:
            raise APIRequestError(f"Некорректный формат ответа API: {e}")