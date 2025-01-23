from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_product_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Получить данные по товару"))
    return kb