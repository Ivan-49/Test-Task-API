from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def sub_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    buttons = ["Да я хочу это сделать"]
    for button_text in buttons:
        builder.button(text=button_text)
    return builder.as_markup(resize_keyboard=True)
