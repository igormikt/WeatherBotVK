"""
Обработчики сообщений для бота ВКонтакте.
Универсальный подход — один обработчик на все сообщения.
"""

from vkbottle import Bot
from vkbottle.bot import Message
from weather_module import WeatherClient
from .keyboard import get_main_keyboard, get_back_keyboard


# Создаём клиента для работы с погодой
weather_client = WeatherClient()

# Словарь для хранения состояния пользователей
user_states = {}


def format_weather_message(city, weather):
    """Отформатировать сообщение с текущей погодой."""
    message = f"""🌍 Погода в городе {city}

🌡️ Температура: {weather['temperature']}°C
   Ощущается как: {weather['feels_like']}°C

️ {weather['description'].capitalize()}

 Влажность: {weather['humidity']}%
️ Ветер: {weather['wind_speed']} м/с
📊 Давление: {weather['pressure']} гПа
👁️ Видимость: {weather['visibility']} км

 Восход: {weather['sunrise'].strftime('%H:%M')}
🌇 Закат: {weather['sunset'].strftime('%H:%M')}"""
    return message


def format_forecast_message(city, forecast):
    """Отформатировать сообщение с прогнозом на 5 дней."""
    message = f"📅 Прогноз погоды для {city} на 5 дней\n\n"
    for day in forecast:
        date_str = day['date'].strftime('%d.%m.%Y (%A)')
        message += f"🗓️ {date_str}\n"
        message += f"   🌡️ {day['temp_min']}°C ... {day['temp_max']}°C\n"
        message += f"   🌤️ {day['description'].capitalize()}\n\n"
    return message


def format_air_quality_message(city, air_data):
    """Отформатировать сообщение о качестве воздуха."""
    aqi_emojis = {1: "✅", 2: "🟢", 3: "🟡", 4: "🟠", 5: "🔴"}
    emoji = aqi_emojis.get(air_data['aqi'], "❓")
    
    message = f"""🌬️ Качество воздуха в городе {city}

{emoji} Индекс AQI: {air_data['aqi']} ({air_data['aqi_description']})

🧪 Состав воздуха:
• CO: {air_data['components']['CO']:.1f} мкг/м³
• NO2: {air_data['components']['NO2']:.1f} мкг/м³
• O3: {air_data['components']['O3']:.1f} мкг/м³
• PM2.5: {air_data['components']['PM2.5']:.1f} мкг/м³
• PM10: {air_data['components']['PM10']:.1f} мкг/м³"""
    return message


def format_comparison_message(comparison):
    """Отформатировать сообщение со сравнением двух городов."""
    city1 = comparison['city1']
    city2 = comparison['city2']
    temp_diff = comparison['temp_difference']
    warmer = city1 if temp_diff > 0 else city2
    
    message = f"""⚖️ Сравнение: {city1} и {city2}

🌡️ Температура:
   {city1}: {comparison['weather1']['temperature']}°C
   {city2}: {comparison['weather2']['temperature']}°C
   Разница: {abs(temp_diff)}°C
   🔥 Теплее в {warmer}

💧 Влажность:
   {city1}: {comparison['weather1']['humidity']}%
   {city2}: {comparison['weather2']['humidity']}%
   Разница: {abs(comparison['humidity_difference'])}%

🌬️ Ветер:
   {city1}: {comparison['weather1']['wind_speed']} м/с
   {city2}: {comparison['weather2']['wind_speed']} м/с
   Разница: {abs(comparison['wind_difference'])} м/с"""
    return message


async def send_welcome_message(message: Message):
    """Отправить приветственное сообщение с меню."""
    welcome_text = """👋 Привет! Я погодный бот!

Я могу помочь тебе узнать:
• 🌤️ Текущую погоду в любом городе
• 📅 Прогноз на 5 дней
• 🌬️ Качество воздуха
• ⚖️ Сравнить погоду в двух городах
• 📍 Определить погоду по геолокации

Выбери команду из меню ниже!"""
    await message.answer(welcome_text, keyboard=get_main_keyboard())


async def handle_current_weather(message: Message, city: str = None):
    """Обработчик команды получения текущей погоды."""
    if not city:
        await message.answer("🏙️ Введите название города:", keyboard=get_back_keyboard())
        user_states[message.from_id] = {'state': 'waiting_city_current'}
        return
    try:
        weather = weather_client.get_weather_by_city(city)
        text = format_weather_message(city, weather)
        await message.answer(text, keyboard=get_main_keyboard())
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def handle_forecast(message: Message, city: str = None):
    """Обработчик команды получения прогноза на 5 дней."""
    if not city:
        await message.answer("🏙️ Введите название города для прогноза:", keyboard=get_back_keyboard())
        user_states[message.from_id] = {'state': 'waiting_city_forecast'}
        return
    try:
        forecast = weather_client.get_forecast_by_city(city)
        text = format_forecast_message(city, forecast)
        await message.answer(text, keyboard=get_main_keyboard())
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def handle_air_quality(message: Message, city: str = None):
    """Обработчик команды получения качества воздуха."""
    if not city:
        await message.answer("🏙️ Введите название города:", keyboard=get_back_keyboard())
        user_states[message.from_id] = {'state': 'waiting_city_air'}
        return
    try:
        air_data = weather_client.get_air_quality_by_city(city)
        text = format_air_quality_message(city, air_data)
        await message.answer(text, keyboard=get_main_keyboard())
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def handle_compare_cities(message: Message):
    """Обработчик команды сравнения двух городов."""
    await message.answer("🏙️ Введите первый город:", keyboard=get_back_keyboard())
    user_states[message.from_id] = {'state': 'waiting_compare_city1'}


