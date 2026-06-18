"""
Главный клиент для работы с погодным API.
Объединяет все сервисы в одном удобном интерфейсе.
"""

from .geocoding import GeocodingService
from .current_weather import CurrentWeatherService
from .forecast import ForecastService
from .air_pollution import AirPollutionService
from .exceptions import CityNotFoundError


class WeatherClient:
    """
    Основной класс для получения погодных данных.
    """
    
    def __init__(self):
        """Инициализация всех сервисов."""
        self.geocoding = GeocodingService()
        self.current_weather = CurrentWeatherService()
        self.forecast = ForecastService()
        self.air_pollution = AirPollutionService()
    
    def get_weather_by_city(self, city_name):
        """
        Получить текущую погоду по названию города.
        
        Args:
            city_name (str): Название города
            
        Returns:
            dict: Данные о текущей погоде
        """
        coords = self.geocoding.get_coordinates(city_name)
        weather = self.current_weather.get_weather(coords['lat'], coords['lon'])
        weather['city'] = city_name
        return weather
    
    def get_forecast_by_city(self, city_name, days=5):
        """
        Получить прогноз погоды по названию города.
        
        Args:
            city_name (str): Название города
            days (int): Количество дней (по умолчанию 5)
            
        Returns:
            list: Список прогнозов по дням
        """
        coords = self.geocoding.get_coordinates(city_name)
        return self.forecast.get_daily_forecast(coords['lat'], coords['lon'], days)
    
    def get_air_quality_by_city(self, city_name):
        """
        Получить качество воздуха по названию города.
        
        Args:
            city_name (str): Название города
            
        Returns:
            dict: Данные о качестве воздуха
        """
        coords = self.geocoding.get_coordinates(city_name)
        return self.air_pollution.get_air_quality(coords['lat'], coords['lon'])
    
    def compare_cities(self, city1, city2):
        """
        Сравнить погоду в двух городах.
        
        Args:
            city1 (str): Название первого города
            city2 (str): Название второго города
            
        Returns:
            dict: Словарь с разницей показателей между городами
        """
        weather1 = self.get_weather_by_city(city1)
        weather2 = self.get_weather_by_city(city2)
        
        return {
            'city1': city1,
            'city2': city2,
            'temp_difference': round(weather1['temperature'] - weather2['temperature'], 1),
            'humidity_difference': weather1['humidity'] - weather2['humidity'],
            'wind_difference': round(weather1['wind_speed'] - weather2['wind_speed'], 1),
            'weather1': weather1,
            'weather2': weather2
        }