from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def item_keyboard():
    builder = ReplyKeyboardBuilder()
    buttons = [
        "Получить информацию о товаре",
        "Подписаться на обновление данных о товаре",
        "Посмотреть AI Анализ товара",
        "Посмотреть аналоги",
        "Получить данные за последнее время",
    ]
    for button_text in buttons:
        builder.button(text=button_text)
    builder.adjust(2)  # Разбиваем по 2 кнопки в строке
    return builder.as_markup(
        resize_keyboard=True, input_field_placeholder="Выберите действие"
    )
