"""
Клавиатуры для бота ВКонтакте (vkbottle 4.x).
"""

from vkbottle import Keyboard, KeyboardButtonColor, Text


def get_main_keyboard():
    """Главная клавиатура с основными функциями."""
    keyboard = Keyboard(one_time=False, inline=False)
    
    # Добавляем кнопки без параметра color — цвет задаётся отдельно
    keyboard.add(Text("🌤️ Погода сейчас", payload={"command": "current"}))
    keyboard.row()
    
    keyboard.add(Text("📅 Прогноз на 5 дней", payload={"command": "forecast"}))
    keyboard.row()
    
    keyboard.add(Text("🌬️ Качество воздуха", payload={"command": "air_quality"}))
    keyboard.row()
    
    keyboard.add(Text("⚖️ Сравнить города", payload={"command": "compare"}))
    keyboard.row()
    
    keyboard.add(Text("📍 Мой город (геолокация)", payload={"command": "geo"}))
    
    return keyboard


def get_back_keyboard():
    """Клавиатура с кнопкой 'Назад в меню'."""
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("↩️ Назад в меню", payload={"command": "back"}))
    return keyboard