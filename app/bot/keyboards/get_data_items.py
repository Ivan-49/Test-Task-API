from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def info_product_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    buttons = [
        "Узнать информацию о товаре",
    ]
    for button_text in buttons:
        builder.button(text=button_text)
    return builder.as_markup(resize_keyboard=True)
