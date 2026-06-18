"""
Точка входа для бота ВКонтакте.
"""

from vkbottle import Bot
from .config import VK_BOT_TOKEN
from .handlers import setup_handlers


def main():
    """Главная функция запуска бота."""
    print("="*50)
    print(" Погодный бот ВКонтакте")
    print("="*50)
    print("📡 Запуск бота...")
    
    # Создаём бота
    bot = Bot(token=VK_BOT_TOKEN)
    
    # Настраиваем обработчики
    setup_handlers(bot)
    
    print("✅ Бот успешно создан!")
    print("🔄 Ожидание сообщений...")
    print("="*50)
    print("💡 Для остановки нажмите Ctrl+C")
    print("="*50)
    
    # Запускаем бота (синхронный метод, блокирует выполнение)
    bot.run_forever()


if __name__ == "__main__":
    main()