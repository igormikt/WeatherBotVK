"""
Пользовательские исключения для работы с OpenWeather API.
"""


class WeatherAPIError(Exception):
    """Базовое исключение для ошибок API погоды."""
    pass


class CityNotFoundError(WeatherAPIError):
    """Исключение, когда город не найден."""
    pass


class APIKeyError(WeatherAPIError):
    """Исключение при неверном API-ключе."""
    pass


class APIRequestError(WeatherAPIError):
    """Исключение при ошибке запроса к API."""
    pass


class InvalidCoordinatesError(WeatherAPIError):
    """Исключение при некорректных координатах."""
    pass