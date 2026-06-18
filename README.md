# 🌤️ Погодный бот ВКонтакте

Бот для получения актуальной погоды, прогноза на 5 дней, качества воздуха и сравнения городов.

## 🚀 Возможности

- ️ **Текущая погода** — температура, влажность, ветер, давление
- 📅 **Прогноз на 5 дней** — с шагом 3 часа
- 🌬️ **Качество воздуха** — индекс AQI и состав загрязнений
- ⚖️ **Сравнение городов** — разница температуры, влажности, ветра
- 📍 **Геолокация** — погода по координатам пользователя

## ️ Технологии

- Python 3.14
- [vkbottle](https://github.com/vkbottle/vkbottle) — библиотека для VK ботов
- [OpenWeather API](https://openweathermap.org/api) — погодные данные
- requests — HTTP-запросы
- python-dotenv — работа с переменными окружения

##  Структура проекта

WeatherBotVK/
├── .env                    # Секретные ключи (НЕ публикуется!)
├── .gitignore
├── requirements.txt        # Зависимости
├── README.md
├── weather_module/         # Модуль OpenWeather API
│   ├── init.py
│   ├── config.py
│   ├── exceptions.py
│   ├── geocoding.py
│   ├── current_weather.py
│   ├── forecast.py
│   ├── air_pollution.py
│   ├── client.py
│   └── cli.py
└── vk_bot/                 # Бот ВКонтакте
    ├── init.py
    ├── config.py
    ├── keyboard.py
    ├── handlers.py
    └── main.py


## ⚙️ Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd WeatherBotVK

2. Создайте виртуальное окружение
python -m venv venv

3. Активируйте окружение
.\venv\Scripts\Activate.ps1

4. Установите зависимости
pip install -r requirements.txt

5. Запустите бота
python -m vk_bot.main

6. Тестирование модуля (опционально)
python -m weather_module.cli

🔑 Получение API-ключей
OpenWeather API

    Зарегистрируйтесь на openweathermap.org
    Подтвердите email
    Перейдите в профиль → My API Keys
    Создайте новый ключ

VK Bot Token

    Создайте сообщество ВКонтакте
    Управление → Сообщения → включите
    Настройки для бота → включите возможности ботов
    Управление → Дополнительно → Работа с API → LongPoll API
    Создайте ключ с правами на сообщения

Настройка LongPoll API
В разделе LongPoll API → Типы событий включите:

    ✅ Входящее сообщение
    ✅ Исходящее сообщение

📄 Лицензия
MIT License