async def handle_geo_location(message: Message):
    """Обработчик команды получения погоды по геолокации."""
    await message.answer(
        "📍 Отправьте мне ваше местоположение (кнопка  → Местоположение)",
        keyboard=get_back_keyboard()
    )
    user_states[message.from_id] = {'state': 'waiting_geo'}


async def handle_location(message: Message, lat: float, lon: float):
    """Обработчик полученной геолокации."""
    try:
        city_name = weather_client.geocoding.get_city_name(lat, lon)
        weather = weather_client.current_weather.get_weather(lat, lon)
        text = format_weather_message(city_name, weather)
        await message.answer(text, keyboard=get_main_keyboard())
    except Exception as e:
        await message.answer(f"❌ Ошибка определения местоположения: {e}")


async def handle_text_message(message: Message):
    """Обработчик обычных текстовых сообщений."""
    text = message.text.strip()
    text_lower = text.lower()
    user_id = message.from_id
    
    # Проверяем состояние пользователя
    if user_id in user_states:
        state = user_states[user_id]['state']
        
        # Команды отмены работают в любом состоянии
        if text_lower in ['назад', 'отмена', 'меню']:
            await send_welcome_message(message)
            del user_states[user_id]
            return
        
        if state == 'waiting_city_current':
            await handle_current_weather(message, text)
            del user_states[user_id]
        elif state == 'waiting_city_forecast':
            await handle_forecast(message, text)
            del user_states[user_id]
        elif state == 'waiting_city_air':
            await handle_air_quality(message, text)
            del user_states[user_id]
        elif state == 'waiting_compare_city1':
            user_states[user_id] = {
                'state': 'waiting_compare_city2',
                'data': {'city1': text}
            }
            await message.answer(
                f"️ Теперь введите второй город для сравнения с {text}:",
                keyboard=get_back_keyboard()
            )
        elif state == 'waiting_compare_city2':
            city1 = user_states[user_id]['data']['city1']
            try:
                comparison = weather_client.compare_cities(city1, text)
                text_msg = format_comparison_message(comparison)
                await message.answer(text_msg, keyboard=get_main_keyboard())
            except Exception as e:
                await message.answer(f"❌ Ошибка сравнения: {e}")
            del user_states[user_id]
        elif state == 'waiting_geo':
            await message.answer(
                "📍 Пожалуйста, отправьте местоположение через кнопку 📎",
                keyboard=get_back_keyboard()
            )
        else:
            del user_states[user_id]
            await send_welcome_message(message)
    else:
        # Нет состояния — проверяем текст на команды
        if text_lower in ['начать', 'start', 'привет', '/start', 'помощь', 'help', 'меню']:
            await send_welcome_message(message)
        elif text_lower in ['погода', 'current']:
            await handle_current_weather(message)
        elif text_lower in ['прогноз', 'forecast']:
            await handle_forecast(message)
        elif text_lower in ['качество', 'air']:
            await handle_air_quality(message)
        elif text_lower in ['сравнить', 'compare']:
            await handle_compare_cities(message)
        elif text_lower in ['гео', 'локация', 'geo']:
            await handle_geo_location(message)
        else:
            # Если текст похож на название города — сразу показываем погоду
            if len(text) > 2 and text[0].isupper():
                await handle_current_weather(message, text)
            else:
                await send_welcome_message(message)


def setup_handlers(bot: Bot):
    """Настроить обработчики для бота — ОДИН универсальный обработчик."""
    
    @bot.on.message()
    async def universal_handler(message: Message):
        """Универсальный обработчик всех сообщений."""
        # Сначала проверяем геолокацию
        if hasattr(message, 'geo') and message.geo:
            try:
                geo = message.geo
                # В vkbottle 4.x geo может быть объектом или dict
                if hasattr(geo, 'coordinates'):
                    lat = geo.coordinates.get('latitude') or geo.coordinates.get('lat')
                    lon = geo.coordinates.get('longitude') or geo.coordinates.get('lon')
                elif isinstance(geo, dict):
                    coords = geo.get('coordinates', {})
                    lat = coords.get('latitude') or coords.get('lat')
                    lon = coords.get('longitude') or coords.get('lon')
                else:
                    lat = getattr(geo, 'latitude', None) or getattr(geo, 'lat', None)
                    lon = getattr(geo, 'longitude', None) or getattr(geo, 'lon', None)
                
                if lat and lon:
                    await handle_location(message, float(lat), float(lon))
                    return
            except Exception as e:
                await message.answer(f"❌ Ошибка обработки геолокации: {e}")
                return
        
        # Проверяем payload (кнопки клавиатуры)
        if message.payload:
            try:
                payload = message.payload
                if isinstance(payload, str):
                    import json
                    payload = json.loads(payload)
                
                cmd = payload.get('command')
                if cmd == 'current':
                    await handle_current_weather(message)
                elif cmd == 'forecast':
                    await handle_forecast(message)
                elif cmd == 'air_quality':
                    await handle_air_quality(message)
                elif cmd == 'compare':
                    await handle_compare_cities(message)
                elif cmd == 'geo':
                    await handle_geo_location(message)
                elif cmd in ['back', 'cancel']:
                    await send_welcome_message(message)
                elif 'city' in payload:
                    await handle_current_weather(message, payload['city'])
                else:
                    await handle_text_message(message)
            except Exception:
                await handle_text_message(message)
        else:
            # Обычное текстовое сообщение
            await handle_text_message(message)