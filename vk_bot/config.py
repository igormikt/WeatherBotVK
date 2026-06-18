"""
Конфигурация бота ВКонтакте.
Загружает токен из переменных окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Получаем токен бота ВКонтакте
VK_BOT_TOKEN = os.getenv('VK_BOT_TOKEN')

# Проверка наличия токена
if not VK_BOT_TOKEN:
    raise ValueError("Токен VK бота не найден. Проверьте файл .env")

# ID администратора (опционально, для отладки)
ADMIN_ID = os.getenv('ADMIN_ID', None)