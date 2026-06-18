"""
Конфигурация модуля OpenWeather API.
Загружает API-ключ из переменных окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Получаем API-ключ из переменной окружения
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Базовые URL для различных API OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5"
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0"
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5"

# Проверка наличия API-ключа
if not OPENWEATHER_API_KEY:
    raise ValueError("API-ключ OpenWeather не найден. Проверьте файл .env")