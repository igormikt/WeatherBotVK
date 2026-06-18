"""
Консольное приложение для тестирования модуля OpenWeather API.
Запускается командой: python -m weather_module.cli
"""

from .client import WeatherClient
from .exceptions import WeatherAPIError


def print_weather(weather):
    """Красиво вывести данные о текущей погоде."""
    print("\n" + "="*40)
    print(f"🌍 Погода в городе: {weather['city']}")
    print("="*40)
    print(f"🌡️  Температура: {weather['temperature']}°C (ощущается как {weather['feels_like']}°C)")
    print(f"🌤️  Описание: {weather['description']}")
    print(f"💧 Влажность: {weather['humidity']}%")
    print(f"🌬️  Ветер: {weather['wind_speed']} м/с")
    print(f"📊 Давление: {weather['pressure']} гПа")
    print(f"👁️  Видимость: {weather['visibility']} км")
    print(f"🌅 Восход: {weather['sunrise'].strftime('%H:%M')}")
    print(f"🌇 Закат: {weather['sunset'].strftime('%H:%M')}")
    print("="*40 + "\n")


def print_forecast(forecast):
    """Красиво вывести прогноз на несколько дней."""
    print("\n" + "="*40)
    print("📅 Прогноз погоды на 5 дней")
    print("="*40)
    for day in forecast:
        date_str = day['date'].strftime('%d.%m.%Y')
        print(f"️  {date_str}:")
        print(f"   🌡️  {day['temp_min']}°C ... {day['temp_max']}°C (средняя {day['temp_avg']:.1f}°C)")
        print(f"   🌤️  {day['description']}")
    print("="*40 + "\n")


def print_air_quality(data):
    """Красиво вывести данные о качестве воздуха."""
    print("\n" + "="*40)
    print("🌬️  Качество воздуха")
    print("="*40)
    print(f"📊 Индекс AQI: {data['aqi']} ({data['aqi_description']})")
    print("🧪 Компоненты:")
    print(f"   CO: {data['components']['CO']} мкг/м³")
    print(f"   NO2: {data['components']['NO2']} мкг/м³")
    print(f"   O3: {data['components']['O3']} мкг/м³")
    print(f"   PM2.5: {data['components']['PM2.5']} мкг/м³")
    print(f"   PM10: {data['components']['PM10']} мкг/м³")
    print("="*40 + "\n")


def print_comparison(comparison):
    """Красиво вывести сравнение двух городов."""
    print("\n" + "="*40)
    print(f"⚖️  Сравнение: {comparison['city1']} и {comparison['city2']}")
    print("="*40)
    print(f"🌡️  Разница температур: {comparison['temp_difference']}°C")
    print(f"💧 Разница влажности: {comparison['humidity_difference']}%")
    print(f"🌬️  Разница ветра: {comparison['wind_difference']} м/с")
    print("="*40 + "\n")


def main():
    """Главная функция с меню."""
    client = WeatherClient()
    
    print(" Добро пожаловать в тестовый клиент OpenWeather API!")
    
    while True:
        print("\nВыберите действие:")
        print("1. Текущая погода по городу")
        print("2. Прогноз на 5 дней")
        print("3. Качество воздуха")
        print("4. Сравнить два города")
        print("5. Выход")
        
        choice = input("\nВаш выбор (1-5): ").strip()
        
        try:
            if choice == '1':
                city = input("Введите название города: ").strip()
                weather = client.get_weather_by_city(city)
                print_weather(weather)
                
            elif choice == '2':
                city = input("Введите название города: ").strip()
                forecast = client.get_forecast_by_city(city)
                print_forecast(forecast)
                
            elif choice == '3':
                city = input("Введите название города: ").strip()
                air = client.get_air_quality_by_city(city)
                print_air_quality(air)
                
            elif choice == '4':
                city1 = input("Введите первый город: ").strip()
                city2 = input("Введите второй город: ").strip()
                comparison = client.compare_cities(city1, city2)
                print_comparison(comparison)
                
            elif choice == '5':
                print("👋 До свидания!")
                break
                
            else:
                print("️  Неверный выбор. Попробуйте снова.")
                
        except CityNotFoundError as e:
            print(f"❌ Ошибка: {e}")
        except WeatherAPIError as e:
            print(f"❌ Ошибка API: {e}")
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()