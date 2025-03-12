from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def start_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    buttons = ["/start"]
    for button_text in buttons:
        builder.button(text=button_text)
    return builder.as_markup(resize_keyboard=True)
