from aiogram.utils.keyboard import ReplyKeyboardBuilder

def info_product_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Узнать информацию о товаре")
    return builder.as_markup(resize_keyboard=True)