from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def helper_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    buttons = ["Продолжить", "Закончить"]
    for button_text in buttons:
        builder.button(text=button_text)
    return builder.as_markup(resize_keyboard=True)
