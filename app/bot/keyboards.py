from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_product_keyboard():
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Узнать о товаре")]], resize_keyboard=True)
    return kb