"""
Модуль для получения прогноза погоды на 5 дней.
Использует 5 Day / 3 Hour Forecast API OpenWeatherMap.
"""

import requests
from datetime import datetime
from .config import BASE_URL, OPENWEATHER_API_KEY
from .exceptions import APIRequestError


class ForecastService:
    """Сервис для получения прогноза погоды."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.api_key = OPENWEATHER_API_KEY
        self.session = requests.Session()
    
    def get_forecast(self, lat, lon):
        """
        Получить прогноз погоды на 5 дней с шагом 3 часа.
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            
        Returns:
            list: Список из 40 записей (5 дней × 8 раз в день),
                  каждая запись содержит:
                - datetime: дата и время
                - temperature: температура (°C)
                - description: описание погоды
                - humidity: влажность (%)
                - wind_speed: скорость ветра (м/с)
                
        Raises:
            APIRequestError: Если произошла ошибка при запросе
        """
        url = f"{BASE_URL}/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  # Температура в Цельсиях
            'lang': 'ru',  # Описание на русском
            'cnt': 40  # 40 записей = 5 дней
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            forecast_list = []
            
            for item in data['list']:
                forecast_item = {
                    'datetime': datetime.fromtimestamp(item['dt']),
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'description': item['weather'][0]['description'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'pressure': item['main']['pressure']
                }
                forecast_list.append(forecast_item)
            
            return forecast_list
            
        except requests.exceptions.RequestException as e:
            raise APIRequestError(f"Ошибка при получении прогноза: {e}")
        except KeyError as e:
            raise APIRequestError(
                f"Некорректный формат ответа API: {e}"
            )
    
    def get_daily_forecast(self, lat, lon, days=5):
        """
        Получить дневной прогноз (по одному значению на день).
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            days (int): Количество дней (по умолчанию 5)
            
        Returns:
            list: Список прогнозов по дням
        """
        forecast = self.get_forecast(lat, lon)
        
        # Группируем по дням и берём среднюю температуру за день
        daily = {}
        
        for item in forecast:
            date = item['datetime'].date()
            if date not in daily:
                daily[date] = {
                    'date': date,
                    'temperatures': [],
                    'descriptions': []
                }
            daily[date]['temperatures'].append(item['temperature'])
            daily[date]['descriptions'].append(item['description'])
        
        # Формируем итоговый список
        result = []
        for i, (date, data) in enumerate(daily.items()):
            if i >= days:
                break
            
            result.append({
                'date': date,
                'temp_min': min(data['temperatures']),
                'temp_max': max(data['temperatures']),
                'temp_avg': sum(data['temperatures']) / len(data['temperatures']),
                'description': data['descriptions'][0]  # Берём первое описание
            })
        
        return result